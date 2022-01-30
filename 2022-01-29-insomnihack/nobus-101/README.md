# nobus-101

After reverse-engineering the binary, we learned that it uses the Dual_EC_DRBG backdoored
keys. The curve generatoin itself is deterministic, but we needed to reverse it. It looks like
this:

```python
MAGIC = 0x132867e88e82431dc40ba24e11bf3ec7ffb18764a3b4df1f5957fd5f37d8be40

def gen_backdoor():
    P = P256.G
    e = MAGIC
    d = mod_inv(e, P256.q)
    Q = e * P
    return P, Q, d
```

This makes it possible to recover the seed using only two random numbers, using the well-studied
attack technique on Dual_EC_DRBG keys.

We modified the https://github.com/AntonKueltz/dual-ec-poc attack to get a deterministic
seed recovery.

The interesting piece of our code is:

```python
def recover_s(bits0, bits1, Q, d):
    for high_bits in range(2**16):
        guess = (high_bits << (8 * 30)) | bits0
        on_curve, y = find_point_on_p256(guess)

        if on_curve:
            # use the backdoor to guess the next 30 bytes
            point = Point(guess, y, curve=P256)
            s = (d * point).x
            r = (s * Q).x & (2**(8 * 30) - 1)

            if r == bits1:
                return s


def main():
    P, Q, d = gen_backdoor()
    data = requests.get("http://nobus101.insomnihack.ch:13337/prng").text
    bits0, bits1, *rest = data.split()
    bits0 = int(bits0, 16)
    bits1 = int(bits1, 16)

    s = recover_s(bits0, bits1, Q, d)
    curve = DualEC(s, P, Q)
    prediction = hex(curve.genbits())[2:].rjust(60, '0')
    text = requests.post("http://nobus101.insomnihack.ch:13337/flag", data=prediction.encode())

    print(text.text)
```

This allowed us to recover the flag.

```
INS{7ru57_7h3_5c13nc3}
```
