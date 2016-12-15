# Vigenere (crypto 100)

###ENG
[PL](#pl-version)

In the task we get a ciphertext:

```
LMIG}RPEDOEEWKJIQIWKJWMNDTSR}TFVUFWYOCBAJBQ
```

And information that this is Vigener Cipher with alphabet:

```
ABCDEFGHIJKLMNOPQRSTUVWXYZ{}
```

And the md5 of plaintext is `f528a6ab914c1ecf856a1d93103948fe`

We of course know the flag prefix `SECCON{` so we can instantly recover the prefix of the key:

```python
def get_key_prefix(alphabet, ct, known_pt):
    result = ""
    for i in range(len(known_pt)):
        plain = known_pt[i]
        cipher = ct[i]
        key = alphabet[alphabet.index(cipher) - alphabet.index(plain)]
        result += key
    return result
```

which gives us `VIGENER`

Next we can just brute-force the missing 4 bytes of the key:

```python
def decode(alphabet, ct, key):
    result = ""
    for i in range(len(ct)):
        c = ct[i]
        k = key[i % len(key)]
        if k != "?":
            p = alphabet[alphabet.index(c) - alphabet.index(k)]
        else:
            p = "?"
        result += p
    return result


def worker(data):
    c, alphabet, ct, key = data
    key += c
    for suffix in itertools.product(alphabet, repeat=4):
        new_key = key + "".join(suffix)
        pt = decode(alphabet, ct, new_key)
        if hashlib.md5(pt).hexdigest() == "f528a6ab914c1ecf856a1d93103948fe":
            print(pt)
            return pt


def main():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ{}"
    ct = "LMIG}RPEDOEEWKJIQIWKJWMNDTSR}TFVUFWYOCBAJBQ"
    key_prefix = get_key_prefix(alphabet, ct, "SECCON{")
    print('key prefix ', key_prefix)
    print(brute(worker, [(c, alphabet, ct, key_prefix) for c in alphabet]))


if __name__ == '__main__':
    freeze_support()
    main()
```

Which gives us almost instantly `SECCON{ABABABCDEDEFGHIJJKLMNOPQRSTTUVWXYYZ}`

###PL version

W zadaniu dostajemy zaszyfrowany tekst:

```
LMIG}RPEDOEEWKJIQIWKJWMNDTSR}TFVUFWYOCBAJBQ
```

I informacje że to szyfr Vigenera z alfabetem:

```
ABCDEFGHIJKLMNOPQRSTUVWXYZ{}
```

Mamy też md5 plaintextu: `f528a6ab914c1ecf856a1d93103948fe`

I oczywiście znamy prefix flagi `SECCON{` więc możemy od razu odzyskać prefix klucza:

```python
def get_key_prefix(alphabet, ct, known_pt):
    result = ""
    for i in range(len(known_pt)):
        plain = known_pt[i]
        cipher = ct[i]
        key = alphabet[alphabet.index(cipher) - alphabet.index(plain)]
        result += key
    return result
```

co daje nam `VIGENER`

Następnie możemy brute-forcować brakujące 4 bajty klucza:

```python
def decode(alphabet, ct, key):
    result = ""
    for i in range(len(ct)):
        c = ct[i]
        k = key[i % len(key)]
        if k != "?":
            p = alphabet[alphabet.index(c) - alphabet.index(k)]
        else:
            p = "?"
        result += p
    return result


def worker(data):
    c, alphabet, ct, key = data
    key += c
    for suffix in itertools.product(alphabet, repeat=4):
        new_key = key + "".join(suffix)
        pt = decode(alphabet, ct, new_key)
        if hashlib.md5(pt).hexdigest() == "f528a6ab914c1ecf856a1d93103948fe":
            print(pt)
            return pt


def main():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ{}"
    ct = "LMIG}RPEDOEEWKJIQIWKJWMNDTSR}TFVUFWYOCBAJBQ"
    key_prefix = get_key_prefix(alphabet, ct, "SECCON{")
    print('key prefix ', key_prefix)
    print(brute(worker, [(c, alphabet, ct, key_prefix) for c in alphabet]))


if __name__ == '__main__':
    freeze_support()
    main()
```

Co od razu daje nam `SECCON{ABABABCDEDEFGHIJJKLMNOPQRSTTUVWXYYZ}`
