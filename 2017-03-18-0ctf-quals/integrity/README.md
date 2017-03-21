# Integrity (crypto)

##ENG
[PL](#pl-version)

In the task we get a service:

```python
#!/usr/bin/python -u

from Crypto.Cipher import AES
from hashlib import md5
from Crypto import Random
from signal import alarm

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[0:-ord(s[-1])]


class Scheme:
    def __init__(self,key):
        self.key = key

    def encrypt(self,raw):
        raw = pad(raw)
        raw = md5(raw).digest() + raw

        iv = Random.new().read(BS)
        cipher = AES.new(self.key,AES.MODE_CBC,iv)

        return ( iv + cipher.encrypt(raw) ).encode("hex")

    def decrypt(self,enc):
        enc = enc.decode("hex")

        iv = enc[:BS]
        enc = enc[BS:]

        cipher = AES.new(self.key,AES.MODE_CBC,iv)
        blob = cipher.decrypt(enc)

        checksum = blob[:BS]
        data = blob[BS:]

        if md5(data).digest() == checksum:
            return unpad(data)
        else:
            return

key = Random.new().read(BS)
scheme = Scheme(key)

flag = open("flag",'r').readline()
alarm(30)

print "Welcome to 0CTF encryption service!"
while True:
    print "Please [r]egister or [l]ogin"
    cmd = raw_input()

    if not cmd:
        break

    if cmd[0]=='r' :
        name = raw_input().strip()

        if(len(name) > 32):
            print "username too long!"
            break
        if pad(name) == pad("admin"):
            print "You cannot use this name!"
            break
        else:
            print "Here is your secret:"
            print scheme.encrypt(name)


    elif cmd[0]=='l':
        data = raw_input().strip()
        name = scheme.decrypt(data)

        if name == "admin":
            print "Welcome admin!"
            print flag
        else:
            print "Welcome %s!" % name
    else:
        print "Unknown cmd!"
        break
```

As can be seen we can either login or register.
Loggin in as admin will give us the flag, so this is the ultimate goal.
We can see that we can't register as `admin` because this is explicitly checked.

Once we register we get as a result login token in the form `IV | AES_CBC(md5(login) | login)`.

Since we can modify freely the IV, we can force the decoding of md5 checksum to any value we want.
This is because in CBC block crypto the first decrypted block is `IV xor AES_decrypt(ciphertext[0])` and we know the value of `AES_decrypt(ciphertext[0])` because it is md5 of the login we provided.
So in order to force k-th decoded byte to value `X` we simply need to modify k-th byte of IV to `IV[k] ^ md5(login)[k] ^ X`.

As a result we can easily fool the md5 checksum and we can provide IV such that the decoded md5 checksum will be a checksum of `pad("admin")`.

Now we need somehow to obtain ciphertext which will decode to `pad("admin")`.
This is again quite simple, since we're dealing with block crypto and the login token does not contain any information about the length of the provided input (unlike in real HMAC).
It means that we can remove some ciphertext blocks from the end and the decryption will still work just fine, assuming the padding is correct.

So if we decide to encrypt login in a form of `pad("admin")+16_random_bytes`, the server will send us ciphertext of `pad(pad("admin")+16_random_bytes)`.
And of course this translates to 3 ciphertext blocks in a form of `pad("admin")+16_random_bytes+PKCS_padding`.
But as said before, we can simply remove the last 2 blocks of ask server to use only the first one, which decodes to `pad("admin")`!

```python
import hashlib
from crypto_commons.netcat.netcat_commons import nc, send, receive_until_match

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)


def generate_payload(ct):
    stripped_ct = ct[:-64]  # skip last 2 blocks, the PKCS padding and the dummy block
    target_md5 = hashlib.md5(pad("admin")).digest()  # md5 we want to get from decryption
    source_md5 = hashlib.md5(pad(pad("admin") + ("a" * 16))).digest()  # md5 the server calculated
    original_iv = stripped_ct[:32].decode("hex")
    new_iv = []
    for i in range(len(original_iv)):
        new_iv.append(chr(ord(original_iv[i]) ^ ord(source_md5[i]) ^ ord(target_md5[i])))
    iv = "".join(new_iv).encode("hex")
    payload = iv + stripped_ct[32:]
    return payload


def main():
    s = nc("202.120.7.217", 8221)
    print(receive_until_match(s, ".*ogin"))
    send(s, "r")
    send(s, pad("admin") + ("a" * 16))
    print(receive_until_match(s, ".*secret:"))
    ct = s.recv(9999).split("\n")[1]
    send(s, "l")
    send(s, generate_payload(ct))
    print(s.recv(9999))
    print(s.recv(9999))
    print(s.recv(9999))


main()
```

And this gives us `flag{Easy_br0ken_scheme_cann0t_keep_y0ur_integrity}`

##PL version

W zadaniu dostajemy dostęp do serwisu:

```python
#!/usr/bin/python -u

from Crypto.Cipher import AES
from hashlib import md5
from Crypto import Random
from signal import alarm

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[0:-ord(s[-1])]


class Scheme:
    def __init__(self,key):
        self.key = key

    def encrypt(self,raw):
        raw = pad(raw)
        raw = md5(raw).digest() + raw

        iv = Random.new().read(BS)
        cipher = AES.new(self.key,AES.MODE_CBC,iv)

        return ( iv + cipher.encrypt(raw) ).encode("hex")

    def decrypt(self,enc):
        enc = enc.decode("hex")

        iv = enc[:BS]
        enc = enc[BS:]

        cipher = AES.new(self.key,AES.MODE_CBC,iv)
        blob = cipher.decrypt(enc)

        checksum = blob[:BS]
        data = blob[BS:]

        if md5(data).digest() == checksum:
            return unpad(data)
        else:
            return

key = Random.new().read(BS)
scheme = Scheme(key)

flag = open("flag",'r').readline()
alarm(30)

print "Welcome to 0CTF encryption service!"
while True:
    print "Please [r]egister or [l]ogin"
    cmd = raw_input()

    if not cmd:
        break

    if cmd[0]=='r' :
        name = raw_input().strip()

        if(len(name) > 32):
            print "username too long!"
            break
        if pad(name) == pad("admin"):
            print "You cannot use this name!"
            break
        else:
            print "Here is your secret:"
            print scheme.encrypt(name)


    elif cmd[0]=='l':
        data = raw_input().strip()
        name = scheme.decrypt(data)

        if name == "admin":
            print "Welcome admin!"
            print flag
        else:
            print "Welcome %s!" % name
    else:
        print "Unknown cmd!"
        break
```

Jak łatwo zauważyć możemy się zalogować lub zarejetrować.
Logowanie jako admin pozwoli uzyskać flagę i to jest naszym finalnym celem.
Możemy zauważyć, że nie możemy zarejestrować się jako `admin` ponieważ jest to wyraźnie sprawdzane.

Po rejestracji dostajemy token logowania w postaci `IV | AES_CBC(md5(login) | login)`.

Ponieważ możemy dowolnie zmieniać IV, możemy wymusić dowolne dekodowanie wartości md5.
Wynika to bezpośrednio z tego jak działa szyfr blokowy w trybie CBC - pierwszy dekodowany blok to `IV xor AES_decrypt(ciphertext[0])` a znamy wartość `AES_decrypt(ciphertext[0])`bo to md5 wyliczone z wprowadzonych przez nas danych.
Więc żeby wymusić dekodowanie k-tego bajtu do wartości `X` musimy jedynie zmienić k-ty bajt IV na `IV[k] ^ md5(login)[k] ^ X`

W efekcie możemy w prosty sposób oszukać checksume md5 i podać takie IV, że odkodowane md5 będzie zgodne z checksumą dla `pad("admin")`.

Teraz potrzebujemy uzyskać ciphertext który zdekoduje się do `pad("admin")`.
To znów jest dość proste, ponieważ mamy do czynienia z szyfrem blokowym a token logowania nie zawiera nigdzie informacji o długości wprowadzonych danych (w przeciwieństwie do prawdziwego HMAC).
To oznacza, że możemy usunąć kilka bloków ciphertextu z końca a deszyfrowanie nadal przebiegnie pomyślnie, o ile padding się zgadza.

Jeśli więc zdecydujemy się zaszyfrować login w postaci `pad("admin")+16_random_bytes` serwer odeśle nam ciphertext dla `pad(pad("admin")+16_random_bytes)`
A to oczywiście oznacza że dostaniemy 3 bloki ciphertextu w postaci `pad("admin")+16_random_bytes+PKCS_padding`.
Jak wspomnieliśmy wcześniej, możemy teraz usunąć 2 ostatnie bloki i poprosić serwer o deszyfrowanie tylko pierwszego, który dekoduje się do `pad("admin")`!

```python
import hashlib
from crypto_commons.netcat.netcat_commons import nc, send, receive_until_match

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)


def generate_payload(ct):
    stripped_ct = ct[:-64]  # skip last 2 blocks, the PKCS padding and the dummy block
    target_md5 = hashlib.md5(pad("admin")).digest()  # md5 we want to get from decryption
    source_md5 = hashlib.md5(pad(pad("admin") + ("a" * 16))).digest()  # md5 the server calculated
    original_iv = stripped_ct[:32].decode("hex")
    new_iv = []
    for i in range(len(original_iv)):
        new_iv.append(chr(ord(original_iv[i]) ^ ord(source_md5[i]) ^ ord(target_md5[i])))
    iv = "".join(new_iv).encode("hex")
    payload = iv + stripped_ct[32:]
    return payload


def main():
    s = nc("202.120.7.217", 8221)
    print(receive_until_match(s, ".*ogin"))
    send(s, "r")
    send(s, pad("admin") + ("a" * 16))
    print(receive_until_match(s, ".*secret:"))
    ct = s.recv(9999).split("\n")[1]
    send(s, "l")
    send(s, generate_payload(ct))
    print(s.recv(9999))
    print(s.recv(9999))
    print(s.recv(9999))


main()
```

A to daje nam `flag{Easy_br0ken_scheme_cann0t_keep_y0ur_integrity}`
