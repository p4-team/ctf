# Vigenere 3d (Crypto, 100p)

In the task we get the code:

```python
import sys
def _l(idx, s):
    return s[idx:] + s[:idx]
def main(p, k1, k2):
    s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz_{}"
    t = [[_l((i+j) % len(s), s) for j in range(len(s))] for i in range(len(s))]
    i1 = 0
    i2 = 0
    c = ""
    for a in p:
        c += t[s.find(a)][s.find(k1[i1])][s.find(k2[i2])]
        i1 = (i1 + 1) % len(k1)
        i2 = (i2 + 1) % len(k2)
    return c
print main(sys.argv[1], sys.argv[2], sys.argv[2][::-1])
```

And a call log:

```
$ python Vigenere3d.py SECCON{**************************} **************
POR4dnyTLHBfwbxAAZhe}}ocZR3Cxcftw9
```

We know that the flag has format: `SECCON{**************************}`, key has 14 characters and ciphertext is `POR4dnyTLHBfwbxAAZhe}}ocZR3Cxcftw9`.

First thing to prepare is decryption function, to use once we manage to recover the key:

```python
def decrypt(ct, k1, k2):
    s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz_{}"
    t = [[_l((i + j) % len(s), s) for j in range(len(s))] for i in range(len(s))]
    i1 = 0
    i2 = 0
    decrypted = ""
    for a in ct:
        for c in s:
            if t[s.find(c)][s.find(k1[i1])][s.find(k2[i2])] == a:
                decrypted += c
                break
        i1 = (i1 + 1) % len(k1)
        i2 = (i2 + 1) % len(k2)
    return decrypted
```

This is a very naive brute-force decryptor, but we don't need anything more fancy.
Now we need to somehow recover the encryption key.

It's easy to notice that this enryption can generate identical ciphertexts for many different keys.
In fact for any chosen key character at position `x` there is a corresponding character at position `13-x` which will produce the right ciphertext character from the plaintext. 
This is simply because array `t` contains all possible combinations.
This means we actually need to recover only 7 characters of the key, because they will automatically fix the other 7 characters.

We can run:
```python
def recover_key(known_prefix, ciphertex):
    final_key = ['*'] * 14
    for pos in range(7):
        for c in s:
            partial_candidate_key = ['*'] * 14
            partial_candidate_key[pos] = c
            partial_candidate_key[13 - pos] = c
            key = "".join(partial_candidate_key)
            res = encrypt(known_prefix, key, key[::-1])
            if res[pos] == ciphertex[pos]:
                final_key[pos] = c
                final_key[13 - pos] = c
                print "".join(final_key)
    return "".join(final_key)
```

To generate a key which will be a palindrome.
We could just as well always set `partial_candidate_key[13 - pos] = 'A'` or any other fixed character.

Once we run this, we recover the key and can decrypt the flag: `SECCON{Welc0me_to_SECCON_CTF_2017}`

Full solver [here](vigenere.py)
