## Rsabin (crypro, 314p, ?? solves)

> Classical things?

> [rsabin-a51076632142e074947b08396bf35ab2.tgz](rsabin.tgz)

### PL
[ENG](#eng-version)

Z dołączonego do zadania pliku tgz wypakowujemy dwa kolejne - [rsabin.py](rsabin.py) (kod szyfrujący coś)
oraz [cipher.txt](cipher.txt) (wynik wykonania go).

Kod szyfrujący wygląda tak:

```python
from Crypto.Util.number import *

p = getPrime(157)
q = getPrime(157)
n = p * q
e = 31415926535897932384

flag = open('flag').read().strip()
assert len(flag) == 50

m = int(flag.encode('hex'), 16)
c = pow(m, e, n)
print 'n =', n
print 'e =', e
print 'c =', c
```

A dane tak:

```
n = 20313365319875646582924758840260496108941009482470626789052986536609343163264552626895564532307
e = 31415926535897932384
c = 19103602508342401901122269279664114182748999577286972038123073823905007006697188423804611222902
```

N jest na tyle małe, że można go sfaktoryzować (albo znaleźć w factordb):

```
p = 123722643358410276082662590855480232574295213977
q = n / p
```

[[ tutaj Shalom oddaje pałeczkę Tobie ]]

(...)

Tak więc otrzymujemy w końcu listę liczb które mogły potencjalnie być wynikami RSA. Nie jest ona specjalnie długa:

```
11781957604393222865231495052284116318876440682267206215409582095778432861874348660845251848045
4169292882246487226436372571580328445408188970955313275707356349635909107039805208587333631745
1170873348295885335059944818034561278496937179514286352764111586578035361653036340797178495797
13871573946024796279189581177591269513969694950673020202114872377044854770083045515434824811804
6441791373850850303735177662669226594971314531797606586938114159564488393181507111460739720503
19142491971579761247864814022225934830444072302956340436288874950031307801611516286098386036510
16144072437629159356488386268680167663532820511515313513345630186973434056224747418308230900562
8531407715482423717693263787976379790064568800203420573643404440830910301390203966050312684262
1055425717878104375386098355306535487232069922237396940514031160338383741028199997840854113277
13756126315607015319515734714863243722704827693396130789864791950805203149458209172478500429284
11591134129841181208716021381503690146413855638482506249018420423689972012921602773678731165798
3978469407694445569920898900799902272945603927170613309316194677547448258087059321420812949498
16334895912181201013003859939460593835995405555300013479736791859061894905177493305474751582809
8722231190034465374208737458756805962527153843988120540034566112919371150342949853216833366509
6557239004268631263409024125397252386236181789074495999188194585804140013806343454417064103023
19257939601997542207538660484953960621708939560233229848538955376270959422236352629054710419030
```

Więc co pozostaje? Tylko je zdeszyfrować za pomocą RSA? Niestety - dalej jest jesten duży problem. W źródle widzimy:

`assert len(flag) == 50`

A jednocześnie `len(long_to_bytes(n))` jest równe 40 - to oznacza, że nasza szyfrowana wiadomość o długości 50 bajtów
jest przycinana przez modulo. Co z tym zrobić? Jedyne co się da to bruteforce - ale niestety, 10 bajtów to dużo
za dużo na jakikolwiek bruteforce. Na szczęście - wiemy coś o wiadomości. Konkretnie, jak się zaczyna i kończy.
Na pewno jest to flaga, więc pierwsze bajty to 'hitcon{' a ostatni bajt to '}'.

Rozpiszmy sobie, jak wygląda flaga, oraz kilka naszych pomocniczych zmiennych (o nich później):

```
flag  = hitcon{ABCxyzxyzxyzxyzxyzxyzxyzxyzxyzxyzx}
const = hitcon{                                  }
brute =        ABC
msg   =           xyzxyzxyzxyzxyzxyzxyzxyzxyzxyzx
```

Po co taki podział? Otóż znamy flag % n, ale niestety, jest to niejednoznaczne (bo ma 50 bajtów, a n 40).
Ale gdybyśmy poznali samo "msg", to msg % n jest już jednoznaczne (bo jest krótsze niż n). A jak go poznać?
Na pewno znamy `const` - możemy odjąć je od flagi. Możemy też brutować `brute` - to tylko trzy bajty, i sprawdzać
każde możliwe `msg` po kolei.

Piszemy kod łamiący/bruteforcujący flagę:

```python
def crack_flag(ct, n):
    n_len = 40
    flag_len = 50
    const = int('hitcon{'.encode('hex'), 16) * (256**(flag_len - 7))
    for a in range(32, 128):
        for b in range(32, 128):
            for c in range(32, 127):
                brute = (a * 256 * 256 + b * 256 + c) * (256**(flag_len - 10))
                flag = (ct - const - brute) % n 
                flag = (flag - ord('}')) * modinv(256, n)
                flagstr = long_to_bytes(flag % n)
                if all(32 <= ord(c) <= 128 for c in flagstr):
                    print chr(a) + chr(b) + chr(c) + flagstr

n = 20313365319875646582924758840260496108941009482470626789052986536609343163264552626895564532307

for msg in possible_inputs:
    print 'testing', msg
    crack_flag(msg, n)
```

Po uruchomieniu go, ostatecznie dostajemy flagę w swoje ręce:

`Congratz~~! Let's eat an apple pi <3.14159`

Pamiętamy żeby dopisać obciętą stałą część:

`hitcon{Congratz~~! Let's eat an apple pi <3.14159}`

Jesteśmy 314 punktów do przodu.

### ENG version

