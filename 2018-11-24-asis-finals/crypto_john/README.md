# John-Bull (crypto, 141p, 29 solved)

In the challenge we get [code and encryption results](John_Bull.txt).
The encryption code is quite simple:

```python
def make_key(k):
    while True:
        r = getRandomInteger(k) << 2
        p, q = r**2+r+1, r**2+3*r+1
        if gmpy.is_prime(p) * gmpy.is_prime(q):
            break
    pubkey = r**6 + 5*r**5 + 10*r**4 + 13*r**3 + 10*r**2 + 5*r + 1
    return pubkey

def encrypt(m, pubkey):
    return pow(bytes_to_long(m), pubkey, pubkey)
```

The encryption looks like RSA with `e` set to `n`, and `n` itself is `(p**2)*q`.
The first step is to recover `r` and thus factor `n`.
We can see that `n` is a polynomial, and a nice property here is that for large `r` the higher order terms will be significantly bigger than lower order terms.

Imagine `r=1000000`, in such case `r**6-r**5 ~= 0.999999*r**6`

In our case we expect `r` to be much bigger than that, around 510 bits, which makes this property even stronger.
This means that value of the polynomial `r**6 + 5*r**5 + 10*r**4 + 13*r**3 + 10*r**2 + 5*r + 1` will be realtively close to `r**6`.
And if we calculate 6-th root the value should be pretty much identical, because all lower order terms will simply be swallowed as small fractions.

We can confirm this by:

```python
r = int(gmpy2.iroot(n, 6)[0])
p, q = r ** 2 + r + 1, r ** 2 + 3 * r + 1
print(gmpy2.is_prime(p))
print(gmpy2.is_prime(q))
assert n == p ** 2 * q
```

Now that we have `p` and `q` we can proceed with decrypting the flag.
The issue now is that this encryption does not match RSA conditions -> `gcd(e,phi(n))!=1`.
This is quite obvious since:

`phi(n) = phi((p**2)*q) = phi(p**2) * phi(q) = p*(p-1) * (q-1)` 

And in our case `e = n = (p**2)*q`

So `phi(n)` and `e` share a factor `p`.

One approach we could try would be to divide `e` by `p` and calculate `d` for such `e`, but as a result we would just get `flag**p mod n` which doesn't help us much because we can't easily calculate k-th modular root.
But we took a different path and guessed that `flag` might not be padded and thus it would be reasonably short.
Specifically shorter not only than `n`, which is expected, but also shorted than `p*q`.

We could calculate `ciphertext % (p*q)` transforming this problem back to classic RSA.
We were lucky and this approach worked just fine:

```python
enc = enc % (p * q)
e = p * p * q
fi = (p - 1) * (q - 1)
d = modinv(e, fi)
flag_p = gmpy2.powmod(enc, d, (p * q))
print(long_to_bytes(flag_p))
```

Which gave us `ASIS{_Wo0W_Y0u_4r3_Mas73R_In____Schmidt-Samoa___}`

Whole solver [here](john.py)

As it turns out this is an existing cryptosystem, and could have been solved by:

```python
d = modinv(n, lcm(p - 1, q - 1))
flag_p = gmpy2.powmod(enc, d, (p * q))
print(long_to_bytes(flag_p))
```
