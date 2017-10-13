# Cameras (Crypto, 300p)

In the task we get [encrypted png](sec.png).
Our first guess is that it's going to be classic repeating key xor, so we try to solve it as such.
We know the constant 16 bytes of PNG header, so we can xor the first 16 bytes of the encrypted file to recover first 16 bytes of the xor key, and then xor the whole file with this key repeated.
We might be missing some bytes in the key by we can try padding it with 0 until we get some reasonable results for some padding length.
We can always look for some constant parts we should find -> IDAT, IHDR, IEND.

```python
import codecs

from crypto_commons.generic import xor


def main():
    with codecs.open("sec.png", "rb") as input_file:
        data = [ord(c) for c in input_file.read()]
        header = [137, 80, 78, 71, 13, 10, 26, 10]
        key = xor(data, header)
        print(key)
        with codecs.open("out.png", "wb") as output_file:
            output_file.write("".join([chr(c) for c in xor(data, key*10000)]))


main()
```

It turns that the recovered key is `[255, 255, 255, 255, 255, 255, 255, 255]` so it's even simpler then we expected.
Whole file is actually xored with the same value `0xFF`, or basically bits are negated.
We get: ![](out.png)
