# b4s1[4l (Misc 150)

```
Dive into this, it's a terrorist transmission, they can't know too much about encoding &|| cryptography. 
It was sent hundreds of times to all their supporters. We really think it s actually the same message.
https://dctf.def.camp/b4s1.php

Hint1: "What is normal in the challenge title?"
Hint 2: strrev(strtoupper($title)) 
```


###ENG
[PL](#pl-version)

In the task we have access to webpage with 6 lines of 16 byte strings:

```
fw[TqCTfDCoXnEpO
HsQd^DnInc}_tVeG
FyIG`ebzDcE\sM{X
fIivqEmcJo_snC\b
TaYNwORnfgoFdRRc
RukE\zEEPegOVu@h
```

Each time you refresh the page the strings change.
Even before the hints were posted we did bitwise analysis of the data on the page and it seemed that in our sample of a few hundred strings there was a regularity: the least significant bit of each byte was constant.

So we extracted those bits and tried to decode this in every way possible (by column, by row, inverted, as 6,7,8 bit bytes, xored etc.), failing.
But after admins spoke to some teams about the task, they figured that they made a mistake...

After the task was `fixed` it turned out that the solution was as simple as treating each 8 bits as a ascii byte, and translating the message to `leastnotlast`.


###PL version

W zadaniu dostajemy dostęp do strony internetowej na której wyświetlane jest 6 linii tekstu po 16 bajtów w linii:

```
fw[TqCTfDCoXnEpO
HsQd^DnInc}_tVeG
FyIG`ebzDcE\sM{X
fIivqEmcJo_snC\b
TaYNwORnfgoFdRRc
RukE\zEEPegOVu@h
```

Za każdym refreshem stringi na stronie są inne.
Jeszcze zanim pojawiły się hinty przeprowadziliśmy analizę bitów stringów na stronie, na próbce kilkuset różnych zestawów, i widać było regularność: niski bit każdego bajtu był stały.

Wyciągnęliśmy powtarzające się bity i próbowaliśmy dekodować je na wszystkie sposoby (po kolumnie, po wierszu, odwrócone, jako 6,7,8 bitowe bajty, xorowane itd), ale bez efektów.
Jakiś czas później admini przeprowadzili wywiad wśród kilku drużyn i zrozumieli że pomylili się w zadaniu...

Po tym jak zadanie zostało `naprawione` rozwiązaniem okazało się po prostu potraktowanie każdych 8 bitów jako bajtu ascii co dało wiadomość `leastnotlast`.
