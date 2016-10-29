# DaaS (crypto 50)

###ENG
[PL](#pl-version)

In the task we get the address of the remote service and the [source code](DaaS.py).
We also get a file with RSA-encrypted flag.

```
flag = 0xc18b1d3b892e29863d8a6b46059995173635a3fd9f2ad877143a2d14ee736d8b12f9e735d6877a553312101eb757a0e3b3795bea88f2b4f72d1eb47ef6062a0dfd659892dfb2b98c70406e0c3e5e8624e81622b772d9e4183a29c9bf2f10ef15de3bfcb112a5f76688a146466db5a8e2dfe6679806c8e0b244458296efcba450
```

The remote service can perform RSA-decode for any input we want, apart from the flag itself.

The RSA implementation is not using any padding, and therefore it is homomorphic, which is what we use to break the encryption.
Homomorphic property means in this case that `rsa_encrypt(a*b) = rsa_encrypt(a)*rsa_encrypt(b)` and the same goes for decrypt, since both are doing exactly the same mathematical operation - modular power.

RSA encryption is `ciphertext = plaintext^e (mod n)` and decryption is `plaintext = ciphertext^d (mod n)`.

We cannot ask the server to decrypt the flag for us, but we can ask it to decrypt `int(flag)/2`, which means we will get the value `enc_flag_2 = (enc_flag/2)^d (mod n)`.
We can then ask the server to decrypt value `2` for us, which means we will get `two = 2^d (mod n)`

Now if we simply multiply those numbers (mod n) we will get:

`enc_flag_2 * two = (enc_flag/2)^d (mod n) * 2^d (mod n) = ((enc_flag/2)^d * 2^d) mod n = enc_flag^d mod n = flag`

So we just sent `flag/2` and `2` as inputs and then recovered flag with:

```python
def long_to_bytes(data):
    data = str(hex(data))[2:-1]
    return "".join([chr(int(data[i:i + 2], 16)) for i in range(0, len(data), 2)])

n = 0xcd67fc599866f87bc45ff87c1634aa144ee257c963ab2541052f3b38d22a11b255b0dd9318153699664b1007b7f38118df77f703909888c3930b73221c57828fc423a643b1eaf47f03d6c24b11d907f979dae4aa47347959c7c77bda8f9804dd95cc438d75ced522c7391a5d1432978440bfacc9939a33d6e6e058b15a084f99
enc_flag_2 = 0x120643f13ec8942b09296bb1e08c3b1608804771815e7a138560e6e5801cae4c073d5f88f3ced989743818a91290f3772614462f3fa6af7cdf5b534ccb031124656117714f7ae602016b9bd732f366be53c59501d393caba6fb12e38b5e55ffc57ccbb4ce3c7a3e2d344cf2a7e487d45c4e0c76e0cf5e8846efdce0955f81930
two = 0x3a997500f5c2e8cb21996f73cc3d05f58a8f6003fa2e97481dc09f04517ffbf6ef6585f415cb2ea95449ab7ced07443e1b330deeed169bb3d88088167a37434cf1d39ce5b639c1b99a18279f26b8f2e197c0a94a291a6d2efb42adf27d082791be6e589e62dfbc85afc882996a4a68d474f0c334ef29b5a953ec4fbcff52bd38

print(long_to_bytes((enc_flag_2 * two) % n))

```

Which gave `ECTF{Good job! You broke RSA!}`

###PL version

W zadaniu dostajemy adres zdalnego serwera oraz [kod źródłowy](DaaS.py).
Dostajemy także plik z flagą zaszyfrowaną za pomocą RSA.


```
flag = 0xc18b1d3b892e29863d8a6b46059995173635a3fd9f2ad877143a2d14ee736d8b12f9e735d6877a553312101eb757a0e3b3795bea88f2b4f72d1eb47ef6062a0dfd659892dfb2b98c70406e0c3e5e8624e81622b772d9e4183a29c9bf2f10ef15de3bfcb112a5f76688a146466db5a8e2dfe6679806c8e0b244458296efcba450
```

Serwer pozwala zdekodować za pomocą RSA dowolne dane, oprócz samej flagi.

Implementacja RSA nie używa paddingu, co oznacza że operacje są homomorficzne, co pozwala nam na złamanie szyfrowania.
Homomorfizm w tym kontekście oznacza, że `rsa_encrypt(a*b) = rsa_encrypt(a)*rsa_encrypt(b)` i analogicznie dla operacji deszyfrowania, ponieważ obie funkcje realizują tą samą operacje matematyczną - potęgowanie modularne.

Szyfrowanie RSA to `ciphertext = plaintext^e (mod n)` a deszyfrowanie `plaintext = ciphertext^d (mod n)`.

Nie możemy poprosić serwra o deszyfrowanie flagi, ale możemy poprosić o deszyfrowanie `int(flag)/2`, co oznacza że dostaniemy wartość `enc_flag_2 = (enc_flag/2)^d (mod n)`.
Teraz możemy poprosić serwer o dekodowanie wartości `2`, co oznacza że dostaniemy `two = 2^d (mod n)`.

Teraz jeśli pomnożymy te liczby (mod n) dostaniemy:

`enc_flag_2 * two = (enc_flag/2)^d (mod n) * 2^d (mod n) = ((enc_flag/2)^d * 2^d) mod n = enc_flag^d mod n = flag`

Więc wysyłamy do serwera `flag/2` oraz `2` a następnie odzyskujemy flagę przez:

```python
def long_to_bytes(data):
    data = str(hex(data))[2:-1]
    return "".join([chr(int(data[i:i + 2], 16)) for i in range(0, len(data), 2)])

n = 0xcd67fc599866f87bc45ff87c1634aa144ee257c963ab2541052f3b38d22a11b255b0dd9318153699664b1007b7f38118df77f703909888c3930b73221c57828fc423a643b1eaf47f03d6c24b11d907f979dae4aa47347959c7c77bda8f9804dd95cc438d75ced522c7391a5d1432978440bfacc9939a33d6e6e058b15a084f99
enc_flag_2 = 0x120643f13ec8942b09296bb1e08c3b1608804771815e7a138560e6e5801cae4c073d5f88f3ced989743818a91290f3772614462f3fa6af7cdf5b534ccb031124656117714f7ae602016b9bd732f366be53c59501d393caba6fb12e38b5e55ffc57ccbb4ce3c7a3e2d344cf2a7e487d45c4e0c76e0cf5e8846efdce0955f81930
two = 0x3a997500f5c2e8cb21996f73cc3d05f58a8f6003fa2e97481dc09f04517ffbf6ef6585f415cb2ea95449ab7ced07443e1b330deeed169bb3d88088167a37434cf1d39ce5b639c1b99a18279f26b8f2e197c0a94a291a6d2efb42adf27d082791be6e589e62dfbc85afc882996a4a68d474f0c334ef29b5a953ec4fbcff52bd38

print(long_to_bytes((enc_flag_2 * two) % n))

```

Co daje nam `ECTF{Good job! You broke RSA!}`
