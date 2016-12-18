# Lobotomized LSB Oracle (crypto 400)

###ENG
[PL](#pl-version)

This was a follow up for `LSB Oracle` task.

Again we get a [binary](lobotomized_lsb_oracle.vmp.exe.zip) which gives RSA public key and LSB of plaintext.
We also get an encrypted flag.

The difference here is that apparently the binary can make mistakes this time.
It seemed initially a rather hard task, because mistakes generate exponential growth in checks.
We can't also tell if the oracle made mistake or not so we were puzzled here for a while.

Finally we decided to run the standard LSB Oracle attack from previous task on this one and check what we can get.

What we got was quite encouraging - we part of the flag `SharifCTF{76a7e30ea5e�` right!

This meant that the first oracle mistake happened at the very end.
We also run this more times to make sure it's consistent - and it was, the results were always the same.

We assumed that maybe there are only a few mistakes and we can fix them semi-interactively.
The mistake in decoding the flag is simple to spot - if a byte is "settled" and is not from hex charset it has to be wrong.
This means that there had to be an oracle mistake no earlier than 8 bits in the past.

We checked first a single bitflip and it was enough - flipping oracle result for bit 848 caused the whole flag decoding to finish correctly!

So we simply run:

```python
from subprocess import Popen, PIPE
from Crypto.Util.number import long_to_bytes


def oracle(ciphertext):
    print("sent ciphertext " + str(ciphertext))
    p = Popen(['lobotomized_lsb_oracle.vmp.exe', '/decrypt'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    result = p.communicate(str(ciphertext) + "\n-1")
    lsb = int(result[0][97])
    print(lsb, result)
    return lsb


def brute_flag_2(encrypted_flag, n, e, oracle_fun, flips):
    flag_count = 1
    n_count = 1
    flag_lower_bound = 0
    flag_upper_bound = n
    ciphertext = encrypted_flag
    mult = 1
    while flag_upper_bound > flag_lower_bound + 1:
        ciphertext = (ciphertext * pow(2, e, n)) % n
        flag_count *= 2
        n_count = n_count * 2 - 1
        print("upper = %d" % flag_upper_bound)
        print("upper flag = %s" % long_to_bytes(flag_upper_bound))
        print("lower = %d" % flag_lower_bound)
        print("lower flag = %s" % long_to_bytes(flag_lower_bound))
        print("bit = %d" % mult)
        print("bit = %d" % mult)
        print("flag_count = %d" % flag_count)
        print("n_count = %d" % n_count)
        oracle_result = oracle_fun(ciphertext)
        if mult in flips:
            oracle_result = not oracle_result
        if oracle_result == 0:
            flag_upper_bound = n * n_count / flag_count
        else:
            flag_lower_bound = n * n_count / flag_count
            n_count += 1
        mult += 1
    return flag_upper_bound


def main():
    n = 94169898764475155086179365872915864925768243050855426387910613522303337327416930459077578555524838413579345103633071500300104580298306187507383687796776619261744561887287065152410825040924957174425131901014950571780211869823508452987101620679856181308669517708916215765377471785309709279780997993371462202127
    ct = 84554310261580598058211620872297995265063480196893812976334022270327838015482739129096939702314740821259766144865677921673974339162910708930818463109733348984687023660294660726179053438750361754457786927212462355725758670143043124242928370865662017903815787388480232771504943423128214544949007416507395402507
    result = brute_flag_2(ct, n, 65537, oracle, [848])
    print(long_to_bytes(result))


main()
```

And recovered the flag: `SharifCTF{76a7e30ea5f3edd488182c4845a6858e}`

###PL version

To była kolejna część do zadania `LSB Oracle`.

Znowu otrzymaliśmy [binarke](lobotomized_lsb_oracle.vmp.exe.zip) która podawała klucz publiczny RSA oraz LSB dla plaintextu. 
Dostaliśmy też zaszyfrowaną flagę.

Różnica była taka, że binarka potencjalnie mogła się mylić tym razem.
Wydawało się to początkowo bardzo ciężkie, bo błędy oznaczają wykładniczy wzrost złożoności.
Dodatkowo nie byliśmy w stanie stwierdzić czy wyrocznia się pomliła czy też nie, więc przez długi czas nie wiedzieliśmy co zrobić.

Finalnie zdecydowaliśmy się uruchomić standardowy solver dla LSB Oracle z poprzedniego zadania tutaj i zobaczyć co dostaniemy.

Wyniki napawały optymizmem - udało się odzyskać poprawnie część flagi: `SharifCTF{76a7e30ea5e�`

To oznaczało, że wyrocznia pomyliła się dopiero gdzieś daleko przy końcu dekodowania.
Uruchomiliśmy to jeszcze kilka razy żeby upewnić się, że wyniki są deterministyczne - i były.

Założyliśmy, że może błędów jest tylko kilka i można je pół-interaktywnie poprawić.
Błąd w dekodowaniu flagi łatwo zauważyć - jeśli bajt jest już "ustalony" i nie należy do charsetu hex to znaczy że jest zły.
To oznacza że wyrocznia musiała popełnić błąd nie dalej niż na 8 bitów wstecz.

Sprawdziliśmy na początek pojedyńcze flipy i okazało się że to wystarczyło - odpowiedzi dla bitu 848 spowodowała zdekodowanie całej flagi do końca!

Uruchomiliśmy:

```python
from subprocess import Popen, PIPE
from Crypto.Util.number import long_to_bytes


def oracle(ciphertext):
    print("sent ciphertext " + str(ciphertext))
    p = Popen(['lobotomized_lsb_oracle.vmp.exe', '/decrypt'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    result = p.communicate(str(ciphertext) + "\n-1")
    lsb = int(result[0][97])
    print(lsb, result)
    return lsb


def brute_flag_2(encrypted_flag, n, e, oracle_fun, flips):
    flag_count = 1
    n_count = 1
    flag_lower_bound = 0
    flag_upper_bound = n
    ciphertext = encrypted_flag
    mult = 1
    while flag_upper_bound > flag_lower_bound + 1:
        ciphertext = (ciphertext * pow(2, e, n)) % n
        flag_count *= 2
        n_count = n_count * 2 - 1
        print("upper = %d" % flag_upper_bound)
        print("upper flag = %s" % long_to_bytes(flag_upper_bound))
        print("lower = %d" % flag_lower_bound)
        print("lower flag = %s" % long_to_bytes(flag_lower_bound))
        print("bit = %d" % mult)
        print("bit = %d" % mult)
        print("flag_count = %d" % flag_count)
        print("n_count = %d" % n_count)
        oracle_result = oracle_fun(ciphertext)
        if mult in flips:
            oracle_result = not oracle_result
        if oracle_result == 0:
            flag_upper_bound = n * n_count / flag_count
        else:
            flag_lower_bound = n * n_count / flag_count
            n_count += 1
        mult += 1
    return flag_upper_bound


def main():
    n = 94169898764475155086179365872915864925768243050855426387910613522303337327416930459077578555524838413579345103633071500300104580298306187507383687796776619261744561887287065152410825040924957174425131901014950571780211869823508452987101620679856181308669517708916215765377471785309709279780997993371462202127
    ct = 84554310261580598058211620872297995265063480196893812976334022270327838015482739129096939702314740821259766144865677921673974339162910708930818463109733348984687023660294660726179053438750361754457786927212462355725758670143043124242928370865662017903815787388480232771504943423128214544949007416507395402507
    result = brute_flag_2(ct, n, 65537, oracle, [848])
    print(long_to_bytes(result))


main()
```

I odzyskaliśmy flagę: `SharifCTF{76a7e30ea5f3edd488182c4845a6858e}`
