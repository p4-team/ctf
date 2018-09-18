# Rot (Crypto)

The only thing we have in this challenge is the base64-encoded ciphertext:

```
JwxTBxELMFxDRUoaFU8BBwkAZz0tNjciQkZFMhEzQlpeEgMSBlQjFEoQXQAGEBYGDytLEFxdGhJf
UxYSRSg6YzQ8KkNGUDQKdl8fRQNMAxhVcRNdRBgLEx8MHRI2XFcRTBMEClIWAhA1PTcucyNWVUEy
DCURDlkVV1E+SSMDTRddGwIXQxAPLFFfR10JBE4PUzMKJTExI3MTUkNUMBZ2fBVDBkoC
```

I dislike ciphertext-only challenges, because to solve them you need to guess the algorithm, and it's neither practical nor fun. Not to mention that basing the difficulty of your cipher on secretness of your algorithm is a [well-known antipattern in cryptography](https://en.wikipedia.org/wiki/Kerckhoffs%27s_principle).

After wasting way too much time on guessing, we discoverd the encryption algorithm. We know the beginning of the flag (flag format is `scsctf_2018{.......}`), and xoring it with the ciphertext:

```python
import string

def xor(a, b):
    return ''.join(chr(ord(ac) ^ ord(bc)) for ac, bc in zip(a, b))

data = 'JwxTBxELMFxDRUoaFU8BBwkAZz0tNjciQkZFMhEzQlpeEgMSBlQjFEoQXQAGEBYGDytLEFxdGhJfUxYSRSg6YzQ8KkNGUDQKdl8fRQNMAxhVcRNdRBgLEx8MHRI2XFcRTBMEClIWAhA1PTcucyNWVUEyDCURDlkVV1E+SSMDTRddGwIXQxAPLFFfR10JBE4PUzMKJTExI3MTUkNUMBZ2fBVDBkoC'.decode('base64')

print xor(data, 'scsctf_2018{')
```

Yields `To demonstra` which looks like a beginning of an English sentence.

If the data was xored with completely random sequence of bytes, the scheme would be [provably secure](https://en.wikipedia.org/wiki/One-time_pad). But we expect the flag to be shorter than the whole ciphertext, so this turns into a [repeated key xor](https://en.wikipedia.org/wiki/XOR_cipher), a well-known weak cipher.

We brute-forced few key lengths to discover the proper one, and found it:

```python
...

def safe(x):
    return ''.join((c if 0x20 <= ord(c) < 0x7f else '.') for c in x)

print safe(xor(data, ('scsctf_2018{' + '\x00' * 31) * 100))
```

That code prints:

```
To demonstra.O....g=-67"BFE2.3BZ^....T#.J.]security mea._S..E(:c4<*CFP4.v_.E.L..Uq.]D.xploiting th..R...5=7.s#VUA2.%..Y.WQ>I#.M.]had discover.N.S3.%11#s.RCT0.v|.C.J.
```

Or, perhaps more clearly:

```
To demonstra.O....g=-67"BFE2.3BZ^....T#.J.]
security mea._S..E(:c4<*CFP4.v_.E.L..Uq.]D.
xploiting th..R...5=7.s#VUA2.%..Y.WQ>I#.M.]
had discover.N.S3.%11#s.RCT0.v|.C.J.
```

How to get the rest of the plaintext (or, equivalently, the rest of the key)?
We can guess plaintext words and update keys based on our guesses.

In other words, we know that `ciphertext_byte = plaintext_byte ^ key_byte`. If we guess `plaintext_byte` correctly, we can recover `key_byte` and use it to decrypt other ciphertexts.

For example, `security mea` sounds awfully like `security measures `.
Decrypting the code with zero bytes on unknown positions yield `security mea\x12_S\x16\x12E...`.
We know that this is supposed to be `security measures `. If we xor the two values together we get
`\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00a*!sae` - the non-zero bytes are next bytes of our key.

After updating our key and running the decryption again, we get:

```
To demonstrate theg=-67"BFE2.3BZ^....T#.J.
security measures (:c4<*CFP4.v_.E.L..Uq.]De
xploiting the secu5=7.s#VUA2.%..Y.WQ>I#.M.
had discovered. Ro%11#s.RCT0.v|.C.J.
```

Now we can guess `security` in the third row, etc. After repeating this process for a few times, we recovered the whole plaintext:


```
To demonstrate the inadequacies of current security measures on computer networks by exploiting the security defects that I had discovered
```

And the flag/key:

```
scsctf_2018{a*!saeGTCWSG33$QxV1z1t#qs&Qq$d}
```
