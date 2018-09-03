# Revolutional Secure Angou (crypto, 154p, 82 solved)

In the challenge we get [encrypted flag](flag.encrypted), [public key](publickey.pem) and [challenge source code](generator.rb):

```ruby
require 'openssl'

e = 65537
while true
  p = OpenSSL::BN.generate_prime(1024, false)
  q = OpenSSL::BN.new(e).mod_inverse(p)
  next unless q.prime?
  key = OpenSSL::PKey::RSA.new
  key.set_key(p.to_i * q.to_i, e, nil)
  File.write('publickey.pem', key.to_pem)
  File.binwrite('flag.encrypted', key.public_encrypt(File.binread('flag')))
  break
end
```

The flag is encrypted with classic RSA here and the only strange part is the way primes `p` and `q` are generated.

We know that: 

`q = modinv(e, p)`

Which we can rephrase to:

`q*e = 1 mod p`

This means that there exist such `k` for which:

`q*e = 1 + k*p`

If we now multiply this by `p` we get

`q*p*e = p + k*p^2`

And since `q*p = n` we get:

`n*e = p + k*p^2`

We could divide this by `k` and calculate a square root to get:

`sqrt(n*e/k) = sqrt(p/k + p^2)`

And if we extract `p^2` as a factor on the right side we get:

`sqrt(n*e/k) = sqrt(p^2(1/p*k + 1))`

It's obvious that `1/p*k` will be close to `0` and this `(1/p*k + 1)` is going to be very close to `1` and thus:

`sqrt(n*e/k) = p * sqrt(1/p*k + 1) = p`

This means we can calculate `p` directly if we only know `k`.
We can verify this with a simple sanity check:

```python
def sanity():
    p = gmpy2.next_prime(2 ** 256)
    while True:
        p = gmpy2.next_prime(p)
        e = 65537
        q = modinv(e, p)
        if gmpy2.is_prime(q):
            break
    n = p * q
    print(p)
    print(q)
    print(n)
    k = (q * e - 1) / p
    p_result = gmpy2.isqrt(n * e / k)
    print(k, 'p', p_result)
    assert p == p_result
```

We don't know the exact value of `k`, but we know that `q` is smaller than `p` (since it's calculated `mod p`), and therefore since `q*e = 1+k*p` then `k < e`.
This means we can easily brute-force `k` value because there are only 65537 values to check.

```python
import codecs
import gmpy2

from Crypto.PublicKey import RSA

from crypto_commons.rsa.rsa_commons import modinv, rsa_printable


def main():
    with codecs.open("flag.encrypted", 'rb') as flag_file:
        ct = flag_file.read()
    with codecs.open("publickey.pem", 'r') as key_file:
        key = RSA.importKey(key_file.read())
        print(key.e, key.n)
    print(key.n * key.e)
    for k in range(1, 65537):
        p = gmpy2.isqrt(key.n * key.e / k)
        if gmpy2.is_prime(p):
            q = key.n / p
            fi = (p - 1) * (q - 1)
            d = modinv(key.e, fi)
            pt = rsa_printable(ct, d, key.n)
            if "TWCTF" in pt:
                print(k, pt)
                break
```

And after a moment we get: `TWCTF{9c10a83c122a9adfe6586f498655016d3267f195}` for `k = 54080`
