## Simple (crypro, 100p, 86 solves)

> Become admin!  
> http://52.69.244.164:51913

> [simple-01018f60e497b8180d6c92237e2b3a67.rb](simple.rb)

### PL

Możemy wykonać HTTP `GET` oraz `POST` do podanej usługi. `POST` szyfruje JSONa złożonego z podanego loginu oraz hasła 128-bitowym AESem w trybie CFB. `GET` deszyfruje go i sprawdza czy JSON ma pole `'admin': true`. Jeżeli tak, to podaje nam flagę. Klucz AESa jest stały i prywatny, a IV generowany losowo i przypinany do ciphertekstu.

Tryb CFB nasz ciphertekst generuje w blokach xorując zaszyfrowany klucz z naszą wiadomością. Używa w tym procesie obecny blok do zaszyfrowania następnego. Oznacza to, że nie możemy zmodyfikować dwóch bloków, które następują po sobie bez sprawienia, że deszyfracja zacznie produkować śmieci.

Sposób w jaki tworzony jest ten konkretny JSON sprawia że niemożliwa jest zmiana tylko ostatniego bloku - nie możemy dodać nowego pola modyfikując tylko 16 ostatnich znaków ciągu `{ ... "password":"provided_password","db":"hitcon-ctf"}`. Możemy natomiast zmodyfikować przedostatni, a ostatni całkowicie wyciąć (po prostu przycinając ciphertext). Możemy również pobawić się z pierwszym blokiem oraz IV, ale wybraliśmy tą pierwsza metodę.

Oto nasz solver:

```python
import requests
import urllib2

response = requests.post('http://52.69.244.164:51913/', data={'username': 'aaa', 'password': 'bbbbbbbbbbbbbbbbbbbbbbbbbbbb'}, allow_redirects=False)
cookie = urllib2.unquote(response.cookies['auth'])

source = 'bbbbbbbbbbbb","db":"hitcon-ctf"}'
target = 'bbb","admin":true}              '

def xor(x, y):
    return ''.join(chr(ord(c1) ^ ord(c2)) for c1, c2 in zip(x, y))

key = xor(cookie[-len(source):], source)
payload = cookie[:-len(source)] + xor(key, target)[:-14]

response = requests.get('http://52.69.244.164:51913/', cookies={'auth': urllib2.quote(payload)})
print response.content
```

**hitcon{WoW_CFB_m0dE_5o_eAsY}**

[ENG](#eng-version)

We can do a HTTP `GET` and `POST` to the provided service. `POST` encrypts a JSON of provided "username" and "password" with a 128-bit AES in CFB mode. `GET` decrypts it and if the JSON has a `'admin': true` field it gives us the flag. Key for the AES is constant and private while IV is randomly generated and prepended to the ciphertext.

CFB mode produces ciphertext in blocks by xoring the encrypted key with a plaintext. It also uses part of the current block to encrypt the next. So that means that we can't change two succesive blocks without throwing off the decryption into outputting garbage.

The way this particular JSON is constructed makes it rather impossible to change only the last block - we can't add a new field by modifying the last 16 characters of `{ ... "password":"provided_password","db":"hitcon-ctf"}`. We can however, edit the one before last and discard the last block of ciphertext by simple truncating. We could also play with the first one and the IV, but we chose the former method.

Here's the solver:

```python
import requests
import urllib2

response = requests.post('http://52.69.244.164:51913/', data={'username': 'aaa', 'password': 'bbbbbbbbbbbbbbbbbbbbbbbbbbbb'}, allow_redirects=False)
cookie = urllib2.unquote(response.cookies['auth'])

source = 'bbbbbbbbbbbb","db":"hitcon-ctf"}'
target = 'bbb","admin":true}              '

def xor(x, y):
    return ''.join(chr(ord(c1) ^ ord(c2)) for c1, c2 in zip(x, y))

key = xor(cookie[-len(source):], source)
payload = cookie[:-len(source)] + xor(key, target)[:-14]

response = requests.get('http://52.69.244.164:51913/', cookies={'auth': urllib2.quote(payload)})
print response.content
```

**hitcon{WoW_CFB_m0dE_5o_eAsY}**
