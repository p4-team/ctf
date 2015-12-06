##Last Challenge (Thank you for playing) (Misc/Crypto, 50p)

```
ex1
Cipher:PXFR}QIVTMSZCNDKUWAGJB{LHYEO
Plain: ABCDEFGHIJKLMNOPQRSTUVWXYZ{}

ex2
Cipher:EV}ZZD{DWZRA}FFDNFGQO
Plain: {HELLOWORLDSECCONCTF}

quiz
Cipher:A}FFDNEA}}HDJN}LGH}PWO
Plain: ??????????????????????
```

###PL
[ENG](#eng-version)

Dostajemy do rozwiązania prost szyfr podstawieniowy. Na podsatwie pierwszej pary plaintext-ciphertext generujemy mapę podstawień a następnie dekodujemy flagę:

```python
data1 = "PXFR}QIVTMSZCNDKUWAGJB{LHYEO"
res1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ{}"
sub = dict(zip(data1, res1))
print("".join([sub[letter] for letter in "A}FFDNEA}}HDJN}LGH}PWO"]))
```

`SECCON{SEEYOUNEXTYEAR}`


### ENG version

We get a very simple substitution cipher to solve. Using the first plaintext-ciphertext pair we genrate a substitution map and the we decode the flag:

```python
data1 = "PXFR}QIVTMSZCNDKUWAGJB{LHYEO"
res1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ{}"
sub = dict(zip(data1, res1))
print("".join([sub[letter] for letter in "A}FFDNEA}}HDJN}LGH}PWO"]))
```

`SECCON{SEEYOUNEXTYEAR}`