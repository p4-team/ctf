# Crazy repetition of codes (crypto, 326p, 45 solved)

In the challenge we get a [source code](crc.py) which would print the flag once it finishes.
However, if we inspect the code, we can see there are multiple loops of `range(int("1" * 10000))` and that's a bit too much for our computers.

The code is pretty simple -> each loop calculates CRC-32 many times using previous result as input for the next iteration, and finally combines the key for decrypting the flag from parts acquired in each loop:

```python
for i in range(int("1" * 10000)):
  crc = crc32(crc, "SOME_STRING")
key += crc.to_bytes(4, byteorder='big')
```

The key observation in this challenge is that CRC32, as name suggests, has 32 bits.
Directly from pigeonhole principle we know that it has to have a cycle after at most 2**32 steps, simply because there are no other values we could get, some value has to repeat itself.
This means that we don't really need to calculate so many iterations of the loop, we can skip all but the last incomplete cycle!

So the idea is pretty simple:

- Calculate the loop until we get the repetition of the initial value `0` to find the cycle
- Next calculate `int("1" * 10000) % cycle_size` to calculate how many iterations we really need
- Decrypt the flag

For some performance improvements we can also use the fact that:

- Each key chunk is independent, so we can easily calculate them in paralell
- `zlib.crc32` in python is much faster than the provided one, and the only tweak is that we need to add `%2**32` because the zlib version uses signed integers

With those points in mind we simply run:

```python
import zlib
from multiprocessing import freeze_support

from crypto_commons.brute.brute import brute
from crypto_commons.generic import long_range, long_to_bytes


def break_for_const(val):
    crc = 0
    final_i = 0
    for i in long_range(0, int("1" * 10000)):
        if i % 2 ** 24 == 0:
            print(i / 2 ** 24)
        crc = zlib.crc32(val, crc)
        if crc == 0:
            final_i = (i % 2 ** 32) + 1
            break
    missing = int("1" * 10000) % final_i
    crc = 0
    for i in long_range(0, missing):
        crc = zlib.crc32(val, crc)
    return crc % 2 ** 32


def decrypt(key):
    from Crypto.Cipher import AES
    flag = "79833173d435b6c5d8aa08f790d6b0dc8c4ef525823d4ebdb0b4a8f2090ac81e".decode("hex")
    aes = AES.new(key, AES.MODE_ECB)
    print(aes.decrypt(flag))


def main():
    results = brute(break_for_const, ["TSG", "is", "here", "at", "SECCON", "CTF!"], processes=6)
    # results = [2962998607L, 3836056187L, 2369777541L, 3007692607L, 1526093488L, 3679021396L]
    print(results)
    key = "".join(map(long_to_bytes, results))
    decrypt(key)


main()

if __name__ == '__main__':
    freeze_support()
    main()

```

And recover the flag: `SECCON{Ur_Th3_L0rd_0f_the_R1NGs}`
