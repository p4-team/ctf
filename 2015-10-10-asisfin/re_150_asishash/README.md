## AsisHash 150 (re, 150p)

### PL
[ENG](#eng-version)

Dostajemy [program](./hash.elf) (elf). Analizujemy jego działanie, w dużym uproszczeniu wygląda to tak:

    int main() {
        char password[...];
        scanf("%s", password);

        char *hash = hash_password(password);
        if (!strcmp(hash, good_hash)) {
            puts("Congratz, you got the flag :) ");
        } else {
            puts("Sorry! flag is not correct!");
        }
    }

Funkcja hash_password jest bardzo skomplikowana i nawet nie próbowaliśmy analizować jej działania. Zamiast tego zrobiliśmy coś prostszego - ponieważ
hash jest monotoniczny (dla dłuższych haseł/wyższych znaków ascii daje wyższe wyniki), spróbowaliśmy zgadnac hash (docelowy hash flagi jest stay i równy 27221558106229772521592198788202006619458470800161007384471764) za pomocą bruteforcowania z nawrotami wszystkich możliwych flag:

    import subprocess

    def run(flag):
        return subprocess.check_output(['./hash.elf', flag]).split('\n')[0]

    def prefx(a, b):
        p = 0
        for ac, bc in zip(a, b):
            if ac == bc:
                p += 1
            else:
                break
        return p

    def plaintext(t):
        return ''.join(c if 32 <= ord(c) <= 127 else '.' for c in t)

    sln = '27221558106229772521592198788202006619458470800161007384471764'
    charset = '0123456789abcdef}'

    def tryit(f, r, n):
        pp = prefx(sln, r)
        print plaintext(f), r[:pp], r[pp:]
        stat = '<' if sln[pp] < r[pp] else '>'
        print plaintext(f), r[:pp], r[pp:], stat
        for c in charset:
            f2 = f[:n] + c + f[n+1:]
            r2 = run(f2)
            p2 = prefx(sln, r2)
            if p2 > pp:
                s = tryit(f2, r2, n+1)
                if s == '>':
                    return
        return stat

    for c in range(256): # try to guess good initial padding
        print c, '!!!!!!!!!!!'  # debug info
        placeholder = chr(c)
        start = 'ASIS{' + placeholder * 33
        start = 'ASIS{d5c808f5dc96567bda48' + placeholder * 13   # algorytm zacinał się czasami, więc ręcznie dawaliśmy mu dobre wartości początkowe przeniesione z poprzednich wykonań.
        start = 'ASIS{d5c808f5dc96567bda48be9ba82fc1d' + placeholder * 2
        tryit(start, run(start), len(start.replace(placeholder, '')))

Po chwili czekania i tweakowania algorytmu, dostajemy flagę:

    ASIS{d5c808f5dc96567bda48be9ba82fc1d6}

### ENG version

We get a [binary](./hash.elf) (elf). We analyse its behaviour and it is doing:

    int main() {
        char password[...];
        scanf("%s", password);

        char *hash = hash_password(password);
        if (!strcmp(hash, good_hash)) {
            puts("Congratz, you got the flag :) ");
        } else {
            puts("Sorry! flag is not correct!");
        }
    }

The `hash_password` function is very complex and we didn't ever try to analyse it. Instead we did something simpler - since the hash is monotonous (for longer input/higher characters it gives higher results) we tried guessing correct flag (flag hash is known and equal to (27221558106229772521592198788202006619458470800161007384471764) using bruteforce with backtracing:

    import subprocess

    def run(flag):
        return subprocess.check_output(['./hash.elf', flag]).split('\n')[0]

    def prefx(a, b):
        p = 0
        for ac, bc in zip(a, b):
            if ac == bc:
                p += 1
            else:
                break
        return p

    def plaintext(t):
        return ''.join(c if 32 <= ord(c) <= 127 else '.' for c in t)

    sln = '27221558106229772521592198788202006619458470800161007384471764'
    charset = '0123456789abcdef}'

    def tryit(f, r, n):
        pp = prefx(sln, r)
        print plaintext(f), r[:pp], r[pp:]
        stat = '<' if sln[pp] < r[pp] else '>'
        print plaintext(f), r[:pp], r[pp:], stat
        for c in charset:
            f2 = f[:n] + c + f[n+1:]
            r2 = run(f2)
            p2 = prefx(sln, r2)
            if p2 > pp:
                s = tryit(f2, r2, n+1)
                if s == '>':
                    return
        return stat

    for c in range(256): # try to guess good initial padding
        print c, '!!!!!!!!!!!'  # debug info
        placeholder = chr(c)
        start = 'ASIS{' + placeholder * 33
        start = 'ASIS{d5c808f5dc96567bda48' + placeholder * 13   # the algorithm sometimes was stuck so we were starting it again with already pre-computed prefixes
        start = 'ASIS{d5c808f5dc96567bda48be9ba82fc1d' + placeholder * 2
        tryit(start, run(start), len(start.replace(placeholder, '')))

And after a short while and some optimizations to the algorithm we get the flag:

    ASIS{d5c808f5dc96567bda48be9ba82fc1d6}
