# The worst RSA joke (Crypto)

In the task we get [public key](public.pem) and [ciphertext](flag.enc).
The description of the task states that someone decided to use a single prime as modulus for RSA encryption.

The difficulty of breaking RSA is based on the fact that the number of co-prime numbers to the modulus (so-called Euler's totient function) is secret.
For a prime number this value is known and is simply `p-1`.
For product of two co-prime numbers it is `(p-1)*(q-1)`, and here is the strength of RSA - in order to calculate this value we need to know prime factors of the modulus, and finding those is hard.

In our case this whole problem doesn't exist, since we know `p` and therefore we know `p-1` as well.
Therefore we can simply calculate the private key exponent as `modinv(e,p-1)` and decrypt the ciphertext.

```python
import codecs

from Crypto.PublicKey import RSA

from crypto_commons.generic import bytes_to_long
from crypto_commons.rsa.rsa_commons import modinv, rsa_printable


def main():
    with codecs.open("public.pem", "r") as input_file:
        pub = input_file.read()
        pub = RSA.importKey(pub)
        print(pub.e, pub.n)
        with codecs.open("flag.enc", 'r') as input_flag:
            data = input_flag.read().decode("base64")
            d = modinv(pub.e, pub.n-1)
            print(rsa_printable(bytes_to_long(data), d, pub.n))


main()
```

And we get `Flag{S1nGL3_PR1m3_M0duLUs_ATT4cK_TaK3d_D0wn_RSA_T0_A_Sym3tr1c_ALg0r1thm}`
