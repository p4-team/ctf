##CatchMeIfYouCan (Forensics, 100p)

	We got this log which is highly compressed. Find the intruder's secret.

###PL
[ENG](#eng-version)

Plik f100 jest pewnego rodzaju Matryoshką kompresyjną, plik trzeba kolejno rozkompresowywać różnymi mniej i bardziej znanymi formatami. Po chwili okazuje się, że plik jest dosyć "głęboki" i trzeba będzie zautomatyzować rozpakowywanie kolejnych warstw. 

[Program](decode.py) jest dosyć prosty w działaniu, sprawdzamy format pliku za pomocą komendy `file`, a następnie rozpakowywujemy go odpowiednim programem. 

Ostatnim folderem jest f100.rar z którego dostajemy 2 foldery "log" i "dl" pełne różnych logów i list linków. Jak już dostatecznie dużo czasu zmarnujemy na przeszukiwanie śmieci to natrafiamy na ciekawy link: https://gist.github.com/anonymous/ac2ce167c3d2c1170efe z tajemniczym stringiem: 

`$=~[];$={___:++$,$$$$:(![]+"")[$],__$:++...` [całość](mysteriousString.txt)

...który okazuje się javascriptowym skryptem printującym flagę: 

`-s-e-c-r-e-t-f-l-a-g-{D-i-d-Y-o-u-R-e-a-l-l-y-F-i-n-d-M-e-}`

###ENG version
