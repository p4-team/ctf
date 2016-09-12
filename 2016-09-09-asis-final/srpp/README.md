## Dam (Crypto, 277p)

###ENG
[PL](#pl-version)

In the task we get access to a service providing some form of encryption.
The server challenges us for a PoW before we can interact, so first we had to solve the PoW, but it was the same as for some others tasks (prefix for string giving some hash value).
After beating the PoW we could query the server for encryption code, key generation code, encrypted flag with current session key, current public session key and we could also encrypt something.

The encryption code is:

```python
def encrypt(msg, pubkey):
    n, g, u = pubkey
    u += 1
    r = getRandomRange(1, n ** u - 1)
    enc = pow(g, msg, n ** u) * pow(r, n ** u, n ** u) % n ** u
    return enc
```

It looked very much like Paillier Cryptosystem so a little googling told us that this is actually a generalized version known as Damgård–Jurik Cryptosystem: https://en.wikipedia.org/wiki/Damgård–Jurik_cryptosystem

It looks almost as the textbook implementation so we didn't expect vulnerability here.

The key generation scheme was:

```python
def get_keypair(kbit, u):
    l = getRandomRange(kbit >> 4, kbit)
    p = long(gmpy.next_prime(2 << l))
    q = long(getPrime(kbit - l - 1))
    n = p * q
    d = (p - 1) * (q - 1) / GCD(p - 1, q - 1)
    r = getRandomRange(1, n - 1)
    while True:
        t = getRandomRange(1, n - 1)
        if GCD(t, n) == 1:
            break
    g = pow(n + 1, t, n ** (u + 1)) * r % n ** (u + 1)
    pubkey = (n, g, u)
    privkey = (n, d)
    return pubkey, privkey
```

At first glance it also looked fine, but after a while we noticed an interesting issue.
The estimated `kbit` value, judging by some public keys we got, was just 512 bits.
This means that `kbit >> 4` is actually `32`! 
So the range for the first prime is between 32 and 512 bits, and for the second prime between 0 and 479 bits!

This doesn't sound very safe, when the primes are not similar in size.
Since for every connection we get a new key, we can expect that at some point we will get a key with reasonably small factor.
For this we wrote a script to grab some public keys and corresponding encrypted flags for them:

```python
import codecs
import hashlib
import re
import socket
import itertools
import string
from time import sleep


def recvuntil(s, tails):
    data = ""
    while True:
        for tail in tails:
            if tail in data:
                return data
        data += s.recv(1)


def proof_of_work(s):
    data = recvuntil(s, ["Enter X:"])
    x_suffix, hash_prefix = re.findall("X \+ \"(.*)\"\)\.hexdigest\(\) = \"(.*)\.\.\.\"", data)[0]
    len = int(re.findall("\|X\| = (.*)", data)[0])
    print(data)
    print(x_suffix, hash_prefix, len)
    for x in itertools.product(string.ascii_letters + string.digits, repeat=len):
        c = "".join(list(x))
        h = hashlib.sha512(c + x_suffix).hexdigest()
        if h.startswith(hash_prefix):
            return c


def grab_data(s):
    s.sendall("G\n")  # get public key
    sleep(1)
    public = recvuntil(s, "\n") + recvuntil(s, "\n")
    s.recv(99999)
    s.sendall("S\n")  # get flag
    sleep(1)
    encflag = recvuntil(s, "\n")
    s.recv(99999)
    return public, encflag


def main():
    while True:
        try:
            url = "dam.asis-ctf.ir"
            port = 34979
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((url, port))
            x = proof_of_work(s)
            print(x)
            s.sendall(x + "\n")
            sleep(2)
            data = s.recv(9999)
            print(data)
            public, encflag = grab_data(s)
            with codecs.open("data.txt", "a") as keys_data:
                keys_data.write(public)
                keys_data.write(encflag + "\n")
        except:
            pass


main()
```

This way we got quite a few keys after a while.
Next step was to find the appropriate modulus with small factor - we simply passed the data to YAFU with some timeout and hoped for the best.
Fortunately we got the data we hoped for:

```
p = 531457043239
q = 24388660549343689307668728357759111763660922989570087116087163747073216709529418907189891430183531024686147899385989241370687309994439728955541
n = 12961525424113842581457481341117729721726176698202598934475332596021163792495193687500962257794764397492324080568328705801930173334863551881104393545637299
g = 2132051839750573299754854507364380969444028499581423474830053011031379601163074792669440458939453573346412661307966491517309566840273475971253252815424138851541945813878339754880371934727997401840883756793174023026387912833787561873964774343104161427421558277429398462610380913199026766005036911561111911498015614446521644547923419768095811788791898552705927717854674901759443511325189376351325806917211560457327283300074902178726201347950069589670988213859630524059734789901571017367997352139514205408014889400527318603702898182503607166931422225113192039575979803468157633585201622512457745586383739179657894475772
u = 3
flag = 16146846956417499078189378495360455759223869595378485457630764561369105704825747347552639327825348858161202688846334168331082417561328878910128831138772951255714265696309304528530025841643933748756877476450078970791315331759262515894580524581915667726800504296931313616859751122921688756817297843797340121021959810015729726300012075071651090158205135737206806416627610169333331691704947002581388291641532314716891417238670535879838292937496483821606837803344591931921999217676036196239569436244254894652087250116786992703898654314284929464910202202816397917119926061000276191503543076180026132619912576609446737065690
```

We got a modulus with a very small factor, just 39 bits in size.
This means we could now recover the private key, which in this case was LCM.

With the private key now the last thing to do was to decrypt the flag corresponding to our broken key.
This proved to be a problem since we couldn't find an implementation for this algorithm, which would not be a simplified version.

So we ended up grabbing the paper: http://www.brics.dk/RS/00/45/BRICS-RS-00-45.pdf and coding this on our own:

```python
def L(x):
    return (x - 1) / n


def decrypt(ct, d, n, s):
    ns1 = pow(n, s + 1)
    a = pow(ct, d, ns1)
    i = 0
    for j in range(1, s + 1):
        t1 = L(a % pow(n, j + 1))
        t2 = i
        for k in range(2, j + 1):
            i -= 1
            t2 = (t2 * i) % pow(n, j)
            factorial = long(gmpy2.factorial(k))
            up = (t2 * pow(n, k - 1))
            down = gmpy2.invert(factorial, pow(n, j))
            t1 = (t1 - up * down) % pow(n, j)
        i = t1
    return i
```

With this function we could now decrypt the flag ciphertext to get `jmd mod n^s` and by decrypting `g` value we could get `jd mod n^s` and modinv of this value to get plain `m`:

```python
ns = pow(n, u)
jd = decrypt(g, d, n, u)
jd_inv = gmpy2.invert(jd, ns)
jmd = decrypt(flag, d, n, u)
f = (jd_inv * jmd) % ns
print("decrypted flag = " + long_to_bytes(f))
```

###PL version

W zadaniu dostajemy dostęp do serwisu umożliwiającego jakąś formę szyfrowania.
Serwer wymaga od nas rozwiązania PoW aby móc z niego korzystać, więc musieliśmy najpierw rozwiązać PoW, niemniej było takie samo jak dla innych zadań (prefix dla stringu dającego odpowiednią wartość hasha).
Po pokonaniu PoW mogliśmy uzyskać od serwisu algorytm szyfrowania, algorytm generacji klucza sesji, zaszyfrowaną kluczem sesji flagę, aktualny klucz publiczny sesji oraz mogliśmy też sami coś zaszyfrować.

Kod szyfrowania:

```python
def encrypt(msg, pubkey):
    n, g, u = pubkey
    u += 1
    r = getRandomRange(1, n ** u - 1)
    enc = pow(g, msg, n ** u) * pow(r, n ** u, n ** u) % n ** u
    return enc
```

Wyglądał bardzo podobnie do Kryptosystemu Pailliera i po chwili googlowania znaleźliśmy informacje że jest to wersja uogóliona, znana jako Kryptosystem Damgård–Jurik: https://en.wikipedia.org/wiki/Damgård–Jurik_cryptosystem

Implementacja wyglądała na książkową, więc nie spodziewaliśmy się tutaj podatności.

Algorytm generacji klucza:

```python
def get_keypair(kbit, u):
    l = getRandomRange(kbit >> 4, kbit)
    p = long(gmpy.next_prime(2 << l))
    q = long(getPrime(kbit - l - 1))
    n = p * q
    d = (p - 1) * (q - 1) / GCD(p - 1, q - 1)
    r = getRandomRange(1, n - 1)
    while True:
        t = getRandomRange(1, n - 1)
        if GCD(t, n) == 1:
            break
    g = pow(n + 1, t, n ** (u + 1)) * r % n ** (u + 1)
    pubkey = (n, g, u)
    privkey = (n, d)
    return pubkey, privkey
```

Na pierwszy rzut oka wygląda ok, ale po chwili zastanowienia zauważliśmy interesujący fakt.
Szacowana przez nas wartość `kbit`, na podstawie kluczy publicznych które wyciagnęliśmy, wynosiła tylko 512 bitów.
To oznacza że `kbit >> 4` to raptem `32`!
Więc zsięg dla jednej z liczb to pomiędzy 32 a 512 bitów a dla drugiej pomiędzy 0 a 479 bitów!

To nie brzmi zbyt bezpiecznie kiedy liczby pierwsze nie są podobnego rozmiaru.
Ponieważ co połączenie dostajemy nowy klucz sesji, możemy oczekiwać, że kiedyś trafi nam się taki z względnie małym czynnikiem.
W związku z tym napisaliśmy skrypt do pobrania kluczy publicznych i pasujących do nich flag:

```python
import codecs
import hashlib
import re
import socket
import itertools
import string
from time import sleep


def recvuntil(s, tails):
    data = ""
    while True:
        for tail in tails:
            if tail in data:
                return data
        data += s.recv(1)


def proof_of_work(s):
    data = recvuntil(s, ["Enter X:"])
    x_suffix, hash_prefix = re.findall("X \+ \"(.*)\"\)\.hexdigest\(\) = \"(.*)\.\.\.\"", data)[0]
    len = int(re.findall("\|X\| = (.*)", data)[0])
    print(data)
    print(x_suffix, hash_prefix, len)
    for x in itertools.product(string.ascii_letters + string.digits, repeat=len):
        c = "".join(list(x))
        h = hashlib.sha512(c + x_suffix).hexdigest()
        if h.startswith(hash_prefix):
            return c


def grab_data(s):
    s.sendall("G\n")  # get public key
    sleep(1)
    public = recvuntil(s, "\n") + recvuntil(s, "\n")
    s.recv(99999)
    s.sendall("S\n")  # get flag
    sleep(1)
    encflag = recvuntil(s, "\n")
    s.recv(99999)
    return public, encflag


def main():
    while True:
        try:
            url = "dam.asis-ctf.ir"
            port = 34979
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((url, port))
            x = proof_of_work(s)
            print(x)
            s.sendall(x + "\n")
            sleep(2)
            data = s.recv(9999)
            print(data)
            public, encflag = grab_data(s)
            with codecs.open("data.txt", "a") as keys_data:
                keys_data.write(public)
                keys_data.write(encflag + "\n")
        except:
            pass


main()
```

W ten sposób pobraliśmy trochę kluczy po jakimś czasie.
Następny krok to znalezienie odpowiedniego modulusa z małym czynnikiem - po prostu wysłaliśmy uzyskane modulusu do YAFU z timeoutem i trzymaliśmy kciuki.
Na szczęście udało się dość szybko i dostaliśmy:

g = 2132051839750573299754854507364380969444028499581423474830053011031379601163074792669440458939453573346412661307966491517309566840273475971253252815424138851541945813878339754880371934727997401840883756793174023026387912833787561873964774343104161427421558277429398462610380913199026766005036911561111911498015614446521644547923419768095811788791898552705927717854674901759443511325189376351325806917211560457327283300074902178726201347950069589670988213859630524059734789901571017367997352139514205408014889400527318603702898182503607166931422225113192039575979803468157633585201622512457745586383739179657894475772
u = 3
flag = 16146846956417499078189378495360455759223869595378485457630764561369105704825747347552639327825348858161202688846334168331082417561328878910128831138772951255714265696309304528530025841643933748756877476450078970791315331759262515894580524581915667726800504296931313616859751122921688756817297843797340121021959810015729726300012075071651090158205135737206806416627610169333331691704947002581388291641532314716891417238670535879838292937496483821606837803344591931921999217676036196239569436244254894652087250116786992703898654314284929464910202202816397917119926061000276191503543076180026132619912576609446737065690

Więc mieliśmy modulus z małym czynnikiem, raptem 39 bitów.
To oznacza że mogliśmy teraz odzyskać klucz prywatny za pomocą LCM.

Z kluczem prywatnym pozostało nam już tylko odszyfrować flagę pasującą do złamanego klucza.
To okazało się problematyczne, bo nie mogliśmy nigdzie znaleźć implementacji tego algorytmu w wersji nie-uproszczonej.

Więc finalnie wzięliśmy publikacje: http://www.brics.dk/RS/00/45/BRICS-RS-00-45.pdf i zaimplementowaliśmy kod samodzielnie:

```python
def L(x):
    return (x - 1) / n


def decrypt(ct, d, n, s):
    ns1 = pow(n, s + 1)
    a = pow(ct, d, ns1)
    i = 0
    for j in range(1, s + 1):
        t1 = L(a % pow(n, j + 1))
        t2 = i
        for k in range(2, j + 1):
            i -= 1
            t2 = (t2 * i) % pow(n, j)
            factorial = long(gmpy2.factorial(k))
            up = (t2 * pow(n, k - 1))
            down = gmpy2.invert(factorial, pow(n, j))
            t1 = (t1 - up * down) % pow(n, j)
        i = t1
    return i
```

Z tą funkcja mogliśmy teraz odszyfrować flagę dostając `jmd mod n^s` a deszyfrując `g` dostaliśmy `jd mod n^s` z którego wyliczyliśmy modinv aby uzyskać wartość `m`:

```python
ns = pow(n, u)
jd = decrypt(g, d, n, u)
jd_inv = gmpy2.invert(jd, ns)
jmd = decrypt(flag, d, n, u)
f = (jd_inv * jmd) % ns
print("decrypted flag = " + long_to_bytes(f))
```