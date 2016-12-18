# LSB Oracle (crypto 150)

###ENG
[PL](#pl-version)

The task was pretty much the same idea as https://github.com/p4-team/ctf/tree/master/2016-04-15-plaid-ctf/crypto_rabit with the exception that in Plaid CTF we had Rabin cryptosystem and there it was RSA.

We get a [binary](lsb_oracle.vmp.exe.zip) which can give us RSA public key and also it can tell us LSB of decrypted ciphertext.
We also get an encrypted flag.

We approach it the same was as for Rabit on Plaid CTF - we can multiply plaintext by 2 if we multiply ciphertext by `pow(2,e,n)`.
This is because:

```
ct = pt^e mod n
ct' = ct * 2^e mod n = pt^e mod n * 2^e mod n = 2pt^e mod n
ct'^d = (2pt^e mod n)^d mod n = 2pt^ed mod n = 2pt mod n
```

LSB from oracle tells us if the plaintext is even or odd.
Modulus `n` is a product of 2 large primes, so it has to be odd.
`2*x` has to be even.
This means that if LSB of `2*x mod n` is 0 (number is still even) this number was smaller than modulus `n`.
Otherwise the number was bigger than modulus.

We can combine this using binary search approach to get upper and lower bounds of the flag in relation to `n`.

We used a python script for this (slighly more accurate than the one in Rabbit, which was messing up last character):

```python
from subprocess import Popen, PIPE
from Crypto.Util.number import long_to_bytes


def oracle(ciphertext):
    print("sent ciphertext " + str(ciphertext))
    p = Popen(['lsb_oracle.vmp.exe', '/decrypt'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    result = p.communicate(str(ciphertext) + "\n-1")
    lsb = int(result[0][97])
    print(lsb, result)
    return lsb


def brute_flag(encrypted_flag, n, e, oracle_fun):
    flag_count = n_count = 1
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
        mult += 1
        if oracle_fun(ciphertext) == 0:
            flag_upper_bound = n * n_count / flag_count
        else:
            flag_lower_bound = n * n_count / flag_count
            n_count += 1
    return flag_upper_bound


def main():
    n = 120357855677795403326899325832599223460081551820351966764960386843755808156627131345464795713923271678835256422889567749230248389850643801263972231981347496433824450373318688699355320061986161918732508402417281836789242987168090513784426195519707785324458125521673657185406738054328228404365636320530340758959
    ct = 2201077887205099886799419505257984908140690335465327695978150425602737431754769971309809434546937184700758848191008699273369652758836177602723960420562062515168299835193154932988833308912059796574355781073624762083196012981428684386588839182461902362533633141657081892129830969230482783192049720588548332813
    print(long_to_bytes(brute_flag(ct, n, 65537, oracle)))


main()
```

And after a short while we got the flag: `SharifCTF{65d7551577a6a613c99c2b4023039b0a}`

Sadly the flag was at the very end of the plaintext to we had to wait for the whole 1024 bits.

###PL version

Zadanie jest generalnie bardzo podobne do https://github.com/p4-team/ctf/tree/master/2016-04-15-plaid-ctf/crypto_rabit z tą różnicą że na Plaid CTF szyfrowanie odbywało się algorytmem Rabina a tutaj było to RSA.

Dostajemy [binarke](lsb_oracle.vmp.exe.zip) która podaje nam klucz publiczny RSA.
Dostajemy też zaszyfrowaną flagę.

Nasze podejście jest takie samo jak dla Rabit z Plaid CTF - możemy mnożyć plaintext przez 2 poprzez mnożenie ciphertextu przez `pow(2,e,n)`.
Wynika to z tego, że:

```
ct = pt^e mod n
ct' = ct * 2^e mod n = pt^e mod n * 2^e mod n = 2pt^e mod n
ct'^d = (2pt^e mod n)^d mod n = 2pt^ed mod n = 2pt mod n
```

Wyrocznia najniższego bitu mówi nam czy plaintext jest parzysty czy nieparzysty.
Modulus `n` jest iloczynem 2 dużych liczb pierwszych więc musi być nieparzysty.
`2*x` musi być parzyste.
To oznacza, że jeśli LSB `2*x mod n` jest 0 (liczba nadal jest parzysta) to liczba musiała być mniejsza od `n`.
W innym wypadku liczba była większa od `n`.

Możemy to uogólnić i użyć szukania binarnego, aby uzyskać dolne i górne ograniczenie dla flagi, względem `n`.

Wykorzystaliśmy do tego skrypt (trochę bardziej dokładny od tego z Rabit, który psuł ostatni znak):

```python
from subprocess import Popen, PIPE
from Crypto.Util.number import long_to_bytes


def oracle(ciphertext):
    print("sent ciphertext " + str(ciphertext))
    p = Popen(['lsb_oracle.vmp.exe', '/decrypt'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    result = p.communicate(str(ciphertext) + "\n-1")
    lsb = int(result[0][97])
    print(lsb, result)
    return lsb


def brute_flag(encrypted_flag, n, e, oracle_fun):
    flag_count = n_count = 1
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
        mult += 1
        if oracle_fun(ciphertext) == 0:
            flag_upper_bound = n * n_count / flag_count
        else:
            flag_lower_bound = n * n_count / flag_count
            n_count += 1
    return flag_upper_bound


def main():
    n = 120357855677795403326899325832599223460081551820351966764960386843755808156627131345464795713923271678835256422889567749230248389850643801263972231981347496433824450373318688699355320061986161918732508402417281836789242987168090513784426195519707785324458125521673657185406738054328228404365636320530340758959
    ct = 2201077887205099886799419505257984908140690335465327695978150425602737431754769971309809434546937184700758848191008699273369652758836177602723960420562062515168299835193154932988833308912059796574355781073624762083196012981428684386588839182461902362533633141657081892129830969230482783192049720588548332813
    print(long_to_bytes(brute_flag(ct, n, 65537, oracle)))


main()
```

I po chwili dostaliśmy flagę: `SharifCTF{65d7551577a6a613c99c2b4023039b0a}`

Niestety flaga była na samym końcu plaintextu więc musieliśmy czekać na całe 1024 bity.
