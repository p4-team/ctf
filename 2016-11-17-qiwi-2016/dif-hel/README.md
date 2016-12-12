# Diffie-Hellman 1 (crypto 300)

###ENG
[PL](#pl-version)

In the task we want to generate a shared secret via Diffie Hellman protocol.
We have 3 participants, but we know all the parameters only for 2 of them.
We are given:

```
p = 8986158661930085086019708402870402191114171745913160469454315876556947370642799226714405016920875594030192024506376929926694545081888689821796050434591251
g = 6
gc =  5361617800833598741530924081762225477418277010142022622731688158297759621329407070985497917078988781448889947074350694220209769840915705739528359582454617 # g^c mod p
a = 230
b = 250
```

So we know the secret values for participants `a` and `b` but for participant `c` we know only the public part of his secret - `g^c mod p`.
Forunately this is all we need to establish the shared key.
After all this is how it's done in real life - everyone gets only this public secret.

The shared secret is simply `g^abc mod p`, and for this we don't need `c` if we already have `g^c mod p`:


```python
secret = pow(pow(gc, a, p), b, p)
```

And the first 20 characters are the flag: ```38058349620867258480```
###PL version

W zadaniu chcemy wygenerować wspólny klucz za pomocą protokołu Diffiego Hellmana.
Mamy 3 uczestników ale znamy wszystkie parametry tylko dla 2 z nich.
Znamy:

```
p = 8986158661930085086019708402870402191114171745913160469454315876556947370642799226714405016920875594030192024506376929926694545081888689821796050434591251
g = 6
gc =  5361617800833598741530924081762225477418277010142022622731688158297759621329407070985497917078988781448889947074350694220209769840915705739528359582454617 # g^c mod p
a = 230
b = 250
```

Więc mamy sekretne wartości dla uczestników `a` oraz `b` ale dla `c` znamy tylko publiczną cześć jego sekretu - `g^c mod p`.
Szczęśliwie to jest wszystko co potrzebujemy aby ustanowić wspólny klucz.
Generalnie tak przebiega to w prawdziwym życiu - każdy inny uczestnik zna tylko publiczny sekret.

Wspólny sekret to po prostu: `g^abc mod p`, a do tego nie potrzeba nam wartości `c` jeśli znamy już `g^c mod p`:

```python
secret = pow(pow(gc, a, p), b, p)
```

I pierwsze 20 znaków daje flage: ```38058349620867258480```
