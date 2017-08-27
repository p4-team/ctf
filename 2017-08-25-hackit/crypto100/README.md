# 4_messages (crypto 100)


## ENG
[PL](#pl-version)

In the task we get [4 Playfair ciphertexts](captured.log) and we know that the plaintext starts with `Good evening hackit two thousand seventeen`.

We actually approached this in a bit unconventional way, since the first attack we found was a heuristic to recover message from a single ciphertext with no plaintext known at all described here: http://practicalcryptography.com/cryptanalysis/stochastic-searching/cryptanalysis-playfair/

So we simply proceed with this and recover plaintexts within seconds:

```
GOOD EVENING HACKIT TWO THOUSAND SEVENTEEN IN THIS TINY BROCURE WE WOULD LIKE TO DESCRIBE HOW IT IS TO BE A PLAYFAIR CRYPTOR NO DOUBT IT IS EASY AS HECK BUT YOU GOT TO HAVE A PIECE OF PAPER ALL THE TIME WE BET THERE IS NO CONVINIENCE NOW LETS CUT THE SHIT RESTORE THE MATRIX KEYS FOR EACH CIPHERTEXT THEN TAKE FIRST SIX LETTERS THEN COMBINE THEM TO GET HER AND YOU WILL GET THE FLAG
```

And the matrix keys:

```
TBDEFGLMNOPQRSUVWXYZHACKI
WXZTUVERISBCDYAHKLFGOPQMN
NGEDACFHRBLMOIKSTUPQXYZVW
UVWXZCRYPTOABDEFGHIKLMNQS
```

Now with some luck, guessing and 5x5 matrix column/row shifts we figure out the codewords:

```
hackit
isvery
danger
crypto
```

So the flag is: `h4ck1t{hackitisverydangercrypto}`

## PL version

W zadaniu dostajemy [4 szyfrogramy Playfair](captured.log) i wiemy że plaintext zaczyna się od `Good evening hackit two thousand seventeen`.

Podeszliśmy do tego zadania trochę niekonwencjonalnie, bo pierwszy atak na który trafiliśmy to była heurystyka do odzyskiwania wiadomości na podstawie jednego szyfrogramu bez żadnej znajomości plaintextu opisana tutaj: http://practicalcryptography.com/cryptanalysis/stochastic-searching/cryptanalysis-playfair/

Uruchomiliśmy więc solver i w kilka sekund odzyskaliśmy wiadomości:

```
GOOD EVENING HACKIT TWO THOUSAND SEVENTEEN IN THIS TINY BROCURE WE WOULD LIKE TO DESCRIBE HOW IT IS TO BE A PLAYFAIR CRYPTOR NO DOUBT IT IS EASY AS HECK BUT YOU GOT TO HAVE A PIECE OF PAPER ALL THE TIME WE BET THERE IS NO CONVINIENCE NOW LETS CUT THE SHIT RESTORE THE MATRIX KEYS FOR EACH CIPHERTEXT THEN TAKE FIRST SIX LETTERS THEN COMBINE THEM TO GET HER AND YOU WILL GET THE FLAG
```

I klucze:

```
TBDEFGLMNOPQRSUVWXYZHACKI
WXZTUVERISBCDYAHKLFGOPQMN
NGEDACFHRBLMOIKSTUPQXYZVW
UVWXZCRYPTOABDEFGHIKLMNQS
```

Dalej przy odrobinie szczęścia, zgadywania i przesuwania kolumn/wierszy macierzy 5x5 dostajemy:

```
hackit
isvery
danger
crypto
```

Więc flaga to: `h4ck1t{hackitisverydangercrypto}`
