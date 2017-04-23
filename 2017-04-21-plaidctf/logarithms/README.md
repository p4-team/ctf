# Logarithms are hard (misc, 10p)

## ENG
[PL](#pl-version)

```
What is e^(1.000000001)?
Please enter in decimal with 7 places.
(For example, if the answer was 2.71828183... the flag would be 2.7182818 )
```

As in previous editions of Plaid CTF we have a misc task regarding some bug in numerical computation.
This time it is calculation is exponent function.
Quick googling gets us to: http://www.datamath.org/Story/LogarithmBug.htm which says that some calculators would get the result wrong and instead of `2.7182818` give `2.7191928`.
We submit the latter as a flag and get 10 points.

## PL version

```
What is e^(1.000000001)?
Please enter in decimal with 7 places.
(For example, if the answer was 2.71828183... the flag would be 2.7182818 )
```

Tak jak w poprzednich edycjach Plajd CTF mamy zadanie związane z błędami w obliczeniach numerycznych.
W tym przypadku chodzi o eksponente.
Szybkie googlowanie pozwala nam trafić na http://www.datamath.org/Story/LogarithmBug.htm gdzie możemy wyczytać, że niektóre kalkulatory zamiast `2.7182818` dawały wynik `2.7191928`.
Wysyłamy niepoprawną wartość jako flagę i dostajemy 10p.
