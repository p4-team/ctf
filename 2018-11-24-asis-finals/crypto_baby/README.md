# Made by baby (for, 141p, 29 solved)

This was a very nice, and not so trivial crypto challenge.
In the end it turned out very simple, but nothing really suggested that, so we did a bit of an overkill here.

In the challenge we get [encryption code](babymade.py) and [encrypted flag](flag.enc) to work with.
We can see that the flag is supposed to be a PNG file.

The encryption code is rather simple:

```python
from secret import exp, key

def encrypt(exp, num, key):
    assert key >> 512 <= 1
    num = num + key
    msg = bin(num)[2:][::-1]
    C, i = 0, 1
    for b in msg:
        C += int(b) * (exp**i + (-1)**i)
        i += 1
    try:
        enc = hex(C)[2:].rstrip('L').decode('hex')
    except:
        enc = ('0' + hex(C)[2:].rstrip('L')).decode('hex')
    return enc
```

We can see that secret `key` parameter is at most 512 bits long, so it will modify only the lowest 128 bytes of the PNG.
This shouldn't be an issue - we can replace the broken PNG trailer, and the picture should be still fine.

The encryption itself is performed bit by bit, in reverse bit order.
If `i-th` bit is lighted, then we add `exp**i` to the accumulator and we also add `(-1)**i`.

The second part with `-1` shouldn't be much of an issue, because assuming a nice random bits distribution in the data, we should get roughly the same number of `1` and `-1` and they should more-or-less even out in the end.

The final encrypted payload is, therefore, a polynomial `exp**i + exp**j + exp**k +.... -+C` where `C` is some small number and `i<j<k<...`

We don't know exactly which powers are present in the polynomial.

It's easy to notice that if we remove the `C` value, then the whole polynomial has to be divisible by `exp`!
And if we divide it by `exp` then the division remainder has to be either `0` or `1`, depending if the divided polynomial contained `exp` in first power or not.
This is a very strong property, because apart from the case when `exp=2`, it simply won't hold for the wrong number over large number of terms.

So our solution approach is as follows:

1. Loop over some small range of values we consider possible for `C` and add/subtract this value from the encrypted payload, hoping to get a clean polynomial. We assumed `+-1024`.
2. Factor the polynomial up to some reasonable primes. We assumed primes up to `2*20`.
3. For all possible composite numbers created from primes we got, we check if our property with division remainders hold. If it holds, then we extract the bits.
4. We then invert the bits, combine a byte stream and check if PNG header strings `PNG` and `IHDR` are present.
5. If they are, then we overwrite the PNG trailer section and save this as a png file.

We run this in paralell, but immediately get back first result for `C = 17` and `exp = 3`:

[result](out17_3.png)

It's a bit broken, but most image viewers can handle it.
For our defence, nothing really indicated that `exp` would be so tiny!

So the flag is: `ASIS{n3w_g1f7_by_babymade_in_ASIS!!!}`

Whole solver [here](solver.py)
