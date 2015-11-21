## Crypto 400 (crypto, 400p)

### PL

[ENG](#eng-version)

Dostajemy cztery ciphertexty, oraz trzy odpowiadające im plaintexty. W czwartym ciphertexcie znajduje się flaga, i naszym zadaniem jest odzyskać ją:

```python
inp0 = "People don't understand computers. Computers are magical boxes that do things. People believe what computers tell them."
out0 = "a2ccb5e4a4f694bd8a87cec3679d69a87db401a4199006dbb0ccbfe6a7ecc3e4f7b2e426c53fed35f95fe3498d038bebdbadeabce9cdfecf87968776876be12088228041c951730a7a30702e197802372236c03dc443934bef55ee71e03f423f7e213715360c1e060aec10fa7ea57ad36f94069f066c50".decode("hex")

inp1 = "There are two types of encryption: one that will prevent your sister from reading your diary and one that will prevent your government."
out1 = "2e4d3e6d2433102f12514b45ae01ef33f32d9869da5b891177076b3b7f34172d237224ca28da588151f349b023a5335a6a0155014b69557c343e2fd3358a538f3c8330a36ffe8eec999ac69abf94a7acbbe01fe108dd4f96378529b96df397e6e6a2fadeb2919b979b38c131f93aa015b709990d9fecdebafdbbf79ead9d819163867db97bb854".decode("hex")

inp2 = "There's an entire flight simulator hidden in every copy of Microsoft Excel 97."
out2 = "fa99eab9f0e0d1bc8588c6da30cb38ef3aa101bc0989139ab2d2a5e1a0f3d8f9f6efb950b54680489e7dda6da923afcfadcfc99bc8ffd4a9aebbe521dc20f82291358510dc6e147a074846463554".decode("hex")

out3 = "b4d0b1b0e5bd8ae7cdcbc4d139cf75b173ad4bfb0787008ff2cdf3bffda783f6fff2a44ba81fd61edf3c853daa65ea9ce99690d586e1dee2e1f7a949a916d50dbd19bc2eab3e50380e0d7a2c1d205a59455fbe0ffa2ea63b9074ce43d11e715d495401235f693e31289b2c8d198158f81ba471b32917644e".decode('hex')

inp = [inp0, inp1, inp2]
out = [out0, out1, out2, out3] 
```

Nie wiemy w jaki sposób zostały zaszyfrowane te dane, musimy więc uciec sie do kryptoanalizy. Jako podpowiedź, w treści zadania otrzymaliśmy informację że szyfr nie używa żadnego klucza.

Pierwszą rzeczą jaką zauważamy, jest bardzo specyficzny rozkład najwyższego bitu wiadomości:

```python
for i in range(len(out)):
    o = out[i]
    print ''.join('1' if ord(oc)&0x80 != 0 else '0' for oc in o)
```

Co daje nam w wyniku:

    11111111111101010101010111111111111010101010101111111111111010101010100000000000001010101010100000000000010101010101000
    000000000000101010101010000000000001010101010100000000000001010101010111111111111101010101010111111111111010101010101111111111110101010
    111111111111010101010101111111111110101010101011111111111110101010101000000000
    111111111111010101010101111111111110101010101011111111111110101010101000000000000010101010101000000000000101010101010000

To bardzo ciekawa informacja - najwyższe bity w każdej wiadomośći są dokładnie takie same (poza drugą wiadomością w której są flipowane).

Kolejna ciekawa rzecz którą odkryliśmy - jeśli będziemy xorować pierwszy bajt CT (ciphertextu) z drugim, drugi z trzecim, etc, to dla drugiego i trzeciego wejścia wynik będzie sie zaczynał tak samo:`

```python
for o in out:
    for i in range(20):
        print ord(o[i]) ^ ord(o[i+1]), 
    print
```

Wynik:

    110 121 81 64 82 98 41 55 13 73 13 164 250 244 193 213 201 181 165 189
    99 115 83 73 23 35 63 61 67 26 14 235 175 238 220 192 222 181 241 179
    99 115 83 73 16 49 109 57 13 78 28 234 251 243 215 213 155 160 189 181
    100 97 1 85 88 55 109 42 6 15 21 232 246 186 196 194 222 230 176 252

Dlaczego tak się dzieje? Drugi i trzeci plaintext zaczyna się tak samo (pierwsze pięć bajtów jest identyczne).

Ale szósty bajt plaintextu się już różni, tak samo ct[4] ^ ct[5] jest różne dla 2 i 3 ciphertextu.

W tym momencie dokonaliśmy ciekawego spostrzeżenia (albo zgadywania, jak kto woli).
Nazwijmy efekty xorowania kolejnych znaków CT jako xorct (xorct[x] = ct[x] ^ ct[x+1])

```python
plain2[5] = " " = 0x20
plain3[5] = "'" = 0x27

xorct2[5] = 0x17
xorct3[5] = 0x10

plain2[5] ^ plain3[5] = 7
xorct2[5] ^ xorct3[5] = 7
```

Okazuje się że to nie przypadek - ta własność zachodzi dla każdego indeksu.
Mając tak silną zależność między plaintextem i ciphertextem, napisanie dekryptora dla ostatniego ciphertextu jest trywialne.

Podsumowanie pomysłu stojącego za dekryptorem (kod niżej) - bierzemy plaintext1 i odpowiadający mu ciphertext1 (musiemy mieć przykładowe zdekryptowane dane).
I teraz żeby zdekryptować ciphertext2 (wynik nazwiemy plaintext2), zauważamy że dla każdego indekxu `i` zachodzi

    plain1[i] ^ plain2[i] == xorct1[i] ^ xorct2[i]

(Przypominam, xorct[i] to oznaczenie na ct[i] ^ ct[i+1])
Więc:

    plain2[i] == xorct1[i] ^ xorct2[i] ^ plain1[i]

Nasz oryginalny kod (będący trochę brzydki bo "bruteforcuje" bajty, ale napisany na szybko, ale co dziwne - zadziałał od razu):

```python
for i in range(len(out0)):
    for c in range(256):
        if (ord(out1[i]) ^ ord(out1[i+1])) ^ (ord(out3[i]) ^ ord(out3[i+1])) == ord(inp1[i+1]) ^ c:
            print chr(c),
```

Ładniejsza wersja (napisana podczas pisania tego writeupa, dla porządku):

```python
print ''.join(chr((ord(out1[i]) ^ ord(out1[i+1])) ^ (ord(out3[i]) ^ ord(out3[i+1])) ^ ord(inp1[i+1])) for i in range(len(out0)))
```

Wynik:

    ow you really are a guru, even if no key was used to make it impossible. Your flag is: c7ddf0e946cc0a5ba09807ce3d33f9a7

### ENG version

We get four ciphertexts and three corresponding plaintexts. The fourth ciphertext contains the flag and we are supposed to decode it:

```python
inp0 = "People don't understand computers. Computers are magical boxes that do things. People believe what computers tell them."
out0 = "a2ccb5e4a4f694bd8a87cec3679d69a87db401a4199006dbb0ccbfe6a7ecc3e4f7b2e426c53fed35f95fe3498d038bebdbadeabce9cdfecf87968776876be12088228041c951730a7a30702e197802372236c03dc443934bef55ee71e03f423f7e213715360c1e060aec10fa7ea57ad36f94069f066c50".decode("hex")

inp1 = "There are two types of encryption: one that will prevent your sister from reading your diary and one that will prevent your government."
out1 = "2e4d3e6d2433102f12514b45ae01ef33f32d9869da5b891177076b3b7f34172d237224ca28da588151f349b023a5335a6a0155014b69557c343e2fd3358a538f3c8330a36ffe8eec999ac69abf94a7acbbe01fe108dd4f96378529b96df397e6e6a2fadeb2919b979b38c131f93aa015b709990d9fecdebafdbbf79ead9d819163867db97bb854".decode("hex")

inp2 = "There's an entire flight simulator hidden in every copy of Microsoft Excel 97."
out2 = "fa99eab9f0e0d1bc8588c6da30cb38ef3aa101bc0989139ab2d2a5e1a0f3d8f9f6efb950b54680489e7dda6da923afcfadcfc99bc8ffd4a9aebbe521dc20f82291358510dc6e147a074846463554".decode("hex")

out3 = "b4d0b1b0e5bd8ae7cdcbc4d139cf75b173ad4bfb0787008ff2cdf3bffda783f6fff2a44ba81fd61edf3c853daa65ea9ce99690d586e1dee2e1f7a949a916d50dbd19bc2eab3e50380e0d7a2c1d205a59455fbe0ffa2ea63b9074ce43d11e715d495401235f693e31289b2c8d198158f81ba471b32917644e".decode('hex')

inp = [inp0, inp1, inp2]
out = [out0, out1, out2, out3] 
```

We don't know how the data were encoded so we need to perform some cryptoanalysis. As a hint in the task there is information that the cipher does not use any key.

First thing we notice is that there is a very particular distribution of values in the highest bit of the ciphertexts:

```python
for i in range(len(out)):
    o = out[i]
    print ''.join('1' if ord(oc)&0x80 != 0 else '0' for oc in o)
```

We get:

    11111111111101010101010111111111111010101010101111111111111010101010100000000000001010101010100000000000010101010101000
    000000000000101010101010000000000001010101010100000000000001010101010111111111111101010101010111111111111010101010101111111111110101010
    111111111111010101010101111111111110101010101011111111111110101010101000000000
    111111111111010101010101111111111110101010101011111111111110101010101000000000000010101010101000000000000101010101010000

This is interesting - the highest bits in every message are identical (or flipped in the second message).

Next interesting find is that if we xor first byte of ciphertext (CT) with second, second with third etc. then for second and third inputs we will get identical results:

```python
for o in out:
    for i in range(20):
        print ord(o[i]) ^ ord(o[i+1]), 
    print
```

Result:

    110 121 81 64 82 98 41 55 13 73 13 164 250 244 193 213 201 181 165 189
    99 115 83 73 23 35 63 61 67 26 14 235 175 238 220 192 222 181 241 179
    99 115 83 73 16 49 109 57 13 78 28 234 251 243 215 213 155 160 189 181
    100 97 1 85 88 55 109 42 6 15 21 232 246 186 196 194 222 230 176 252

Why is that? Second and third plaintexts start exactly the same way (first 5 bytes are identical).

But sixth byte of plaintext is different and therefore ct[4] ^ ct[5] is different for second and third ciphertext.

At this point we noticed (or guessed) a very interesting rule.
Let's define effects of xoring consecutive characters from CT as xorct -> xorct[x] = ct[x] ^ ct[x+1]

```python
plain2[5] = " " = 0x20
plain3[5] = "'" = 0x27

xorct2[5] = 0x17
xorct3[5] = 0x10

plain2[5] ^ plain3[5] = 7
xorct2[5] ^ xorct3[5] = 7
```

It turns out this is not accidental - this property works for every index.

With such a strong correlation between plaitnext and ciphertext it becomes trivial to make a decryption algorithm for the last ciphertext.

Summary of the decryption algorithm (code is below) - we take plaintext1 and corresponding ciphertext1 (we need example of decoded data).
Now to decrypt ciphertext2 (we mark the result as plaintextx2), we notice that for every intex `i` there is:

    plain1[i] ^ plain2[i] == xorct1[i] ^ xorct2[i]

(As a reminder: xorct[i] means ct[i] ^ ct[i+1])
So:

    plain2[i] == xorct1[i] ^ xorct2[i] ^ plain1[i]

Our original code (quite messy since it brute-forces bytes, but we were trying to write it fast, interestingly it worked right away):

```python
for i in range(len(out0)):
    for c in range(256):
        if (ord(out1[i]) ^ ord(out1[i+1])) ^ (ord(out3[i]) ^ ord(out3[i+1])) == ord(inp1[i+1]) ^ c:
            print chr(c),
```

Pretty version (wrote when preparing this writeup):

```python
print ''.join(chr((ord(out1[i]) ^ ord(out1[i+1])) ^ (ord(out3[i]) ^ ord(out3[i+1])) ^ ord(inp1[i+1])) for i in range(len(out0)))
```

Result:

    ow you really are a guru, even if no key was used to make it impossible. Your flag is: c7ddf0e946cc0a5ba09807ce3d33f9a7
