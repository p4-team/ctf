# Daring (misc, 100+50p, 30 solved)

In the challenge we get a set of files:

- AES-CTR encrypted [data](aes.enc)
- RSA public [key](pubkey.txt)
- RSA encrypted [data](rsa.enc)
- Challenge [source code](vuln.py)

The code is quite simple:

```python
#!/usr/bin/env python3
import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util import Counter
from Crypto.PublicKey import RSA

flag = open('flag.txt', 'rb').read().strip()

key = RSA.generate(1024, e=3)
open('pubkey.txt', 'w').write(key.publickey().exportKey('PEM').decode() + '\n')
open('rsa.enc', 'wb').write(pow(int.from_bytes(flag.ljust(128, b'\0'), 'big'), key.e, key.n).to_bytes(128, 'big'))

key = SHA256.new(key.exportKey('DER')).digest()
open('aes.enc', 'wb').write(AES.new(key, AES.MODE_CTR, counter=Counter.new(128)).encrypt(flag))
```

First thing we notice is that strangely the flag is encrypted both by RSA and by AES-CTR, but pretty much using related key.
If we could decrypt one, we could decrypt the other one as well.

Once we load the RSA public key we can notice that `e` is very small - `3`.
This leads us to check what kind of padding scheme is used here, and bingo, there is `\x00` right padding:

```python
flag.ljust(128, b'\0')
```

The value seems to be padded before RSA encryption, so there is no risk for degenerated RSA case when `flag^3 < n`, which would mean we can just calculate cube root of the ciphertext.
But since the padding is just zeroes, we can actually use RSA homomorphic property to remove this padding from the ciphertext.

This comes from the fact that RSA encryption is just `msg^e mod n` and if we multiply this by `x^e mod n` the result is `(mgs*x)^e mod n`.
So if we decrypt this we would get back `msg*x mod n`.

Adding zero padding here can be viewed simply as bit-shifting left, so just simple multiplication.
Each `0` byte added to the plaintext as padding is just multiplying plaintext by 256.
So in order to remove those, we need to divide by 256, which is the same as multiply by `modinv(256,n)`.

Now, how many padded bytes are there?
This is where the AES-CTR ciphertext comes into play.
AES-CTR is a stream cipher, so the length of ciphertext is the same as length of plaintext.
We can just load the aes ciphertext and check for the length.
It's `43` bytes long, so there are 85 bytes of padding we can remove:

```python
new_ct = ct * pow(modinv(256, n) ** padding_len, e, n)
new_ct %= n
```

Now if we check this with some example, we will see that the plaintext is still 1 byte too long.
This means that still `flag^3 > n` so the ciphertext we have was cut by `mod n` operation.
But we know that it can't have overflown too much, so we can just brute-force it.

We pretty know that `flag^3 = ct + k*n`, for some small `k`.
We can loop over some values for `k` and see when `ct + k*n` is a cube:

```python
for i in range(256):
    potential_pt, is_cube = gmpy2.iroot(new_ct + (n * i), e)
    if is_cube:
        print(i, long_to_bytes(potential_pt))
```

When we run this we get `hxp{DARINGPADS_1s_4n_4n4gr4m_0f_RSAPADDING}`

Whole solver [here](daring.py)
