##CatchMeIfYouCan (Forensics, 100p)

	We got this log which is highly compressed. Find the intruder's secret.

###PL
[ENG](#eng-version)

Plik f100 jest pewnego rodzaju Matryoshką kompresyjną, plik trzeba kolejno rozkompresowywać różnymi mniej i bardziej znanymi formatami. Po chwili okazuje się, że plik jest dosyć "głęboki" i trzeba będzie zautomatyzować rozpakowywanie kolejnych warstw. 

[Program](decode.py) jest dosyć prosty w działaniu, sprawdzamy format pliku za pomocą komendy `file`, a następnie rozpakowywujemy go odpowiednim programem. 

Ostatnim folderem jest f100.rar z którego dostajemy 2 foldery "log" i "dl" pełne różnych logów i list linków. Jak już dostatecznie dużo czasu zmarnujemy na przeszukiwanie śmieci to natrafiamy na ciekawy link: https://gist.github.com/anonymous/ac2ce167c3d2c1170efe z tajemniczym stringiem: 

`$=~[];$={___:++$,$$$$:(![]+"")[$],__$:++`... [całość](mysteriousString.txt)

...który okazuje się javascriptowym skryptem printującym flagę: 

`-s-e-c-r-e-t-f-l-a-g-{D-i-d-Y-o-u-R-e-a-l-l-y-F-i-n-d-M-e-}`

###ENG version

File f100 is sort of a Matryoshka-compression-doll, we have to decompress each file to get to another one. After a while of tinkering with it manually, it appears that the file is quite deep and we're going to need to automatize the process.

[Program](decode.py) is pretty straight forward, we check the file's format using `file` and then decompress it using appropriate algorithm/program.

The last folder we get is f100.rar which contains 2 folders "log" and "dl" full of different logs and links. After a *while* of searching, we stubmle into an interesting link: https://gist.github.com/anonymous/ac2ce167c3d2c1170efe with a mysterious string:

`$=~[];$={___:++$,$$$$:(![]+"")[$],__$:++`... [full](mysteriousString.txt)

...which appears to be a javascript program that prints the flag:

`-s-e-c-r-e-t-f-l-a-g-{D-i-d-Y-o-u-R-e-a-l-l-y-F-i-n-d-M-e-}`
