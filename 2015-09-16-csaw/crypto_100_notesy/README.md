## Notesy (crypto, 100p, 1064 solves)
`http://54.152.6.70/
The flag is not in the flag{} format.
HINT: If you have the ability to encrypt and decrypt, what do you think the flag is?
HINT: https://www.youtube.com/watch?v=68BjP5f0ccE`

Pod wskazanym adresem znajduje się strona z textboxem który szyfruje wpisany text.

![](./notesy.png)

Już wiecie co jest flagą? My też nie wiedzieliśmy jak ją wydobyć… przez 20 godzin… trzymając ją w rękach….

Strona robiła zapytanie get do skryptu encrypt.php, który jako parametr m przyjmował wiadomość do zaszyfrowania.

Już po godzinie stwierdziliśmy, że zależność między literkami przedstawia się następująco

```
ABCDEFGHIJKLMNOPQRSTUVWXYZ
UNHMAQWZIDYPRCJKBGVSLOETXF
```

Próbowaliśmy naprawdę nieschematycznego myślenia ale nic nie pomogło. Dopiero pierwsza wskazówka przyniosła nam myśl, że flagą musi być klucz, a z racji, że to szyfr przestawieniowy kluczem będzie `UNHMAQWZIDYPRCJKBGVSLOETXF`. Najbardziej fustrujące zadanie z jakim się ostatnio spotkałem.
