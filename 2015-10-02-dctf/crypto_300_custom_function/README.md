## Crypto 300 (crypto, 300p)

### PL

[ENG](#eng-version)

Bardzo ciekawe zadanie dla nas, musieliśmy sporo z nim powalczyć, ale w końcu udało się rozwiązać zagadkę szyfru.

Otóż dostajemy taki szyfr:

    320b1c5900180a034c74441819004557415b0e0d1a316918011845524147384f5700264f48091e45
    00110e41030d1203460b1d0752150411541b455741520544111d0000131e0159110f0c16451b0f1c
    4a74120a170d460e13001e120a1106431e0c1c0a0a1017135a4e381b16530f330006411953664334
    593654114e114c09532f271c490630110e0b0b

Oraz kod którym go zaszyfrowano (w wersji przepisanej przez nas do pythona, nie jesteśmy fanami PHP):

    def encrypt(plainText):
        space = 10
        cipherText = ""
        for i in range(len(plainText)):
            if i + space < len(plainText) - 1:
                cipherText += chr(ord(plainText[i]) ^ ord(plainText[i + space]))
            else:
                cipherText += chr(ord(plainText[i]) ^ ord(plainText[space]))
            if ord(plainText[i]) % 2 == 0:
                space += 1
            else:
                space -= 1
        return cipherText

Bardzo komplikuje wszystko ta ruszająca się space. Ale jej stan zależy tylko od najniższego bitu, co wykorzystaliśmy przy rozwiązywaniu zadania.
Rozwiązywaliśmy je w dwóch częściach - najpierw odzyskaliśmy najniższe bity plaintextu, a później dopiero całe hasło.

Pierwsza próba złamania najniższych bitów wyglądała tak:

    def verify(cipherText, guessedBits):
        space = 10
        for i in range(len(guessedBits)):
            if i + space < len(cipherText) - 1:
                if i + space >= len(guessedBits):
                    return True
                if (ord(cipherText[i]) & 1) != ((ord(guessedBits[i]) & 1) ^ (ord(guessedBits[i + space]) & 1)):
                    return False
            else:
                if space >= len(guessedBits):
                    return True
                if (ord(cipherText[i]) & 1) != ((ord(guessedBits[i]) & 1) ^ (ord(guessedBits[space]) & 1)):
                    return False
            if guessedBits[i] == '0':
                space += 1
            else:
                space -= 1
        return True


    def decrypt(cipherText, guessedBits, i):
        if i >= len(cipherText):
            print 'ok:', guessedBits
            return
        if len(guessedBits) == 10:
            print (int(guessedBits, 2) / 1024.0) * 100, '%'
        if verify(cipherText, guessedBits):
            decrypt(cipherText, guessedBits + '0', i + 1)
            decrypt(cipherText, guessedBits + '1', i + 1)

Konkretnie, był to bruteforce z odcinaniem - sprawdzaliśmy wszystkie możliwości, i jeśli verify() się nie udał, wychodziliśmy ze sprawdzanej gałęzi

Niestety, było to dużo za wolne. Zaczeliśmy od mikrooptymalizacji - jeśli dobrze pamiętam, przyśpieszyło to wykonanie skryptu prawie 600 razy (!) (a używaliśmy już pypy do wszystkich testów i tak):

    def verify(cipherText, guessedBits, length, guessed_len):
        space = 10
        for i in range(guessed_len):
            if i + space < length - 1:
                if i + space >= guessed_len:
                    return True
                if (cipherText[i] & 1) != ((guessedBits[i] & 1) ^ (guessedBits[i + space] & 1)):
                    return False
            else:
                if space >= guessed_len:
                    return True
                if (cipherText[i] & 1) != ((guessedBits[i] & 1) ^ (guessedBits[space] & 1)):
                    return False
            if guessedBits[i] == 0:
                space += 1
            else:
                space -= 1
        return True


    def decrypt(cipherText):
        guessed_bits = [0] * len(cipherText)
        length = len(cipherText)
        i = 0
        orded_cipher = [ord(c) for c in cipherText]
        decrypt_r(orded_cipher, guessed_bits, i, length)


    def decrypt_r(orded_cipher, guessedBits, i, length):
        if i >= length:
            print 'ok:', guessedBits
            return
        if i == 10:
            print (int(''.join(str(c) for c in guessedBits[:10]), 2) / 1024.0) * 100, '%'
        if verify(orded_cipher, guessedBits, length, i):
            guessedBits[i] = 0
            decrypt_r(orded_cipher, guessedBits, i + 1, length)
            guessedBits[i] = 1
            decrypt_r(orded_cipher, guessedBits, i + 1, length)

Wykonywało się już relatywnie szybko. Odpaliliśmy to na czterech rdzeniach u jednego z członków naszego zespołu.

Ale nie zapowiadało się to zbyt optymistycznie, więc spróbowaliśmy jeszcze zmienić podejście (viva la algorytmika!). Zamiast za każdym razem weryfikować całe hasło (i wychodzić w przód niepotrzebnie), odrzucać niemożliwe rozwiązania od razu:

    def decrypt(cipherText):
        guessed_bits = ['?'] * len(cipherText)
        length = len(cipherText)
        i = 0
        orded_cipher = [ord(c) & 1 for c in cipherText]
        decrypt_r(orded_cipher, guessed_bits, i, length, 10)
    
    
    def try_guess(orded_cipher, guessedbits, i, length, guess, space):
        guessedbits = list(guessedbits)
        guessedbits[i] = guess
        if i + space < length - 1:
            nextndx = i + space
        else:
            nextndx = space
    
        nextbit = orded_cipher[i] ^ guess
        if guess == 0:
            newspace = space + 1
        else:
            newspace = space - 1
    
        if guessedbits[nextndx] == '?' or guessedbits[nextndx] == nextbit:
            guessedbits[nextndx] = nextbit
            decrypt_r(orded_cipher, guessedbits, i + 1, length, newspace)
    
    def decrypt_r(orded_cipher, guessedbits, i, length, space):
        if i >= length:
            print 'ok:', ''.join(str(c) for c in guessedbits)
            return
        if guessedbits[i] == '?':
            try_guess(orded_cipher, guessedbits, i, length, 0, space)
            try_guess(orded_cipher, guessedbits, i, length, 1, space)
        elif guessedbits[i] == 0:
            try_guess(orded_cipher, guessedbits, i, length, 0, space)
        elif guessedbits[i] == 1:
            try_guess(orded_cipher, guessedbits, i, length, 1, space)

Używamy tu swoistego triboola w tablicy guessedbits, czyli 0 oznacza "na pewno będzie tam 0", 1 oznacza "na pewno będzie tam 1", a ? oznacza ofc "nie wiadomo".

Pisanie i debugowanie tej wersji zajęło nam około godziny. A rozwiązanie dała dosłownie kilka sekund po uruchomieniu (poprzednia wersja ciągle się liczyła jeszcze).

Tak czy inaczej, poprawne rozwiązania (szukaliśmy tutaj najniższych bitów plaintextu, przypominam) były cztery:

sln = '1001011001110101110010100010110110010000010000100111010010111010010100111100001001110000011110010011110100101001010110010110101000110110100'
sln = '1001011001110101110010100010110110000100010111010011010000011001001100111100111011110000000110100001110100101001010110010110101000110110100'
sln = '0101011000010101110100001010000110100101001011010111000100111000010010000011001000110101001110101111110100001000110110101001010111111110100'
sln = '0101011000010101110100001010000110100101001011000011000100111000110010001100011001110101000010100001110101100111000100101001010111001001011'

Otrzymaliśmy w ten sposób układ równań dla 140 zmiennych. Nasza pierwsza próba to było użycie gotowego solvera do rozwiązania tego układu. Przykładowo dla 4 rozwiązania:

    from constraint import *
    problem = Problem()

    ODD = range(33, 128, 2) + [13]
    EVEN = range(32, 128, 2) + [10]

    problem.addVariable(0, ODD)
    problem.addVariable(1, EVEN)
    problem.addVariable(2, EVEN)
    problem.addVariable(3, ODD)
    problem.addVariable(4, EVEN)
    # (...) snip
    problem.addVariable(134, ODD)
    problem.addVariable(135, EVEN)
    problem.addVariable(136, ODD)
    problem.addVariable(137, EVEN)
    problem.addVariable(138, EVEN)

    problem.addConstraint(lambda av, bv: av ^ bv == 0x32, (0, 10))
    problem.addConstraint(lambda av, bv: av ^ bv == 0xb, (1, 10))
    problem.addConstraint(lambda av, bv: av ^ bv == 0x1c, (2, 12))
    problem.addConstraint(lambda av, bv: av ^ bv == 0x59, (3, 14))
    problem.addConstraint(lambda av, bv: av ^ bv == 0x0, (4, 14))
    problem.addConstraint(lambda av, bv: av ^ bv == 0x18, (5, 16))
    # (...) snip
    problem.addConstraint(lambda av, bv: av ^ bv == 0x6, (133, 17))
    problem.addConstraint(lambda av, bv: av ^ bv == 0x30, (134, 16))
    problem.addConstraint(lambda av, bv: av ^ bv == 0x11, (135, 15))
    problem.addConstraint(lambda av, bv: av ^ bv == 0xe, (136, 16))
    problem.addConstraint(lambda av, bv: av ^ bv == 0xb, (137, 15))
    problem.addConstraint(lambda av, bv: av ^ bv == 0xb, (138, 16))

    print problem.getSolutions()

Niestety, solver wykonywał się wieki (nie mamy pewności czy wykonałby się w tym stuleciu). Dlatego, w czasie kiedy on się liczył, my zabraliśmy się za ręczne pisanie solvera:

    import string
    slv = [None] * len(sln)
    
    def filling_pass(slv):
        while True:
            any = False
            space = 10
            for i in range(len(sln)):
                if i + space < len(sln) - 1:
                    nx = i + space
                else:
                    nx = space
                if sln[i] == '0':
                    space += 1
                else:
                    space -= 1
                if slv[i] is not None:
                    sn = ord(slv[i]) ^ ord(ciph[i])
                    if slv[nx] is None:
                        slv[nx] = chr(sn)
                        if (sn >= 32 and sn < 127) or sn == 10 or sn == 13:
                            any = True
                        else:
                            return False
                    else:
                        if slv[nx] != chr(sn):
                            return False
            if not any:
                return True
    
    def tryit(slvo, start):
        while slvo[start] is not None:
            start += 1
            if start >= len(slvo):
                print ''.join(' ' if c is None else '.' if ord(c) < 32 else c for c in slvo)
                return
            continue
        for c in string.printable:
            slv = list(slvo)
            slv[start] = c
            possible = filling_pass(slv)
            if possible:
                tryit(slv, start)
    
    tryit(slv, 0)

I po raz drugi w tym zadaniu, to co liczyło się godziny/dni naiwnym programem, po poprawie algorytmu zadziałało w *sekundy*. Cieszy że mimo postępu komputerów jednak myślenie nad wydajnością ma czasami zastosowanie.

Konkretnie, nasze rozwiązanie działało na takiej zasadzie:

    hasło = ['?'] * długość_hasła
    while (nie wszystkie literki w haśle znane):
        for char in charset:
            podstaw char za kolejną literkę w haśle
            wywnioskuj na podstawie znanych ograniczeń jak najwięcej innych znaków (funkcja filling_pass). Jeśli wyjdzie sprzeczność, zaniechaj, inaczej rekurencyjnie powtarzaj.

Odpaliliśmy więc nasz algorytm:

    C:\Users\xxx\Code\RE\CTF\2015-10-02 def\crypto300>python hackz.py
    Cpgl5bpyy5qz{p5lz`5VAS5eb{pg;5[zb5\5}tcp5az5r|cp5lz`5a}p5gpbtgq5szg5tyy5a}|f5}tgq5bzg~5zg5xtlwp5r`pff|{r;5A}p5sytr5|f5vgleat{tylf|fJ|fJ}tgq
    Izmf?hzss?{pqz?fpj?\KY?ohqzm1?Qph?V?w~iz?kp?xviz?fpj?kwz?mzh~m{?ypm?~ss?kwvl?w~m{?hpmt?pm?r~f}z?xjzllvqx1?Kwz?ys~x?vl?|mfok~q~sflvl@vl@w~m{
    Qbu~'pbkk'chib'~hr'DSA'wpibu)'Ihp'N'ofqb'sh'`nqb'~hr'sob'ubpfuc'ahu'fkk'sont'ofuc'phul'hu'jf~eb'`rbttni`)'Sob'akf`'nt'du~wsfifk~tntXntXofuc
    Rav}$sahh$`kja$}kq$GPB$tsjav*$Jks$M$lera$pk$cmra$}kq$pla$vasev`$bkv$ehh$plmw$lev`$skvo$kv$ie}fa$cqawwmjc*$Pla$bhec$mw$gv}tpejeh}wmw[mw[lev`
    S`w|%r`ii%ajk`%|jp%FQC%urk`w+%Kjr%L%mds`%qj%bls`%|jp%qm`%w`rdwa%cjw%dii%qmlv%mdwa%rjwn%jw%hd|g`%bp`vvlkb+%Qm`%cidb%lv%fw|uqdkdi|vlvZlvZmdwa
    Tgp{"ugnn"fmlg"{mw"AVD"rulgp,"Lmu"K"jctg"vm"ektg"{mw"vjg"pgucpf"dmp"cnn"vjkq"jcpf"umpi"mp"oc{`g"ewgqqkle,"Vjg"dnce"kq"ap{rvclcn{qkq]kq]jcpf
    Ufqz#tfoo#glmf#zlv#@WE#stmfq-#Mlt#J#kbuf#wl#djuf#zlv#wkf#qftbqg#elq#boo#wkjp#kbqg#tlqh#lq#nbzaf#dvfppjmd-#Wkf#eobd#jp#`qzswbmbozpjp\jp\kbqg
    Very well done you CTF pwner. Now I have to give you the reward for all this hard work or maybe guessing. The flag is cryptanalysis_is_hard
    Wdsx!vdmm!enod!xnt!BUG!qvods/!Onv!H!i`wd!un!fhwd!xnt!uid!sdv`se!gns!`mm!uihr!i`se!vnsj!ns!l`xcd!ftdrrhof/!Uid!gm`f!hr!bsxqu`o`mxrhr^hr^i`se
    Xk|w.ykbb.ja`k.wa{.MZH.~y`k| .@ay.G.foxk.za.igxk.wa{.zfk.|kyo|j.ha|.obb.zfg}.fo|j.ya|e.a|.cowlk.i{k}}g`i .Zfk.hboi.g}.m|w~zo`obw}g}Qg}Qfo|j

    C:\Users\xxx\Code\RE\CTF\2015-10-02 def\crypto300>

Świetnie - zdobyliśmy flagę - `cryptanalysis_is_hard`

### ENG version

Very interesting task for us, we had to put much effort into this by we finally solved it.

We get a ciphertext:

    320b1c5900180a034c74441819004557415b0e0d1a316918011845524147384f5700264f48091e45
    00110e41030d1203460b1d0752150411541b455741520544111d0000131e0159110f0c16451b0f1c
    4a74120a170d460e13001e120a1106431e0c1c0a0a1017135a4e381b16530f330006411953664334
    593654114e114c09532f271c490630110e0b0b

And code whcih was used to encode it (rewritten to Python since we're not fans of PHP):

    def encrypt(plainText):
        space = 10
        cipherText = ""
        for i in range(len(plainText)):
            if i + space < len(plainText) - 1:
                cipherText += chr(ord(plainText[i]) ^ ord(plainText[i + space]))
            else:
                cipherText += chr(ord(plainText[i]) ^ ord(plainText[space]))
            if ord(plainText[i]) % 2 == 0:
                space += 1
            else:
                space -= 1
        return cipherText

The biggest issue here is the moving space. However its state depends only on the lowest bit of the plaintext character, which we exploited to solve the task.
The solution was split into two parts - first we extracted lowest bits of the plaintext and after that we decoded the whole ciphertext.

First attempts to extract the lowest bits:

    def verify(cipherText, guessedBits):
        space = 10
        for i in range(len(guessedBits)):
            if i + space < len(cipherText) - 1:
                if i + space >= len(guessedBits):
                    return True
                if (ord(cipherText[i]) & 1) != ((ord(guessedBits[i]) & 1) ^ (ord(guessedBits[i + space]) & 1)):
                    return False
            else:
                if space >= len(guessedBits):
                    return True
                if (ord(cipherText[i]) & 1) != ((ord(guessedBits[i]) & 1) ^ (ord(guessedBits[space]) & 1)):
                    return False
            if guessedBits[i] == '0':
                space += 1
            else:
                space -= 1
        return True


    def decrypt(cipherText, guessedBits, i):
        if i >= len(cipherText):
            print 'ok:', guessedBits
            return
        if len(guessedBits) == 10:
            print (int(guessedBits, 2) / 1024.0) * 100, '%'
        if verify(cipherText, guessedBits):
            decrypt(cipherText, guessedBits + '0', i + 1)
            decrypt(cipherText, guessedBits + '1', i + 1)

This is a simple brute-force with prunning - we test all possibilities and if verify() failed we prune given branch.

Unfortunately this was too slow. We started with some optimization of the code - and if I remember correctly this resulted in 600 times faster execution (!) (and we were already running on pypy for all the tests):

    def verify(cipherText, guessedBits, length, guessed_len):
        space = 10
        for i in range(guessed_len):
            if i + space < length - 1:
                if i + space >= guessed_len:
                    return True
                if (cipherText[i] & 1) != ((guessedBits[i] & 1) ^ (guessedBits[i + space] & 1)):
                    return False
            else:
                if space >= guessed_len:
                    return True
                if (cipherText[i] & 1) != ((guessedBits[i] & 1) ^ (guessedBits[space] & 1)):
                    return False
            if guessedBits[i] == 0:
                space += 1
            else:
                space -= 1
        return True


    def decrypt(cipherText):
        guessed_bits = [0] * len(cipherText)
        length = len(cipherText)
        i = 0
        orded_cipher = [ord(c) for c in cipherText]
        decrypt_r(orded_cipher, guessed_bits, i, length)


    def decrypt_r(orded_cipher, guessedBits, i, length):
        if i >= length:
            print 'ok:', guessedBits
            return
        if i == 10:
            print (int(''.join(str(c) for c in guessedBits[:10]), 2) / 1024.0) * 100, '%'
        if verify(orded_cipher, guessedBits, length, i):
            guessedBits[i] = 0
            decrypt_r(orded_cipher, guessedBits, i + 1, length)
            guessedBits[i] = 1
            decrypt_r(orded_cipher, guessedBits, i + 1, length)

This was already reasonably fast. We fired this four times for different prefixes on one machine.

But since we had to wait anyway, we decided to try a different approach (viva la algorithmics). Instead of verifying the whole password every time (by going forward) we rejected impossible solutions right away:

    def decrypt(cipherText):
        guessed_bits = ['?'] * len(cipherText)
        length = len(cipherText)
        i = 0
        orded_cipher = [ord(c) & 1 for c in cipherText]
        decrypt_r(orded_cipher, guessed_bits, i, length, 10)
    
    
    def try_guess(orded_cipher, guessedbits, i, length, guess, space):
        guessedbits = list(guessedbits)
        guessedbits[i] = guess
        if i + space < length - 1:
            nextndx = i + space
        else:
            nextndx = space
    
        nextbit = orded_cipher[i] ^ guess
        if guess == 0:
            newspace = space + 1
        else:
            newspace = space - 1
    
        if guessedbits[nextndx] == '?' or guessedbits[nextndx] == nextbit:
            guessedbits[nextndx] = nextbit
            decrypt_r(orded_cipher, guessedbits, i + 1, length, newspace)
    
    def decrypt_r(orded_cipher, guessedbits, i, length, space):
        if i >= length:
            print 'ok:', ''.join(str(c) for c in guessedbits)
            return
        if guessedbits[i] == '?':
            try_guess(orded_cipher, guessedbits, i, length, 0, space)
            try_guess(orded_cipher, guessedbits, i, length, 1, space)
        elif guessedbits[i] == 0:
            try_guess(orded_cipher, guessedbits, i, length, 0, space)
        elif guessedbits[i] == 1:
            try_guess(orded_cipher, guessedbits, i, length, 1, space)

We use a tri-value-boolean in guessedbits, 0 for `there is definitely 0`, 1 for `there is definitely 1` and ? for `don't know`.

