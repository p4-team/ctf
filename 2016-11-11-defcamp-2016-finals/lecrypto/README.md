# LeCrypto (crypto 250)

###ENG
[PL](#pl-version)

In the task we get the code:

```python
#!/usr/bin/env python
from random import SystemRandom
import hashlib
import copy_reg, types


class RC4:
    def __init__(self, message, password):
        self.state = [None] * 256
        self.p = None
        self.q = None

        self.message = message
        self.password = [ord(c) for c in password]
        self.setKey()

    def setKey(self):
        key = self.password
        self.state = [n for n in range(256)]
        self.p = self.q = j = 0
        for i in range(256):
            if len(key) > 0:
                j = (j + self.state[i] + key[i % len(key)]) % 256
            else:
                j = (j + self.state[i]) % 256
            self.state[i], self.state[j] = self.state[j], self.state[i]

    def byteGenerator(self):
        self.p = (self.p + 1) % 256
        self.q = (self.q + self.state[self.p]) % 256
        self.state[self.p], self.state[self.q] = self.state[self.q], self.state[self.p]
        return self.state[(self.state[self.p] + self.state[self.q]) % 256]

    def encrypt(self):
        return [ord(p) ^ self.byteGenerator() for p in self.message]

    def decrypt(self):
        return "".join([chr(c ^ self.byteGenerator()) for c in self.message])


def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)


copy_reg.pickle(types.MethodType, _pickle_method)


def getRC4From(password, s="", debug=True):
    if (len(s) == 0):
        cg = SystemRandom()
        s = "".join([unichr(cg.randrange(32, 126)) for i in range(16)])

    h0 = hashlib.md5(password.encode('utf-8')).hexdigest()
    md5t = "".join([unichr(ord(c)) for c in h0[:10]])  #
    ib = 16 * (md5t + s)
    h1 = hashlib.md5(ib.encode('utf-8')).hexdigest()
    h1th = h1[:8] + "00" * 4
    print("h1th ", h1th)
    hf = hashlib.md5(h1th.encode('utf-8')).hexdigest()
    return [s, hf]


def encrypt(text, password):
    crypter = RC4(text, password)
    enc = crypter.encrypt()
    enc = "".join([unichr(c) for c in enc])
    return enc


def leCrypt(text, password, debug=False):
    theH = {'s': '', 'v': '', 'vH': ''}

    cg = SystemRandom()
    v = "".join([unichr(cg.randrange(32, 126)) for i in range(16)])  # 16 bytes
    v = v.encode("utf-8")
    print('v ', v)

    (s, key) = getRC4From(password, debug=True)
    theH['s'] = s
    theH['v'] = encrypt(v, key)
    theH['vH'] = encrypt(hashlib.md5(v).digest(), key)
    theH['enc'] = encrypt(text, key)
    if debug:
        print theH
    return theH
```

And data:

```
{"vH": "\u008c\u00d4\u0000\u00e0\u0005\u00b4\u0096\u00c4\u00ad\u00a9c\u00c3\u00ec/\u00e0t", 
"s": "*mqZ(dpJMvM)a2y3", 
"enc": "5\u00e0q\u00df\u00fb\u0017\u00ee\u001e\u00f85\u0016\u00efN\u0095\f\u00e2P\u0013\u00e5\u007f\u00a5r\u00a8\u00d5\u00ff\u00fc\u00c2\u00cb\u00a2K\u000b|\t\u009e{\u00b9c\r", 
"v": "]\u0084r\u00d5\u00f7K\u008a4\u00862\u001a\u00a6I\u009d\u0018\u00ba"}
```

RC4 here is implemented fine, no vulnerabilities there.
The problem with encryption is in:

```python
    h1th = h1[:8] + "00" * 4
    print("h1th ", h1th)
    hf = hashlib.md5(h1th.encode('utf-8')).hexdigest()
    return [s, hf]
```

The `hf` value returned here is later used as RC4 encryption key for all parameters so this is the value we eventually want to recover.
There is no point trying to reverse the algorithm since there is md5 everywhere.
But we can see that the final key is md from `h1th = h1[:8] + "00" * 4` which means first 8 bytes of some md5 value (so basically just 4 bytes) concatenated with 4 times `00`.
This means we could brute-force those 4 bytes, calculate the resulting key and the test if the decoding output if correct.

As correctness check we decided to use `v` because we know the charset for all 16 bytes there - `cg.randrange(32, 126)`.
So if we decode the `v` and all characters are in the right range we can assume the key to be a possible match:

```python
def decrypt(data, password):
    crypter = RC4(data, password)
    enc = crypter.decrypt()
    return enc


def in_charset(decrypted_v):
    for c in decrypted_v:
        if not 32 <= ord(c) <= 126:
            return False
    return True


def worker(data):
    a, crypted_v = data
    ac = chr(a)
    results = []
    for b in range(256):
        bc = chr(b)
        for c in range(256):
            cc = chr(c)
            for d in range(256):
                h1th = (ac + bc + cc + chr(d)).encode("hex") + "00" * 4
                hf = hashlib.md5(h1th.encode('utf-8')).hexdigest()
                decrypted_v = decrypt(crypted_v, hf)
                if in_charset(decrypted_v):
                    results.append(hf)
    return results


def crack():
    with codecs.open("challenge.txt", "r")as input_file:
        data = input_file.read()
        m = eval(data)
        crypted_v = [ord(c) for c in m['v'].decode("unicode_escape")]
        print(len(crypted_v))
        start = 0
        stop = 256
        data = [(a, crypted_v) for a in range(start, stop)]
        result = brute(worker, data)
        print(result)
        with codecs.open("output.txt", "a")as output_file:
            output_file.write(str(result))


if __name__ == '__main__':
    freeze_support()
    crack()
```

We run this in paralell and recover all candidate keys.
Then we simply run:

```python
def main():
    flag = "5\u00e0q\u00df\u00fb\u0017\u00ee\u001e\u00f85\u0016\u00efN\u0095\f\u00e2P\u0013\u00e5\u007f\u00a5r\u00a8\u00d5\u00ff\u00fc\u00c2\u00cb\u00a2K\u000b|\t\u009e{\u00b9c\r".decode(
        "unicode_escape")
    crypted = [ord(c) for c in flag]
    partial = [[]]  # data from workers
    for worker_result in partial:
        for potential_key in worker_result:
            print(decrypt(crypted, potential_key) + "\n\n\n\n\n\n")


main()
```

And recover the flag for one of the candidate keys.

###PL version

W zadaniu dostajemy kod:

```python
#!/usr/bin/env python
from random import SystemRandom
import hashlib
import copy_reg, types


class RC4:
    def __init__(self, message, password):
        self.state = [None] * 256
        self.p = None
        self.q = None

        self.message = message
        self.password = [ord(c) for c in password]
        self.setKey()

    def setKey(self):
        key = self.password
        self.state = [n for n in range(256)]
        self.p = self.q = j = 0
        for i in range(256):
            if len(key) > 0:
                j = (j + self.state[i] + key[i % len(key)]) % 256
            else:
                j = (j + self.state[i]) % 256
            self.state[i], self.state[j] = self.state[j], self.state[i]

    def byteGenerator(self):
        self.p = (self.p + 1) % 256
        self.q = (self.q + self.state[self.p]) % 256
        self.state[self.p], self.state[self.q] = self.state[self.q], self.state[self.p]
        return self.state[(self.state[self.p] + self.state[self.q]) % 256]

    def encrypt(self):
        return [ord(p) ^ self.byteGenerator() for p in self.message]

    def decrypt(self):
        return "".join([chr(c ^ self.byteGenerator()) for c in self.message])


def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)


copy_reg.pickle(types.MethodType, _pickle_method)


def getRC4From(password, s="", debug=True):
    if (len(s) == 0):
        cg = SystemRandom()
        s = "".join([unichr(cg.randrange(32, 126)) for i in range(16)])

    h0 = hashlib.md5(password.encode('utf-8')).hexdigest()
    md5t = "".join([unichr(ord(c)) for c in h0[:10]])  #
    ib = 16 * (md5t + s)
    h1 = hashlib.md5(ib.encode('utf-8')).hexdigest()
    h1th = h1[:8] + "00" * 4
    print("h1th ", h1th)
    hf = hashlib.md5(h1th.encode('utf-8')).hexdigest()
    return [s, hf]


def encrypt(text, password):
    crypter = RC4(text, password)
    enc = crypter.encrypt()
    enc = "".join([unichr(c) for c in enc])
    return enc


def leCrypt(text, password, debug=False):
    theH = {'s': '', 'v': '', 'vH': ''}

    cg = SystemRandom()
    v = "".join([unichr(cg.randrange(32, 126)) for i in range(16)])  # 16 bytes
    v = v.encode("utf-8")
    print('v ', v)

    (s, key) = getRC4From(password, debug=True)
    theH['s'] = s
    theH['v'] = encrypt(v, key)
    theH['vH'] = encrypt(hashlib.md5(v).digest(), key)
    theH['enc'] = encrypt(text, key)
    if debug:
        print theH
    return theH
```

I dane:

```
{"vH": "\u008c\u00d4\u0000\u00e0\u0005\u00b4\u0096\u00c4\u00ad\u00a9c\u00c3\u00ec/\u00e0t", 
"s": "*mqZ(dpJMvM)a2y3", 
"enc": "5\u00e0q\u00df\u00fb\u0017\u00ee\u001e\u00f85\u0016\u00efN\u0095\f\u00e2P\u0013\u00e5\u007f\u00a5r\u00a8\u00d5\u00ff\u00fc\u00c2\u00cb\u00a2K\u000b|\t\u009e{\u00b9c\r", 
"v": "]\u0084r\u00d5\u00f7K\u008a4\u00862\u001a\u00a6I\u009d\u0018\u00ba"}
```

Szyfrowanie RC4 jest tu zaimplementowane bezbłędnie, nie ma tam podatności.
Problem z szyfrowaniem jest tutaj:

```python
    h1th = h1[:8] + "00" * 4
    print("h1th ", h1th)
    hf = hashlib.md5(h1th.encode('utf-8')).hexdigest()
    return [s, hf]
```

Wartość `hf` zwrócona tutaj jest użyta później jako klucz szyfrowania RC4 dla wszystkich znanych wartości, wiec finalnie chcemy odzyskać ten klucz.
Nie ma sensu "odwracanie" tego algorytmu, ponieważ wszędzie mamy nieodwracalne md5.
Ale możemy zauważyć że finalny klucz to md5 z `h1th = h1[:8] + "00" * 4` czyli z pierwszych 8 bajtów jakiegoś md5 (czyli de facto tylko 4 bajtów) sklejonych z 4 `00`.
To oznacza że możemy brutować te 4 bajty, obliczyć wynikowy klucz za pomocą md5 a potem sprawdzić czy można nim coś odszyfrować.

Do sprawdzenia poprawności klucza wybraliśmy zmienną `v` bo znamy charset dla wszystkich 16 bajtów - `cg.randrange(32, 126)`.
Więc jeśli dekodując `v` dostaniemy wszystkie znaki w zadanym zasięgu możemy uznać że mamy potencjalny klucz:


```python
def decrypt(data, password):
    crypter = RC4(data, password)
    enc = crypter.decrypt()
    return enc


def in_charset(decrypted_v):
    for c in decrypted_v:
        if not 32 <= ord(c) <= 126:
            return False
    return True


def worker(data):
    a, crypted_v = data
    ac = chr(a)
    results = []
    for b in range(256):
        bc = chr(b)
        for c in range(256):
            cc = chr(c)
            for d in range(256):
                h1th = (ac + bc + cc + chr(d)).encode("hex") + "00" * 4
                hf = hashlib.md5(h1th.encode('utf-8')).hexdigest()
                decrypted_v = decrypt(crypted_v, hf)
                if in_charset(decrypted_v):
                    results.append(hf)
    return results


def crack():
    with codecs.open("challenge.txt", "r")as input_file:
        data = input_file.read()
        m = eval(data)
        crypted_v = [ord(c) for c in m['v'].decode("unicode_escape")]
        print(len(crypted_v))
        start = 0
        stop = 256
        data = [(a, crypted_v) for a in range(start, stop)]
        result = brute(worker, data)
        print(result)
        with codecs.open("output.txt", "a")as output_file:
            output_file.write(str(result))


if __name__ == '__main__':
    freeze_support()
    crack()
```

Uruchamiamy to współbieżnie i odzyskujemy wszystkie klucze kandydujące.
Następnie uruchamiamy:

```python
def main():
    flag = "5\u00e0q\u00df\u00fb\u0017\u00ee\u001e\u00f85\u0016\u00efN\u0095\f\u00e2P\u0013\u00e5\u007f\u00a5r\u00a8\u00d5\u00ff\u00fc\u00c2\u00cb\u00a2K\u000b|\t\u009e{\u00b9c\r".decode(
        "unicode_escape")
    crypted = [ord(c) for c in flag]
    partial = [[]]  # data from workers
    for worker_result in partial:
        for potential_key in worker_result:
            print(decrypt(crypted, potential_key) + "\n\n\n\n\n\n")


main()
```

I odczytujemy flagę dla jednego z kluczy kandydujących.
