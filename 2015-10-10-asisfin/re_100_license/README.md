## License 100 (re, 100p)

### PL
[ENG](#eng-version)

Dostajemy [program](./license) (elf), do analizy, i rozpoczynamy czytanie kodu.

Program otwiera plik (domyślamy sie że z tytułową licencją), wykonuje serię operacji/sprawdzeń, i jeśli coś mu się nie podoba na którymś kroku, wypisuje błąd i skończy działanie.

    .text:00000000004009C7                 mov     edi, offset a_aBC_ ; "_a\nb\tc_"
    ...
    .text:00000000004009EE                 call    _fopen

Jak widać, nazwa pliku jest dość nietypowa. Nie jest to nic czego linux nie osiągnie, ale praca z plikiem o takiej nazwie jest dość nieprzyjemna. Z tego powodu plik nazwaliśmy "kot" i spatchowaliśmy binarkę z programem (tak że otwierał plik o nazwie "kot").

Pierwszy check - jeśli otworzenie pliku albo czytanie z niego się nie powiedzie, program kończy działanie.

Drugi check - wykonywana jest skomplikowana operacja na długości pliku, która po chwili reversowania sprowadza się do:

    if (-45235*x*x*x*x + -1256*x*x*x + 14392*x*x + -59762*x - 1949670109068 + 44242*x*x*x*x*x == 0) {
        // ok
    } else {
        // koniec programu
    } 

Gdzie x to ilość bajtów w pliku licencji. 
W celu rozwiązania tego równania pytamy naszego niezastąpionego pomocnika, WolframAlpha. Rozwiązaniem jest x = 34.

Następnie następuje długa pętla dzieląca plik wejściowy na linie i zliczająca znaki nowej linii, a później:

    if (linesInFile == 5) {
        // ok
    } else {
        // koniec programu
    }

Jako że wszystkie linie mają taką samą długość (co można zaobserwować w kodzie), Można z tego łatwo wyliczyć że każda linia musi mieć 6 znaków (6 * 5 znaków w linii + 4 znaki '\n')

Następnie następuje długie sprawdzenie, w pythonie wyglądałoby na przykład tak (word1, word2... to odpowiednio pierwsza, druga... linia z pliku)

    result = 'iKWoZLVc4LTyGrCRedPhfEnihgyGxWrCGjvi37pnPGh2f1DJKEcQZMDlVvZpEHHzUfd4VvlMzRDINqBk;1srRfRvvUW' # stała zaszyta w programie
    w23 = '\x23\x23\x23\x23\x23\x23'
    level1 = result[0:n]
    level2 = result[n:2*n]
    level3 = result[2*n:3*n]
    level5 = result[3*n:4*n]
    level4 = xor(word3, level5)

    assert level1 == xor(word1, word2)
    assert level2 == xor(xor(word2, word4), w23)
    assert level3 == xor(word3, word4)
    assert level4 == xor(xor(word5, word4), w23)
    assert level5 == xor(level4, word3)

Wszystkie operacje tutaj są odwracalne, więc po chwili mamy kod tworzący poprawny plik z licencją:

    level1 = result[0:n]
    level2 = result[n:2*n]
    level3 = result[2*n:3*n]
    level5 = result[3*n:4*n]

    w23 = '\x23\x23\x23\x23\x23\x23'
    word4 = result[4*n:5*n]
    word3 = xor(word4, level3)
    word2 = xor(xor(word4, w23), level2)
    word1 = xor(word2, level1)
    level4 = xor(word3, level5)
    word5 = xor(xor(word4, w23), level4)

    # check
    level1c = xor(word1, word2)
    level2c = xor(xor(word2, word4), w23)
    level3c = xor(word3, word4)
    level4c = xor(xor(word5, word4), w23)
    level5c = xor(level4c, word3)

    assert level1.encode('hex') == level1c.encode('hex')
    assert level2.encode('hex') == level2c.encode('hex')
    assert level3.encode('hex') == level3c.encode('hex')
    assert level4.encode('hex') == level4c.encode('hex')
    assert level5.encode('hex') == level5c.encode('hex')

    open('kot', 'wb').write('\n'.join([word1, word2, word3, word4, word5]))

Uruchamiamy więc program z odpowiednią [licencją](kot), i...

    vagrant@precise64:~$ ./license
    program successfully registered to ASIS{8d2cc30143831881f94cb05dcf0b83e0}

gotowe.

### ENG version

We get a [program](./license) (elf) for analysis and we start to read the code.

It opens a file (we expect this to be the "licence" from task title), executs a series of operations/checks and if something is wrong at one step it prints an error and exits.

    .text:00000000004009C7                 mov     edi, offset a_aBC_ ; "_a\nb\tc_"
    ...
    .text:00000000004009EE                 call    _fopen

As we can see the filename is not ordinary. While we could get this done on linux, we consider working with such file to be unpleasant. Therefore we named the file `kot` and we patched the binary (so it opens a file `kot`).

First check - if opening the file or reading it fails, the program exits.

Second check - a complex operation is performed on the file length, which after a while of reverse engineering turned out to be:

    if (-45235*x*x*x*x + -1256*x*x*x + 14392*x*x + -59762*x - 1949670109068 + 44242*x*x*x*x*x == 0) {
        // ok
    } else {
        // exit
    } 

Where x is number of bytes in the licence file.
In order to solve this equation we use WolframAlpha and we get x = 34.

Next there is a long loop which splits the input file into lines and counts newline characters and then:

    if (linesInFile == 5) {
        // ok
    } else {
        // exit
    }

Every line has the same length (which can be observed in the code), we can deduce that every line needs 6 characters (6*5 characters in line + 4 newline characters = 34 bytes in file).

Next there is a long check which in python would look like (word1, word2... is first, second.... line from file)

    result = 'iKWoZLVc4LTyGrCRedPhfEnihgyGxWrCGjvi37pnPGh2f1DJKEcQZMDlVvZpEHHzUfd4VvlMzRDINqBk;1srRfRvvUW' # stała zaszyta w programie
    w23 = '\x23\x23\x23\x23\x23\x23'
    level1 = result[0:n]
    level2 = result[n:2*n]
    level3 = result[2*n:3*n]
    level5 = result[3*n:4*n]
    level4 = xor(word3, level5)

    assert level1 == xor(word1, word2)
    assert level2 == xor(xor(word2, word4), w23)
    assert level3 == xor(word3, word4)
    assert level4 == xor(xor(word5, word4), w23)
    assert level5 == xor(level4, word3)

All operations are reversible so after a while we have code to generate correct licence file:

    level1 = result[0:n]
    level2 = result[n:2*n]
    level3 = result[2*n:3*n]
    level5 = result[3*n:4*n]

    w23 = '\x23\x23\x23\x23\x23\x23'
    word4 = result[4*n:5*n]
    word3 = xor(word4, level3)
    word2 = xor(xor(word4, w23), level2)
    word1 = xor(word2, level1)
    level4 = xor(word3, level5)
    word5 = xor(xor(word4, w23), level4)

    # check
    level1c = xor(word1, word2)
    level2c = xor(xor(word2, word4), w23)
    level3c = xor(word3, word4)
    level4c = xor(xor(word5, word4), w23)
    level5c = xor(level4c, word3)

    assert level1.encode('hex') == level1c.encode('hex')
    assert level2.encode('hex') == level2c.encode('hex')
    assert level3.encode('hex') == level3c.encode('hex')
    assert level4.encode('hex') == level4c.encode('hex')
    assert level5.encode('hex') == level5c.encode('hex')

    open('kot', 'wb').write('\n'.join([word1, word2, word3, word4, word5]))

We run the binary with correct [licence](kot), and...

    vagrant@precise64:~$ ./license
    program successfully registered to ASIS{8d2cc30143831881f94cb05dcf0b83e0}

Done.