It took us an hour to write this and debug but we got the results within a few seconds (while the previous version was still computing).

Anyway, the final correct sulutions (for lowest bits of the plaintext) were four:

sln = '1001011001110101110010100010110110010000010000100111010010111010010100111100001001110000011110010011110100101001010110010110101000110110100'
sln = '1001011001110101110010100010110110000100010111010011010000011001001100111100111011110000000110100001110100101001010110010110101000110110100'
sln = '0101011000010101110100001010000110100101001011010111000100111000010010000011001000110101001110101111110100001000110110101001010111111110100'
sln = '0101011000010101110100001010000110100101001011000011000100111000110010001100011001110101000010100001110101100111000100101001010111001001011'

This way we got a set of equations with 140 variables. We tried to use a constraint-programming solver to solve it. For example for the bits number 4:

    from constraint import *
    problem = Problem()

    ODD = range(33, 128, 2) + [13]
    EVEN = range(32, 128, 2) + [10]

    problem.addVariable(0, ODD)
    problem.addVariable(1, EVEN)
    problem.addVariable(2, EVEN)
    problem.addVariable(3, ODD)
    problem.addVariable(4, EVEN)
    # (...) snip
    problem.addVariable(134, ODD)
    problem.addVariable(135, EVEN)
    problem.addVariable(136, ODD)
    problem.addVariable(137, EVEN)
    problem.addVariable(138, EVEN)

    problem.addConstraint(lambda av, bv: av ^ bv == 0x32, (0, 10))
    problem.addConstraint(lambda av, bv: av ^ bv == 0xb, (1, 10))
    problem.addConstraint(lambda av, bv: av ^ bv == 0x1c, (2, 12))
    problem.addConstraint(lambda av, bv: av ^ bv == 0x59, (3, 14))
    problem.addConstraint(lambda av, bv: av ^ bv == 0x0, (4, 14))
    problem.addConstraint(lambda av, bv: av ^ bv == 0x18, (5, 16))
    # (...) snip
    problem.addConstraint(lambda av, bv: av ^ bv == 0x6, (133, 17))
    problem.addConstraint(lambda av, bv: av ^ bv == 0x30, (134, 16))
    problem.addConstraint(lambda av, bv: av ^ bv == 0x11, (135, 15))
    problem.addConstraint(lambda av, bv: av ^ bv == 0xe, (136, 16))
    problem.addConstraint(lambda av, bv: av ^ bv == 0xb, (137, 15))
    problem.addConstraint(lambda av, bv: av ^ bv == 0xb, (138, 16))

    print problem.getSolutions()

