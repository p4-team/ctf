# SMTPresident (crypto 400)


###ENG
[PL](#pl-version)

This was sadly a very badly designed task, because the last step was broken and required a crystal ball to figure out what auther had in mind.
Unfortunately we figured this out after the CTF was over.

In this task we get 170 encrypted emails, 170 public keys for them and encrypted flag.
First thing we notice is that there are 17 emails per single date.
Next we notice that each pubblic key has public exponent `e` equal to 17.

This automatically bring to mind the Hastad broadcast attack using Chinese Reminder Theorem!
We assume here that each day the message that was sent is identical and therefore we have CRT resiude-modulus pairs.

We solve CRT with:

```python
def solve_crt(residues, moduluses):
    import gmpy2
    N = reduce(lambda x, y: x * y, moduluses)
    Nxs = [N / n for n in moduluses]
    ds = [gmpy2.invert(N / n, n) for n in moduluses]
    mults = [residues[i] * Nxs[i] * ds[i] for i in range(len(moduluses))]
    return reduce(lambda x, y: x + y, mults) % N
```

This way we hopefully get `message ^ 17` and by applying integer nth root we recover the value of `message` for each date.
Messages are for example:

```
4/5/16
Sub##ct:#My ##llow#D#C#Mem###s
#onte#t:##e#p t#####a## <MI#SIN##1#62866###4###8349#477####17117####0#97909##6#6##248#11##0478#######87##3##0169#2######30#71###### th#######e#key #####r### o#.
4/2/16
####e#t:##y F#l#o# DN# #e###r#
Co#ten## Kee# this#s##e #M#S#I##>18#2#661##4##08#4##47#2#1#1##1#5#6#0#9#90###6467#24##1180###8#2#29##8705350##6#####6#13#0#7###553# t##t'# ##e key #e a#ree####.
```
So it seems it's a single message just with missing bytes in different mails.
We combine this to get:

```
Subject: My Fellow DNC Members
Content: Keep this safe <MISSING>1862866103431083493477241717117566609979097064670248011800478128293487053500169824960133057115553, that's the key we agreed on.
```

And now comes the uber-confusing guessing part.
Apparently author assumed that we will figure out that he meant the number above does not only specify the suffix of the decryption exponent but also the low bits.
This of course is not justified at all by the data we have, it's just a pure guess.
But it you follow this, you can recover most of `d` bits simply by checking which combination of higher bits won't change the suffix value.

In the end you can run a standard partial key recovery algorithm and even with high public exponent 65537 you can recover the key reasonably quickly.

This could, theoretically, be solved without a crystal ball, but it would require significant computational power...

###PL version

To niestety było bardzo źle zaprojektowane zadanie, głównie dlatego, że ostatni krok wymagał szklanej kuli, żeby zgadnać co autor miał na myśli.
Nam udało sie to dopiero po zakończeniu CTFa.

W tym zadaniu dostajemy na początku 170 zaszyfrowanych maili, 170 kluczy publicznych oraz zaszyfrowaną flagę.
Pierwsza rzecz którą zauważamy, to fakt, że każdego dnia jest 17 maili.
Następnie zauważamy, że publiczny wykładnik szyfrujacy wynosi 17.

To automatycznie przywodzi na myśl atak Hastad broadcast z wykorzystaniem Chińskiego Twierdzenia o Resztach.
Zakładamy tutaj, że każdego dnia wysyłano tą samą wiadomość a tym samym znamy pary reszta-modulus dla CRT.

Rozwiązujemy CRT:

```python
def solve_crt(residues, moduluses):
    import gmpy2
    N = reduce(lambda x, y: x * y, moduluses)
    Nxs = [N / n for n in moduluses]
    ds = [gmpy2.invert(N / n, n) for n in moduluses]
    mults = [residues[i] * Nxs[i] * ds[i] for i in range(len(moduluses))]
    return reduce(lambda x, y: x + y, mults) % N
```

I w ten sposób liczymy na otrzymanie wartości `message^17` i wyliczając całkowity pierwiastek 17 stopnia odzyskujemy wartość `message` dla każdej daty.
Wiadomości które dostajemy wyglądają tak:

```
4/5/16
Sub##ct:#My ##llow#D#C#Mem###s
#onte#t:##e#p t#####a## <MI#SIN##1#62866###4###8349#477####17117####0#97909##6#6##248#11##0478#######87##3##0169#2######30#71###### th#######e#key #####r### o#.
4/2/16
####e#t:##y F#l#o# DN# #e###r#
Co#ten## Kee# this#s##e #M#S#I##>18#2#661##4##08#4##47#2#1#1##1#5#6#0#9#90###6467#24##1180###8#2#29##8705350##6#####6#13#0#7###553# t##t'# ##e key #e a#ree####.
```

Więc widać, że to jedna wiadomość, tylko dla różnych dat brakuje różnych fragmentów.
Składamy to i dostajemy:

```
Subject: My Fellow DNC Members
Content: Keep this safe <MISSING>1862866103431083493477241717117566609979097064670248011800478128293487053500169824960133057115553, that's the key we agreed on.
```

I teraz następuje bardzo dziwna część zgaduj zgaduli.
Najwyraźniej autor założył, że wpadniemy na to, że liczba powyżej nie określa jedynie suffixu wykładnika deszyfrującego, ale także niskie bity.
To jest oczywiście niczym nie poparte w danych którymi dysponujemy, to zwykłe zgadywanie.
Ale jeśli poczynimy takie założenie, możemy odzyskać większość bitów `s` zwyczajnie testując które kombinacje wysokich bitów nie zmienią nam suffixu.

Finalnie możemy uruchomić standardowy algorytm odzyskiwania klucza z częściowych danch i nawet dla wysokiej eksponenty 65537 możemy odzyskać klucz wzlgędnie szybko.

To teoretycznie można by też rozwiązać bez szklanej kuli, ale wymagałoby dość sporej mocy obliczeniowej...
