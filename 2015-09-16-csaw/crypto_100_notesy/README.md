## Notesy (crypto, 100p, 1064 solves)
`http://54.152.6.70/
The flag is not in the flag{} format.
HINT: If you have the ability to encrypt and decrypt, what do you think the flag is?
HINT: https://www.youtube.com/watch?v=68BjP5f0ccE`

### PL Version
`for ENG version scroll down`

Pod wskazanym adresem znajduje się strona z textboxem, który szyfruje wpisany text.

![](./notesy.png)

Strona robiła zapytanie GET do skryptu encrypt.php, który jako parametr m przyjmował wiadomość do zaszyfrowania. Placeholder w tekst boksie brzmiał `Give me like a note dude`, javascript odmawiał szyfrowania wiadomości krótszych niż 5 znaków. Próbowaliśmy na prawdę różnych rzeczy, wysyłania wiadomości bardzo krótkich i bardzo długich.

Już wiecie co jest flagą? My też nie wiedzieliśmy jak ją wydobyć… przez 20 godzin… trzymając ją w rękach…


Już po godzinie od rozpoczęcia konkursu (nie wiemy kiedy zabraliśmy sie za to zadanie) stwierdziliśmy, że zależność między literkami przedstawia się następująco

```
ABCDEFGHIJKLMNOPQRSTUVWXYZ
UNHMAQWZIDYPRCJKBGVSLOETXF
```

Próbowaliśmy naprawdę nieschematycznego myślenia, ale nic nie pomogło. Dopiero pierwsza wskazówka przyniosła nam myśl, że flagą musi być klucz, a z racji, że to szyfr podstawieniowy kluczem będzie `UNHMAQWZIDYPRCJKBGVSLOETXF`. Najbardziej frustrujące zadanie z jakim się ostatnio spotkaliśmy.

### ENG Version

We are given a web page textbox, that encrypts entered messages.

![](./notesy.png)

The page made GET request to php script encrypt.php, passing our message as m parameter. Placeholder on the main site was `Give me like a note dude`, javascript refuses to encrypt messages shorter than 5 characters. We have tried wide range of various attempts: sending short messages directly to php script, really long messages, but nothing succeeded.

Do you know now what the flag is? We didn't for about 20 hours… right in front of our eyes…

Just an hour after the contest began (we don't know exact time of starting our attempts to solve the task), we've noticed that dependency between letters is as follows:

```
ABCDEFGHIJKLMNOPQRSTUVWXYZ
UNHMAQWZIDYPRCJKBGVSLOETXF
```
We tried to think really out of the box, but that didn't help much. The hint helped us a lot (If you have the ability to encrypt and decrypt, what do you think the flag is?) it became clear that the flag is the cipher's key. But because this was substitution cipher, there was no key per se. So flag could only be `UNHMAQWZIDYPRCJKBGVSLOETXF`. This had to be the most frustrating challenge we have faced since a very long time.
