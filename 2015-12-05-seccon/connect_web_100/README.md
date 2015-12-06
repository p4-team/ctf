##Connect the server (Web/Network, 100p)

```
login.pwn.seccon.jp:10000
```

###PL
[ENG](#eng-version)

Po połączeniu się z serwerem za pomocą nc dostajemy:

![](connection.png)

Wpisanie dowolnego loginu także nie daje żadnych efektów. Próbowaliśmy podejść do tego zadania z różnych stron, bez efektów. W końcu uznaliśmy, że skoro zadanie wspomina o wolnym połączeniu to może spróbujemy ataku czasowego albo próby wyczerpania wątków serwera. Jednak w trakcie pisania skryptu zauważyliśmy dość dziwny wynik:

```
b'CONNECT 300\r\n\r\nWelcome to SECCON server.\r\n\r\nThe server is connected via slow dial-up connection.\r\nPlease be patient, and do not brute-force.\r\nS\x08 \x08E\x08 \x08C\x08 \x08C\x08 \x08O\x08 \x08N\x08 \x08{\x08 \x08S\x08 \x08o\x08 \x08m\x08 \x08e\x08 \x08t\x08 \x08i\x08 \x08m\x08 \x08e\x08 \x08s\x08 \x08_\x08 \x08w\x08 \x08h\x08 \x08a\x08 \x08t\x08 \x08_\x08 \x08y\x08 \x08o\x08 \x08u\x08 \x08_\x08 \x08s\x08 \x08e\x08 \x08e\x08 \x08_\x08 \x08i\x08 \x08s\x08 \x08_\x08 \x08N\x08 \x08O\x08 \x08T\x08 \x08_\x08 \x08w\x08 \x08h\x08 \x08a\x08 \x08t\x08 \x08_\x08 \x08y\x08 \x08o\x08 \x08u\x08 \x08_\x08 \x08g\x08 \x08e\x08 \x08t\x08 \x08}\x08 \x08\r\nlogin: '
```

Naszą uwagę zwróciły niepiśmienne znaki o numerze ascii 8, czyli backspace. Otóż serwer wypisywał flagę, ale było to niewidoczne w konsoli.

`SECCON{Sometimes_what_you_see_is_NOT_what_you_get}`

### ENG version

After connecting with nc we get:

![](connection.png)

Using any login doesn't help us moving forward with the task. We tried different approaches but to no avail. Finally we decided that, since the task mentions and weak slow connection, we could try a timing attack or try to exhaust server threads. However, while writing a script we noticed a strange data coming from server:

```
b'CONNECT 300\r\n\r\nWelcome to SECCON server.\r\n\r\nThe server is connected via slow dial-up connection.\r\nPlease be patient, and do not brute-force.\r\nS\x08 \x08E\x08 \x08C\x08 \x08C\x08 \x08O\x08 \x08N\x08 \x08{\x08 \x08S\x08 \x08o\x08 \x08m\x08 \x08e\x08 \x08t\x08 \x08i\x08 \x08m\x08 \x08e\x08 \x08s\x08 \x08_\x08 \x08w\x08 \x08h\x08 \x08a\x08 \x08t\x08 \x08_\x08 \x08y\x08 \x08o\x08 \x08u\x08 \x08_\x08 \x08s\x08 \x08e\x08 \x08e\x08 \x08_\x08 \x08i\x08 \x08s\x08 \x08_\x08 \x08N\x08 \x08O\x08 \x08T\x08 \x08_\x08 \x08w\x08 \x08h\x08 \x08a\x08 \x08t\x08 \x08_\x08 \x08y\x08 \x08o\x08 \x08u\x08 \x08_\x08 \x08g\x08 \x08e\x08 \x08t\x08 \x08}\x08 \x08\r\nlogin: '
```

We focused on the acii characters number 8 - backspace. The server was printing a flag but we simply didn't see that in the console.

`SECCON{Sometimes_what_you_see_is_NOT_what_you_get}`