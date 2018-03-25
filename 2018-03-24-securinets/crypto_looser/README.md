# Looser (Crypto)

We get [encrypted flag](flag.png.crypt) to work with.
Judging by extension we can deduce that the orignal file was a PNG.
We don't have much to work with, so we assume the simplest approach - some kind of stream cipher / XOR encryption.
We know header of PNG file, so we can XOR the existing header with what we expect, and therefore extract the potential XOR key.

We assume that this is going to be some kind of repeating-xor encryption, so once we get the key, we can multiply it and decrypt the whole file:

```python
from crypto_commons.generic import xor, xor_string


def main():
    with open('flag.png.crypt', 'rb') as f:
        data = f.read()
        png_header = [137, 80, 78, 71, 13, 10, 26, 10, 0, 0, 0, 0xd, 0x49, 0x48, 0x44, 0x52, 0x0, 0x0]
        result = xor(png_header, map(ord, data[:len(png_header)]))
        key = "".join([chr(c) for c in result]) + ("\0" * (18 - len(png_header)))
        print(key.encode("hex"))
        with open('result.png', 'wb') as f:
            f.write(xor_string(data, key * (len(data) / len(key))))


main()
```

As it turns out, it was even simpler - the whole file was encrypted with a single byte XOR key `e`.
We recover the original picture:

![](result.png)
