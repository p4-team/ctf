# Eva’s chance (crypto 150)


## ENG
[PL](#pl-version)

We get [cipher code](encryptor.c), [encrypted message](message.txt), and we know that plaintext starts with `Hello, Alice!`.

We're really only interested in the part:

```c
void encrypt(uint8_t * buffer, uint32_t lfsr, uint32_t poly, unsigned int length)
{
    for(uint32_t i = 0; i != length; i++)
    {
        for(uint8_t j = 7;; j--)
        {
            unsigned char lsb = lfsr & 1;
            buffer[i] ^= lsb<<j;
            lfsr >>= 1;
            if (lsb)
                lfsr ^= poly;
            if (j == 0) break;
        }
    }
}
```

For each byte of the message we xor `i`-th bit of `lfsr` with `7-i`-th bit of the message byte.
Along the encryption the value of `lfsr` is being shifted right, and each time we use bit `1` we xor `lfsr` with `poly` value.

It's worth noting that this function is both encrypt and decrypt, because for identical input values `lfsr` and `poly` we will xor with exactly the same bit values, and therefore it will invert itself.

Seems a bit complicated, but we know some initial bytes of plaintext, so we can easily recover the first bits we were xoring with.
So we know the `lsb` values for those initial bytes.
This also means we know when `lfsr ^= poly` was done.

Working with this by hand would be tedious, so we decided to pass this to Z3.

We simply re-write the encrypt function:

```python
    lfsr = z3.BitVec('x', 32)
    x = lfsr
    poly = z3.BitVec('y', 32)
    y = poly
    s = Solver()
    for i in range(len(known_plaintext_part)):
        for j in range(7, -1, -1):
            lsb = ((ord(known_plaintext_part[i]) ^ ord(ciphertext[i])) & (1 << j)) >> j
            s.add(lfsr & 1 == lsb)
            lfsr = LShR(lfsr, 1)
            if lsb:
                lfsr ^= poly
    print(s.check())
    return int(str(s.model()[x])), int(str(s.model()[y]))
```

We proceed with the function recovering the `lsb` values for known plaintext part and we extend the constraints for our parameters.

We spent additional hour debugging this because of `lfsr =>> 1` and `LShR(lfsr, 1)`.
It seems Z3 treats `>>` as `signed` operation even for bit vectors and we have to force using `LShR` (logical shift right) to get what we wanted.

From the solver we get the parameters values: `(2463678191, 464384013)`

Whole solver [here](eve.py)

With decrypted data we get the flag: `h4ck1t{madskillz_crypt0}`

## PL version

W zadaniu dostajemy [kod szyfrowania](encryptor.c), [szyfrogram](message.txt) i wiemy że plaintext zaczyna się od `Hello, Alice!`.

Jedyna interesująca część to:

```c
void encrypt(uint8_t * buffer, uint32_t lfsr, uint32_t poly, unsigned int length)
{
    for(uint32_t i = 0; i != length; i++)
    {
        for(uint8_t j = 7;; j--)
        {
            unsigned char lsb = lfsr & 1;
            buffer[i] ^= lsb<<j;
            lfsr >>= 1;
            if (lsb)
                lfsr ^= poly;
            if (j == 0) break;
        }
    }
}
```

Dla każdego bajtu wiadomości xorujemy `i`-ty bit zmiennej `lfsr` z `7-i`-tym bitem bajtu wiadomości.
W trakcie działania szyfrowania wartość zmiennej `lfsr` jest przeuswana o kolejne bity w prawo a za każdym razem gdy użyjemy bitu `1` xorujemy wartość `lfsr` z `poly`.

Warto zauważyć, że podana funkcja jest zarówno szyfrowaniem jak i deszyfrowaniem, bo dla takich samych wartości `lfsr` i `poly` będziemy xorować z takimi samymi wartościami bitów, więc szyfr sam się odwróci.

Wydaje się to dość złożone, ale znamy pierwsze bajty plaintextu, więc możemy łatwo odzyskać wartości bitów `lsb` z którymi xorowano wiadomość.
Wiemy też oczywiście kiedy następowały operacje `lfsr ^= poly`.

Odwracanie tego ręcznie byłoby dość żmudne, więc korzystamy tu z Z3.

Przepisaliśmy po prostu funkcje szyfrującą:

```python
    lfsr = z3.BitVec('x', 32)
    x = lfsr
    poly = z3.BitVec('y', 32)
    y = poly
    s = Solver()
    for i in range(len(known_plaintext_part)):
        for j in range(7, -1, -1):
            lsb = ((ord(known_plaintext_part[i]) ^ ord(ciphertext[i])) & (1 << j)) >> j
            s.add(lfsr & 1 == lsb)
            lfsr = LShR(lfsr, 1)
            if lsb:
                lfsr ^= poly
    print(s.check())
    return int(str(s.model()[x])), int(str(s.model()[y]))
```

Odzyskujemy znane wartości `lsb` dla znanego plaintextu i dodajemy te informacje jako ograniczenia na parametry.

Spędziliśmy dodatkową godzinę debugując skrypt przez `lfsr =>> 1` i `LShR(lfsr, 1)`
Okazuje się że dla Z3 `>>` to operacja `signed` nawet dla bit vectorów i musimy wymusić użycie funkcji `LShR` (logical shift right) żeby dostać to czego się spodziewaliśmy.

Solver odzyskuje dla nas wartości: `(2463678191, 464384013)`

Cały kod [tutaj](eve.py)

Uruchamiamy funkcje szyfrującą/deszyfrujacą z powyższymi parametrami i dostajemy: `h4ck1t{madskillz_crypt0}`
