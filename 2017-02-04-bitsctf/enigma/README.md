# Enigma (crypto)

```
Its World War II and Germans have been using Enigma to encrypt their messages. Our analysts have figured that they might be using XOR-encryption. XOR-encrption is vulnerable to a known-plaintext attack. Sadly all we have got are the encrypted intercepted messages. Your task is to break the Enigma and get the flag.
```

###ENG
[PL](#pl-version)

In the task we get a set of [ciphertexts](encrypted.tar.xz) to work with.
Initially we thought this is another one of repeating-key-xor and we were using our semi-interactive breaker for it, but it seemed to not work at all - we could not find any words.
Then we decided to look at the data we got, and we saw for example:

```
Dtorouenc&Vguugaoct+Mihpio&dcuenksr|r&dco&06&Atgb&Hitbch&shb&73&Atgb&Qcurch(&Hcnkch&Uoc&cu&ui`itr
```

```
60<56*&Bgu&Qcrrct&our&ncsrc&mjgt(&Tcach&gk&Gdchb
```

What sticks of instantly is how many `&` are there.
It can't be a coincidence so we figured that those have to be spaces and therefore the xor key has to be 1 or 2 characters at most.
We checked and it turned out that it was a single `\6`.

We run:

```python
import codecs
from crypto_commons.generic import chunk_with_remainder, xor_string


def main():
    cts = []
    for i in range(1, 7):
        with codecs.open("encrypted/" + str(i) + "e", "r") as input_file:
            data = input_file.read()
            cts.append(data)
    xored = [xor_string(chr(ord('&') ^ ord(' ')) * len(data), d) for d in cts]
    print(xored)


main()
```

And we get `BITCTF{Focke-Wulf Fw 200}` in one of the messages.

###PL version

W zadaniu dostajemy zestaw [szyfrogramów](encrypted.tar.xz).
Początkowo myśleliśmy, że to kolejna wersja łamania powtarzącego się klucza xor i chcieliśmy użyć naszego semi-interaktywnego łamacza, ale nic ciekawego z tego nie wychodziło - nie mogliśmy znaleźć żadnych sensownych słów.
Postanowiliśmy więc popatrzeć na dane które mamy w plikach:

```
Dtorouenc&Vguugaoct+Mihpio&dcuenksr|r&dco&06&Atgb&Hitbch&shb&73&Atgb&Qcurch(&Hcnkch&Uoc&cu&ui`itr
```

```
60<56*&Bgu&Qcrrct&our&ncsrc&mjgt(&Tcach&gk&Gdchb
```

Co rzuca się od razu w oczy to liczba znaków `&`.
To nie może być przypadek więc założyliśmy, że to mogą być spacje a tym samym klucz xora może mieć co najwyżej 1 lub 2 znaki.
Sprawdziliśmy i okazało sie że kluczem był znak `\6`.

Uruchamiamy:

```python
import codecs
from crypto_commons.generic import chunk_with_remainder, xor_string


def main():
    cts = []
    for i in range(1, 7):
        with codecs.open("encrypted/" + str(i) + "e", "r") as input_file:
            data = input_file.read()
            cts.append(data)
    xored = [xor_string(chr(ord('&') ^ ord(' ')) * len(data), d) for d in cts]
    print(xored)


main()
```

I dostajemy `BITCTF{Focke-Wulf Fw 200}` w jednej z wiadomości.