Unfortunately, it was taking a long time (and we're not sure if it would compute in this century). So in the meanwhile we attempted to make a custom solver:

    import string
    slv = [None] * len(sln)
    
    def filling_pass(slv):
        while True:
            any = False
            space = 10
            for i in range(len(sln)):
                if i + space < len(sln) - 1:
                    nx = i + space
                else:
                    nx = space
                if sln[i] == '0':
                    space += 1
                else:
                    space -= 1
                if slv[i] is not None:
                    sn = ord(slv[i]) ^ ord(ciph[i])
                    if slv[nx] is None:
                        slv[nx] = chr(sn)
                        if (sn >= 32 and sn < 127) or sn == 10 or sn == 13:
                            any = True
                        else:
                            return False
                    else:
                        if slv[nx] != chr(sn):
                            return False
            if not any:
                return True
    
    def tryit(slvo, start):
        while slvo[start] is not None:
            start += 1
            if start >= len(slvo):
                print ''.join(' ' if c is None else '.' if ord(c) < 32 else c for c in slvo)
                return
            continue
        for c in string.printable:
            slv = list(slvo)
            slv[start] = c
            possible = filling_pass(slv)
            if possible:
                tryit(slv, start)
    
    tryit(slv, 0)

And again for the second time in this task, what was taking hours in the naive implementation, took only *seconds* with a better algorithm. It's nice to think that even though we get more and more powerful computers, thinking about the computational complexity pays off sometimes.

The solver worked like this:

    plaintext = ['?'] * plaintext_length
    while (not all characters in plaintext are decoded):
        for char in charset:
            use char as next letter in password
			using known constraints try to figure out as much as possible of next characters in plaintext (filling_pass function). If there is a constraint violation break, otherwise repeat recursively.

This way we got:

    C:\Users\xxx\Code\RE\CTF\2015-10-02 def\crypto300>python hackz.py
    Cpgl5bpyy5qz{p5lz`5VAS5eb{pg;5[zb5\5}tcp5az5r|cp5lz`5a}p5gpbtgq5szg5tyy5a}|f5}tgq5bzg~5zg5xtlwp5r`pff|{r;5A}p5sytr5|f5vgleat{tylf|fJ|fJ}tgq
    Izmf?hzss?{pqz?fpj?\KY?ohqzm1?Qph?V?w~iz?kp?xviz?fpj?kwz?mzh~m{?ypm?~ss?kwvl?w~m{?hpmt?pm?r~f}z?xjzllvqx1?Kwz?ys~x?vl?|mfok~q~sflvl@vl@w~m{
    Qbu~'pbkk'chib'~hr'DSA'wpibu)'Ihp'N'ofqb'sh'`nqb'~hr'sob'ubpfuc'ahu'fkk'sont'ofuc'phul'hu'jf~eb'`rbttni`)'Sob'akf`'nt'du~wsfifk~tntXntXofuc
    Rav}$sahh$`kja$}kq$GPB$tsjav*$Jks$M$lera$pk$cmra$}kq$pla$vasev`$bkv$ehh$plmw$lev`$skvo$kv$ie}fa$cqawwmjc*$Pla$bhec$mw$gv}tpejeh}wmw[mw[lev`
    S`w|%r`ii%ajk`%|jp%FQC%urk`w+%Kjr%L%mds`%qj%bls`%|jp%qm`%w`rdwa%cjw%dii%qmlv%mdwa%rjwn%jw%hd|g`%bp`vvlkb+%Qm`%cidb%lv%fw|uqdkdi|vlvZlvZmdwa
    Tgp{"ugnn"fmlg"{mw"AVD"rulgp,"Lmu"K"jctg"vm"ektg"{mw"vjg"pgucpf"dmp"cnn"vjkq"jcpf"umpi"mp"oc{`g"ewgqqkle,"Vjg"dnce"kq"ap{rvclcn{qkq]kq]jcpf
    Ufqz#tfoo#glmf#zlv#@WE#stmfq-#Mlt#J#kbuf#wl#djuf#zlv#wkf#qftbqg#elq#boo#wkjp#kbqg#tlqh#lq#nbzaf#dvfppjmd-#Wkf#eobd#jp#`qzswbmbozpjp\jp\kbqg
    Very well done you CTF pwner. Now I have to give you the reward for all this hard work or maybe guessing. The flag is cryptanalysis_is_hard
    Wdsx!vdmm!enod!xnt!BUG!qvods/!Onv!H!i`wd!un!fhwd!xnt!uid!sdv`se!gns!`mm!uihr!i`se!vnsj!ns!l`xcd!ftdrrhof/!Uid!gm`f!hr!bsxqu`o`mxrhr^hr^i`se
    Xk|w.ykbb.ja`k.wa{.MZH.~y`k| .@ay.G.foxk.za.igxk.wa{.zfk.|kyo|j.ha|.obb.zfg}.fo|j.ya|e.a|.cowlk.i{k}}g`i .Zfk.hboi.g}.m|w~zo`obw}g}Qg}Qfo|j

    C:\Users\xxx\Code\RE\CTF\2015-10-02 def\crypto300>

Great, we got the flag - `cryptanalysis_is_hard`
