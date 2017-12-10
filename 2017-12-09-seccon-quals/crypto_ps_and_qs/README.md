# Ps and Qs (Crypto, 200p)

In the task we get a [ciphertext](cipher) and two RSA public keys: [pub1](pub1.pub), [pub2](pub2.pub).

As usual in case when there are more than one RSA public key, it's worth to check if maybe they don't share a prime:

```python
import codecs
from Crypto.PublicKey import RSA
from crypto_commons.rsa.rsa_commons import gcd

def read_key(filename):
    with codecs.open(filename, "r") as input_file:
        data = input_file.read()
        pub = RSA.importKey(data)
        print(pub.e, pub.n)
    return pub


def main():
    pub1 = read_key("pub1.pub")
    pub2 = read_key("pub2.pub")
    p = gcd(pub1.n, pub2.n)
    print(p)
```

And yes, in this case they do share a prime, so we can easily factor both keys.
Now we simply need to recover private keys for both keys by calculating `modinv(e, (p-1)*(q-1))` and trying to use them to decrypt the flag:

```python
import codecs
from Crypto.Util.number import long_to_bytes
from crypto_commons.generic import bytes_to_long
from crypto_commons.rsa.rsa_commons import gcd, get_fi_distinct_primes, modinv

def read_ct():
    with codecs.open("cipher", "rb") as input_file:
        data = input_file.read()
        print(len(data))
        msg = bytes_to_long(data)
    return msg


p = gcd(pub1.n, pub2.n)
print(p)
q1 = pub1.n / p
q2 = pub2.n / p
print(p, q1)
print(p, q2)
msg = read_ct()

d1 = modinv(pub1.e, get_fi_distinct_primes([p, q1]))
d2 = modinv(pub2.e, get_fi_distinct_primes([p, q2]))

first = pow(msg, d1, pub1.n)
print(long_to_bytes(first))
```

Already the first key gives us the flag: `SECCON{1234567890ABCDEF}`

Complete solver [here](solver.py)
