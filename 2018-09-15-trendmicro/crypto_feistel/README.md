# Feistel (crypto, 300p)

In the task we get a [plaintext-ciphertext pair](pt-ct.txt) and [encrypted flag](flag.txt).

We also get a description of the encryption algorithm - it's a classic Feistel cipher, but the function F applied in the iterations is simply XOR with deterministic round key.

This means the round keys for the known PT-CT pair are the same as for the encrypted flag!

If we write down what are the possible outcomes from the encryption we can notice a pattern:

```
C1 = PT1 ^ PT2 ^ K1
C2 = C1 ^ P2 ^ K2 = (PT1 ^ PT2 ^ K1) ^ P2 ^ K2 = PT1 ^ K1 ^ K2
C3 = C1 ^ C2 ^ K3 = (PT1 ^ PT2 ^ K1) ^ (PT1 ^ K1 ^ K2) ^ K3 = PT2 ^ K2 ^ K3
C4 = C2 ^ C3 ^ K4 = (PT1 ^ K1 ^ K2) ^ (PT2 ^ K2 ^ K3) ^ K4 = PT1 ^ PT2 ^ K1 ^ K3 ^ K4
C5 = C4 ^ C3 ^ K5 = ... = PT1 ^ K1 ^ K2 ^ K4 ^ K5
```

It loops like this, so that in the resulting ciphertexts we have either `PT1 ^ KX` or `PT2 ^ KX` or `PT1 ^ PT2 ^ KX`, where `KX` is XOR of some round keys.

It's easy to notice that we can XOR given `C` with `PT1`, `PT1` or `PT1 ^ PT2` to recover the `KX`, and then XOR this again with flag ciphertexts, in order to decrypt them.

W do this with a simple script:

```python
from crypto_commons.generic import long_to_bytes, chunk, is_printable


def main():
    pt = '010000010110111000100000011000010111000001110000011011000110010100100000011000010110111001100100001000000110000101101110001000000110111101110010011000010110111001100111011001010010000001110111011001010110111001110100001000000111010001101111001000000101010001110010011001010110111001100100'
    ct = '000100100011000101110101001101100110001100110001001110100011110101100000011110010010111000110011001110000000110100100101011111000011000000100001010000100110011100100001011000000111001101110100011011100110000000100000011011010110001001100100001011010110111001100110001010110110110101110001'
    flag = '000000110000111001011100001000000001100100101100000100100111111000001001000001100000001100001001000100100010011101001010011000010111100100100010010101110100010001000010010101010100010101111111010001000110000001101001011111110111100001100101011000010010001001001011011000100111001001101011'
    print(long_to_bytes(int(pt, 2)))
    pt1, pt2 = tuple(map(lambda x: int(x, 2), chunk(pt, len(ct) / 2)))
    ct1, ct2 = tuple(map(lambda x: int(x, 2), chunk(ct, len(ct) / 2)))
    f1, f2 = tuple(map(lambda x: int(x, 2), chunk(flag, len(ct) / 2)))
    for x in [pt1, pt2, pt1 ^ pt2]:
        for y in [ct1, ct2, ct1 ^ ct2]:
            for z in [f1, f2, f1 ^ f2]:
                result = long_to_bytes(x ^ y ^ z)
                if is_printable(result):
                    print(result)


main()
```

And we get the flag: `TMCTF{Feistel-Cipher-Flag-TMCTF2018}`
