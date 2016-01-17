## QR Puzzle: Web (Unknown, 400p)

    Solve the slide puzzle and decode the QR code.
    http://puzzle.quals.seccon.jp:42213/slidepuzzle

###PL
[ENG](#eng-version)

Podobnie jak w poprzednich QR Puzzle dostajemy QR code i mamy go rozwiązać. Tym razem problemem jest to, że brakuje fragmentu kodu.

![](screen.png)

Z czasem zadania robią się coraz trudniejsze - na początku brakuje zawsze prawego dolnego rogu kodu, później również krawędzi, później środka, a na końcu może brakować również innego rogu (co okazało się problematyczne).
Dość oczywisty jest cel zadania - należy napisać program który złoży taki QR code, rozwiąże go, oraz wyśle do programu.

Wykorzystaliśmy do tego solver z poprzedniego zadania QR Puzzle, jedynie nieznacznie musieliśmy przerobić funkcje pobierającą obrazki z ekranu, oraz nie wysyłaliśmy rozwiązań a przeklejaliśmy ręcznie.

Kodu jest za dużo by omawiać go funkcja po funkcji, ale działa prawie identycznie jak w zadaniu [QR puzzle: Windows](https://github.com/p4-team/ctf/tree/master/2015-12-05-seccon/qr_windows_200) - ma jedynie kilka poprawek.

Flaga:

    SECCON{U_R_4_6R347_PR06R4MM3R!}



### ENG version

We are given qr code, and we have to unscramble it - just like in earlier qr puzzle challenge. It's harder now, because there is much more fragments, and one piece is missing.

![](screen.png)

Qr codes are getting harder with time - at the beggining missing piece is always lower right corner, but later we can expect also missing edge, missing central piece, or even missing another corner (worst case scenario).
It's obvious what task authors are expecting from us - we kave to write program that assembles such QR code, solve it, and then sends it to server.

We used our solver from previons challenge - we only had to slightly rework function that captured qr code, and we didn't sent solutions automatically (it had to be done manually).

There is too much code to go through it function by function, but it is almost identical as in [QR puzzle: Windows](https://github.com/p4-team/ctf/tree/master/2015-12-05-seccon/qr_windows_200) challenge - we only fixed few minor things.

Flag:

    SECCON{U_R_4_6R347_PR06R4MM3R!}
