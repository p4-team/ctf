##RSA (Crypto, 500p)

	Now you are one step away from knowing who is that WARRIOR. 
	The Fighter who will decide the fate of war between the 2 countries. 
	The Pride of One and Envey of the Other... 
	You have got the secrete file which has the crucial information to identify the fighter. 
	But the file is encrypted with a RSA-Private key. 
	Good news you have its corresponding public key in a file. 
	Bad news there are 49 other keys. 
	Whos is the Fighter.

###PL
[ENG](#eng-version)

Dostajemy szyfrowany [plik](warrior.txt) oraz zbiór [kluczy publicznych](all_keys.txt).
Plik został zaszyfrowany przy pomocy klucza prywatnego RSA (dość dziwny pomysł, ale matematycznie zupełnie poprawny) a jeden z kluczy publicznych którymi dysponujemy pasuje do tego klucza prywatnego.

W przypadku RSA parametry kluczy są dobrane tak, aby:

`d*e = 1 mod (totient(n))`

ponieważ dzięki temu

`(x^e)^d mod n = x^ed mod n = m`

Jak nie trudno zauważyć, nie ma więc znaczenia czy jak w klasycznym przypadku mamy:

`ciphertext = plaintext^e mod n` 

i dekodujemy go przez podniesienie do potęgi `d` czy też mamy:

`ciphertext = plaintext^d mod n` 

i dekoduejmy go przez podniesienie do potęgi `e`.

Uruchamiamy więc prosty skrypt który spróbuje zdekodować plik przy pomocy każdego z kluczy:

```python
import codecs
from Crypto.PublicKey import RSA
from base64 import b64decode
from Crypto.Util.number import long_to_bytes, bytes_to_long

with codecs.open("warrior.txt", "rb") as warrior:
    w = warrior.read()
    ciphertext = bytes_to_long(w)
    print(len(w))
    with codecs.open("all_keys.txt") as input_file:
        data = input_file.read()
        for i, key in enumerate(data.split("-----END PUBLIC KEY-----")):
            key = key.replace("\n", "")
            key = key.replace("-----BEGIN PUBLIC KEY-----", "")
            if key:
                keyDER = b64decode(key)
                keyPub = RSA.importKey(keyDER)
                print(i)
                pt = pow(ciphertext, keyPub.key.e, keyPub.key.n)
                print("plaitnext: " + long_to_bytes(pt))

```

Jeden z wyników zawiera:

	This fighter is a designation for two separate, heavily upgraded derivatives of the Su-35 'Flanker' jet plane. 
	They are single-seaters designed by Sukhoi(KnAAPO).

Sprawdzamy więc skąd pochodzi cytat i trafiamy na https://en.wikipedia.org/wiki/Sukhoi_Su-35 a flagą jest `Sukhoi Su-35`
	
###ENG version

We get a encrypted [file](warrior.txt) and set of [public keys](all_keys.txt)
The file was encrypted with RSA private key (unusual, but mathematically correct) and one of the public keys we have is corresponding key to the private key used in encryption.

In case of RSA cipher the key parameters are selected so that:


`d*e = 1 mod (totient(n))`

and therefore:

`(x^e)^d mod n = x^ed mod n = m`

As can be noticed, it doesn't matter if we have the classic example:

`ciphertext = plaintext^e mod n` 

and we decode it with raising to power `d`, or if we have:

`ciphertext = plaintext^d mod n` 

and decode by raising to power `e`.

So we run a simple script which will decode the file using each of the keys:

```python
import codecs
from Crypto.PublicKey import RSA
from base64 import b64decode
from Crypto.Util.number import long_to_bytes, bytes_to_long

with codecs.open("warrior.txt", "rb") as warrior:
    w = warrior.read()
    ciphertext = bytes_to_long(w)
    print(len(w))
    with codecs.open("all_keys.txt") as input_file:
        data = input_file.read()
        for i, key in enumerate(data.split("-----END PUBLIC KEY-----")):
            key = key.replace("\n", "")
            key = key.replace("-----BEGIN PUBLIC KEY-----", "")
            if key:
                keyDER = b64decode(key)
                keyPub = RSA.importKey(keyDER)
                print(i)
                pt = pow(ciphertext, keyPub.key.e, keyPub.key.n)
                print("plaitnext: " + long_to_bytes(pt))

```

One of the results contains:

	This fighter is a designation for two separate, heavily upgraded derivatives of the Su-35 'Flanker' jet plane. 
	They are single-seaters designed by Sukhoi(KnAAPO).

We check where did this come from and we find https://en.wikipedia.org/wiki/Sukhoi_Su-35 and the flag is `Sukhoi Su-35`