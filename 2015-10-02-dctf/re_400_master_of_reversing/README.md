## Reverse 400 (re, 400p)

### PL
[ENG](#eng-version)

Najtrudniejsze zadanie z RE na tym CTFie. Dostajemy [program](./r400) (znowu elf), który pobiera od usera hasło. Domyślamy się że to hasło jest flagą.

Tutaj niespodzianka, bo hasło nie jest sprawdzane nigdzie w programie. Po chwili grzebania/debugowania, okazuje się, że hasło jest zamieniane na DWORD (cztery znaki) i pewna tablica bajtów jest "deszyfrowana" (tzn. xorowana) z nim, a następnie wykonywana. Xorowane dane wyglądają tak:

    5E 68 0E 59 46 06 47 5E 55 11 15 41 5C 0A 03 16
    44 0A 08 52 14 16 0E 16 52 0D 13 5E 14 3B 09 43
    5C 0D 08 45 15 0A 0A 57 40 0B 0E 44 55 16 13 5E
    77 0D 08 51 8E 48 66 36 34 EB 87 8D 35 62 66 36
    8C 66 66 36 34 AF E6 8E 35 62 66 36 F9 E2 F6 A6

Pierwsze próby zgadnięcia hasła nie udały się (myśleliśmy że może ten fragment to funkcja, i zacznie się jakimś klasycznym prologiem). Ale szybko wpadliśmy na lepszy pomysł. Otóż jaki jest najczęściej spotykany bajt w kodzie? Oczywiście zero. Więc jeśli znajdziemy najczęściej występujący bajt w zaszyfrowanym fragmencie, będziemy wiedzieli że prawdopodobnie były to oryginalnie zera. Kod wyszukujący najczęstsze bajty:

    source = '5E680E594606475E551115415C0A0316440A085214160E16520D135E143B09435C0D0845150A0A57400B0E445516135E770D08518E48663634EB878D356266368C66663634AFE68E35626636F9E2F6A6'.decode('hex')
    prologue = '554889E5'.decode('hex')

    def xor(a, b):
        return ''.join(chr(ord(ac) ^ ord(bc)) for ac, bc in zip(a, b))

    print xor(source, prologue).encode('hex')

    a0 = source[0::4]
    a1 = source[1::4]
    a2 = source[2::4]
    a3 = source[3::4]

    def most_common(x):
        import collections
        s = collections.Counter(x).most_common(1)[0]
        return (s[0].encode('hex'), s[1])

    print most_common(a0),
    print most_common(a1),
    print most_common(a2),
    print most_common(a3),

Okazało się to być strzałem w dziesiątkę! (Jeśli dobrze pamiętamy, jeden z czterech fragmentów źle trafił, ale udało się to już ręcznie poprawić trywialnie).

W ten sposób rozwiązaliśmy najtrudniejsze zadanie RE na CTFie i zdobyliśmy kolejną flagę, wartą 400 punktów.

### ENG version

The most difficult RE task on this CTF. We get a [binary](./r400) (elf again) which takes password as input. We expect the password to be the flag.

Here we have a surprise, because the password is not checked anywhere in the binary. After a while of debugging we realise that the password is casted into a DWORD (four characters) and a byte table is decoded (via xor) with this DWORD and the executed as code. The xored data are:

    5E 68 0E 59 46 06 47 5E 55 11 15 41 5C 0A 03 16
    44 0A 08 52 14 16 0E 16 52 0D 13 5E 14 3B 09 43
    5C 0D 08 45 15 0A 0A 57 40 0B 0E 44 55 16 13 5E
    77 0D 08 51 8E 48 66 36 34 EB 87 8D 35 62 66 36
    8C 66 66 36 34 AF E6 8E 35 62 66 36 F9 E2 F6 A6

First attempts to get the password failed (we assumed this code block is a function nad has some standard prolog). Soon we got a better idea. What is the most common byte value in the code? Zero of course. So if we find the most common byte in the encoded block we can expect those to be zeroes in the decoded verson. We use the code to measure byte frequency:

    source = '5E680E594606475E551115415C0A0316440A085214160E16520D135E143B09435C0D0845150A0A57400B0E445516135E770D08518E48663634EB878D356266368C66663634AFE68E35626636F9E2F6A6'.decode('hex')
    prologue = '554889E5'.decode('hex')

    def xor(a, b):
        return ''.join(chr(ord(ac) ^ ord(bc)) for ac, bc in zip(a, b))

    print xor(source, prologue).encode('hex')

    a0 = source[0::4]
    a1 = source[1::4]
    a2 = source[2::4]
    a3 = source[3::4]

    def most_common(x):
        import collections
        s = collections.Counter(x).most_common(1)[0]
        return (s[0].encode('hex'), s[1])

    print most_common(a0),
    print most_common(a1),
    print most_common(a2),
    print most_common(a3),

And this was a bull's-eye! (If we remeber correctly one of the four fragments were wrong but we could fix those by hand)
This way we solved the hardest RE task on the CTF and got another flag worth 400 points.