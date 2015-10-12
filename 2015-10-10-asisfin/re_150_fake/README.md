## Fake 150 (re, 150p)

### PL
[ENG](#eng-version)

Dostajemy [program](./fake) (elf), do analizy, i rozpoczynamy od zdekompilowania go:

    int main(int argc, char **argv)
    {
        v = 0;
        vv = (v >> 19);
        vvv = (v >> 63);
        if (argc > 1) {
            v = strtol(argv[1], 0, 10);
        }
        uint64_t va[5];
        va[0] = 1019660215 * v;
        va[1] = 2676064947712729
            * ((v >> 19) - 2837 * (((int64_t)((6658253765061184651 * (v >> 19)) >> 64) >> 10) - (v >> 63)))
            * ((v >> 19) - 35 * (((int64_t)((1054099661354831521 * (v >> 19)) >> 64) >> 1) - (v >> 63)))
            * ((v >> 19) - 33 * (((int64_t)((1117984489315730401 * (v >> 19)) >> 64) >> 1) - (v >> 63)));
        va[2] = (vv - 9643 * (((int64_t)((1958878557656183849 * vv) >> 64) >> 10) - vvv)) * 5785690976857702
            * (vv - 167 * (((int64_t)((7069410902499468883 * vv) >> 64) >> 6) - vvv));
        va[3] = (vv - 257 * (((int64_t)((9187483429707480961 * vv) >> 64) >> 7) - vvv)) * 668176625215826
            * (vv - 55 * (((int64_t)((5366325548715505925 * vv) >> 64) >> 4) - vvv));
        va[4] = (vv - 48271 * (((int64_t)((1565284823722614477 * vv) >> 64) >> 12) - vvv)) * 2503371776094
            * (vv - 23 * (((int64_t)(vv + ((0x0B21642C8590B2165 * vv) >> 64)) >> 4) - vvv));
        puts((const char *)va);
        return 0;
    }

Jak widać wykonywane jest tutaj sporo operacji matematycznych, a potem wynikowa liczba wypisywana jako tekst na konsolę.

Piszemy więc prosty skrypt w pythonie, który po prostu zbrutuje możliwe liczby i wypisze wynik. Założenie jest takie, że output zaczyna się od ASIS{ oraz zawiera tylko znaki 0..9a..f. Sprawdzamy więc wyniki mnożenia pierwszej i drugiej operacji. Piszemy więc:

    import struct

    start = 'ASIS{xxx'

    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def modinv(a, m):
        g, x, y = egcd(a, m)
        if g != 1:
            raise Exception('modular inverse does not exist')
        else:
            return x % m

    def tou64(v):
        return struct.unpack('<q', struct.pack('<Q', v))[0]

    N = 2 ** 64
    M = 1019660215
    M1 = modinv(M, N)

    v = 1
    vv = v * 1019660215
    vvv = struct.pack('<Q', vv)

    #  vv = 0x415349537bxxxxxx
    vvmin = 0x0000007b53495341
    vvmax = 0xffffff7b53495341
    i = vvmin
    while i <= vvmax:
        v = (i * M1) % N
        v =  tou64(v)

        v2 = (2676064947712729
         * ((v >> 19) - 2837 * ((((6658253765061184651 * (v >> 19)) >> 64) >> 10) - (v >> 63)))
         * ((v >> 19) - 35 * ((((1054099661354831521 * (v >> 19)) >> 64) >> 1) - (v >> 63)))
         * ((v >> 19) - 33 * ((((1117984489315730401 * (v >> 19)) >> 64) >> 1) - (v >> 63)))) % N
        v2 = struct.pack('<Q', v2)
        if all(c in '0123456789abcdef' for c in v2):
            print v
        i += 0x10000000000

Wyników wyszło dość dużo:

    E:\User\Code\RE\CTF\2015-10-10 asisfin\re_150_fake>python fake.py
    890777067138092231
    2980647405354257607
    1536404797410020551
    6863131814682463431
    1636293229770214599
    698726470626086087
    4493585300778683591
    25313971399
    6583455638994848967
    5139213031050611911
    5239101463410805959
    4301534704266677447
    8096393534419274951
    3602808258954562759
    8742021264691203271
    8841909697051397319
    7904342937907268807
    3260323581041872071
    7205616492595154119

Można by wszystkie false positivy wyeliminować sprawdzając jeszcze wynik następnego działania, ale wyników jest na tyle mało że 
prościej przetestować je wszystkie masowo poleceniem:

    vagrant@precise64:/vagrant$ cat te.txt | xargs -l ./fake
    ASIS{▒7af556bd▒^9▒▒▒_P▒#▒e▒'▒▒▒f
    ASIS{+▒!7af556bd▒▒▒̀▒▒IK▒▒t'p▒R▒*un
    ASIS{▒▒"7af556bd▒▒VZ▒e▒H5▒▒▒▒;3
    ASIS{8▒57af556bd`▒ӡ5▒e▒6▒▒▒T▒B▒▒▒
    ASIS{▒▒<7af556bdଜRF@b▒nwR▒_
    ASIS{X=7af556bd▒2▒▒▒▒▒▒▒\▒▒3X~▒CӤ
    ASIS{▒:Z7af556bd6▒▒▒▒?\L▒c▒6J
    ASIS{f5f7af556bd6973bd6f2687280a243d9}
    ASIS{▒6g7af556bdʇ▒Dj▒▒b▒.▒)-▒▒
    ASIS{G@h7af556bd E▒:▒▒▒X▒&p[▒`\0▒V▒A
    ASIS{g▒7af556bdd▒;R▒b▒▒HI▒▒▒▒▒p▒1▒c▒▒
    ASIS{▒▒▒7af556bdp▒DR>▒▒▒▒M▒f▒<dU▒\,▒
    ASIS{#▒▒7af556bd▒5▒?`3▒▒9▒.  6w▒O▒▒D
    ASIS{▒7af556bd<^-▒]ro*
    ASIS{Њ▒7af556bd▒N▒▒>▒rhUp▒▒G▒)@▒▒▒%" mp▒#S3▒m▒▒s▒F▒bd▒{7'
    ASIS{▒▒7af556bd▒?▒▒$▒p ▒<▒[
    ASIS{▒v▒7af556bd▒▒&▒y3|xRR▒0▒92▒?▒▒▒.
    ASIS{x▒▒7af556bd▒Z

Oczywiście w oczy rzuca się poprawna flaga - ASIS{f5f7af556bd6973bd6f2687280a243d9}.

I od mamy +150 punktów.

### ENG version
