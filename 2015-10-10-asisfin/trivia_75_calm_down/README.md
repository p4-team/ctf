## Which one is flag? (trivia, 75p, 89 solves)

> Which one is [flag](flagBag.zip)?

### PL
[ENG](#eng-version)

Otrzymujemy plik tekstowy z prawie 300 tysiącami flag. Jednak pierwsze co rzuca się w oczy to po jednym null byte na wiersz.

![](img1.png)

Sprawdzamy ile tych null byte-ów jest: okazuje się, że o jeden mniej niż wszystkich flag. Znajdźmy więc flagę bez niego - najpierw usuwamy wszystkie znaki w każdym z wierszy od nullbyte'a: `\x00.+`, a następnie szukamy znaku `}`. Pozostał tylko jeden - we fladze:

`ASIS{dc99999733dd1f4ebf8c199753c05595}`
