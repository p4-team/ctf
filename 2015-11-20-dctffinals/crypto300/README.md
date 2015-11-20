## Crypto 300 (crypto, 300p)

### PL

[ENG](#eng-version)

Zadanie polegało na odwróceniu działania podanego algorytmu, zaimplementowanego w javascripcie, dla podanego zaszyfrowanego tekstu. Kod szyfrujący i deszyfrujący umieszczony w zadaniu znajduje się [tutaj](./crypto300.js)

Zaszyfrowanego tekst: `51136f3b763d7d5e5910106d423f0908093931284bc6eda1a4ffa595c390b390ef89a4a08ffb9797a2b797f5af92b7a0aaac9cf2dbf9ccecd5c8b3cbb9fffefa4fcf0c26d761f9145793fb6a44ed048cb92a1c0f420e3af756d66f2d1ee94414ed335f180b34fca1fda4f9698a23287ca9e9acb2e8b7c0216c132c078c93a438217e0927ce1afbcf016fd7cc6b1f8b903ec3c0a19f723ae5c0fa46679ded50d17259f89688a5ff4340784a155d`

Analiza kodu pozwoliła nam stwierdzić, że każdy z bajtów w zakodowanym tekście jest wynikiem operacji XOR na 3 wartościach: bajcie danych wejściowych, bajcie ze specjalnie przygotowanej tablicy z elementami 0-128 oraz bajcie z klucza. 
Jeśli klucz szyfrowania był za krótki, dokonywane było jego przedłużenie poprzez dokonanie przesunięcia bitowego w lewo o 1 pozycję, a następnie wykonanie kilku dodatkowych operacji bitowych a na koniec tak przygotowany element dodawany był na koniec klucza.
Przesuwanie bitów pewnego elementu klucza w celu uzyskania nowego elementu klucza oznaczało, że dla odpowiednio dlugiego tekstu pewne bajty będą xorowane z kluczem, kolejne bajty z poprzesuwanym kluczem itd.
Z tych 3 elementów xorowanych aby uzyskać ciphertext jedynie klucz mógł zawierać zapalony najwyższy bit, ponieważ klucz w trakcie "wydłużania" przesuwał bity w lewo.
Oznacza to, że mogliśmy sprawdzić czy wysoki bit ciphertextu jest zapalony lub nie i na tej podstawie stwierdzić czy najwyższy bit klucza był zapalony czy tez nie.

Warto zauważyć, że jeśli szyfrując zaczniemy korzystać z przedłużonej części klucza, to najwyższy bit pierwszego przedłużenia to jest 2 bit najbardziej znaczący z oryginalnego klucza, najwyższy bit drugiego przedłużenia to 3 najbardziej znaczący bit oryginalnego klucza etc.

W efekcie jeśli nasz klucz jest przynajmniej 8 razy krótszy niż plaintext możemy w ten sposób odzyskac wszystkie bity klucza.

Ostatnim krokiem było poznanie długości klucza. Wykorzystaliśmy do tego założenie, że klucz jako tekst ascii nie posiada zapalonych wysokich bitów, więc pierwsza pozycja w ciphertexcie, która ma zapalony najwyższy bit określa miejsce gdzie musiał zostać użyty klucz przedłużony. Taka pozycja określa maksymalną długość klucza oryginalnego. Następnie wykonaliśmy operacje ekstrakcji kluczy dla wszystkich wartości pomiędzy 2 a tym indeksem. Używając kodu:

```python
def test(KEY_LEN):
    out = []

    for i in range(len(inp)):
        new = 1 if (ord(inp[i]) & 0x80) != 0 else 0
        out.append(new)

    res = ''
    for i in range(KEY_LEN):
        bits = out[i::KEY_LEN]
        bitstr = ''.join(str(x) for x in bits)
        res += chr(int(bitstr[:8], 2))
    return res
```

Uzyskaliśmy dla długości klucza 21 wartość `weplayctfoutofpassion`. Tą wartość wykorzystaliśmy w oryginalnym skrypcie javascript do zdekodowania wejściowego ciągu:

```javascript
key = "weplayctfoutofpassion";
input = '51136f3b763d7d5e5910106d423f0908093931284bc6eda1a4ffa595c390b390ef89a4a08ffb9797a2b797f5af92b7a0aaac9cf2dbf9ccecd5c8b3cbb9fffefa4fcf0c26d761f9145793fb6a44ed048cb92a1c0f420e3af756d66f2d1ee94414ed335f180b34fca1fda4f9698a23287ca9e9acb2e8b7c0216c132c078c93a438217e0927ce1afbcf016fd7cc6b1f8b903ec3c0a19f723ae5c0fa46679ded50d17259f89688a5ff4340784a155d'
console.log(proceed(input, key, 'decrypt'));
```

Co dało nam:

`Awesome work, you should now have just one left to go unless you selected randomly. I m giving you the flag: 1112fc63b939ab8b22a2b6995ba0be95. Enjoy the rest of the journey!`

### ENG version

The task was to revert given algorithm, implemented in javascript, for given ciphertext. The cipher code was given and is available [here](./crypto300.js).

Ciphertext: `51136f3b763d7d5e5910106d423f0908093931284bc6eda1a4ffa595c390b390ef89a4a08ffb9797a2b797f5af92b7a0aaac9cf2dbf9ccecd5c8b3cbb9fffefa4fcf0c26d761f9145793fb6a44ed048cb92a1c0f420e3af756d66f2d1ee94414ed335f180b34fca1fda4f9698a23287ca9e9acb2e8b7c0216c132c078c93a438217e0927ce1afbcf016fd7cc6b1f8b903ec3c0a19f723ae5c0fa46679ded50d17259f89688a5ff4340784a155d`

The analysis of the code showed us that every byte in the encoded text is a result of XOR operations on 3 values: byte from input, byte from special table with values 0-128 and byte from key.
If the the key was too short, it was extended byt duing a left bitshift, the some more bit operations and in the end it was appended to the original key.
Shifting bits of element of the key in order to get a new element of the key means that for sufficiently large text some bytes will be xored with original key, next bytes with shifted key etc.
Out of those 3 elements xored to get the ciphertext/plaintext only the key could have a lighted higest bit, since when the key was "extended" it was shifting bits to the left. This means that we could check if the higest bit of ciphertext is lighted or not and based on that decide if the highest bit of the key was lighted or not.

It's worth noting that that when we encode the input and start using the extended key part, then highest bit of the first extension is actually the 2nd most significant bit of the original key, highest bit of the 2nd extension is the 3rd most significant bit of the original key etc.

As a result if our key is at least 8 times shorter than he plaintext we can extract all the bits of the key.

The last step was to figure out how long is the key. We used the assumption that te key is ascii text so does not have high bits set to 1, and therefore the first lighted highest bit marks the index at which we must have started using key extension. This means that the key can be at most that long. Then we extracted all potential keys of length from 2 to the index we found, with the code:

```python
def test(KEY_LEN):
    out = []

    for i in range(len(inp)):
        new = 1 if (ord(inp[i]) & 0x80) != 0 else 0
        out.append(new)

    res = ''
    for i in range(KEY_LEN):
        bits = out[i::KEY_LEN]
        bitstr = ''.join(str(x) for x in bits)
        res += chr(int(bitstr[:8], 2))
    return res
```

This way for key length 21 we got `weplayctfoutofpassion`. We used it in the original javascript script to decode the input ciphertext:

```javascript
key = "weplayctfoutofpassion";
input = '51136f3b763d7d5e5910106d423f0908093931284bc6eda1a4ffa595c390b390ef89a4a08ffb9797a2b797f5af92b7a0aaac9cf2dbf9ccecd5c8b3cbb9fffefa4fcf0c26d761f9145793fb6a44ed048cb92a1c0f420e3af756d66f2d1ee94414ed335f180b34fca1fda4f9698a23287ca9e9acb2e8b7c0216c132c078c93a438217e0927ce1afbcf016fd7cc6b1f8b903ec3c0a19f723ae5c0fa46679ded50d17259f89688a5ff4340784a155d'
console.log(proceed(input, key, 'decrypt'));
```

Which gave us:

`Awesome work, you should now have just one left to go unless you selected randomly. I m giving you the flag: 1112fc63b939ab8b22a2b6995ba0be95. Enjoy the rest of the journey!`