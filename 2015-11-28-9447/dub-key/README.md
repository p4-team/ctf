## dub-key (crypto, 120p)

> My friend set up a small signing scheme, however she won't let me sign stuff. Can you get it signed?
>
> Find it at dub-key-t8xd5pn6.9447.plumbing port 9447
>
> [dub-key.py](dub-key.py)

###PL
[ENG](#eng-version)

Rozpoczeliśmy analizę algorytmu podpisywania i jego własności
(w skrócie - podpisywanie polega na tym że zmieniamy wiaodmość w graf, i podpis to
iloczyn długości wszystkich cykli w wiadomości). Niestety, nie udało nam się skończyć pisać pełnego ataku
przed końcem CTFa, ale w ostatnich godzinach zdecydowaliśmy się wykonać trywialny atak na algorytm podpisywania.

Otóż w tym zadaniu możemy podpisać dowolną wiadomość poza jedną - tą którą mamy podpisać żeby dostać flagę.
Zauważyliśmy, że jeśli zmienimy tylko jeden bajt w wiadomości i podpiszemy go, to jest spora szansa że podpis się nie zmieni
Oszacowaliśmy tą szansę jako pesymistycznie 1/(256*e), ale prawdopodobnie znacznie większą - i rzeczywiście, w praktyce już
po kilkudziesięciu sprawdzeniach udało się.

Pomysł sprowadza się do:

    msg = odbierz_wiadomość_do_podpisania()
    msg1 = msg[-1] + '\x00'
    sig1 = podpisz(msg1)
    wyślij_podpis(sig1)

Tak więc nasz cały kod atakujący wyglądał tak:

```python
import hashlib
import socket
import string
import itertools
import base64

def pow(init):
    for c in itertools.product(string.lowercase, repeat=6):
        dat = init + ''.join(c)
        hash = hashlib.sha1(dat)
        if hash.digest().endswith('\x00\x00\x00'):
            return dat

def recv():
    return s.recv(99999)
    return r

def send(msg):
    s.send(msg)

while True:
    HOST, PORT = 'dub-key-t8xd5pn6.9447.plumbing', 9447
    s = socket.socket()
    s.connect((HOST, PORT))
    inp = recv()
    print inp
    p = pow(inp)
    send(p)
    r = recv()
    tosign = recv().split("\n")[0]
    dat = base64.b64decode(tosign)
    dat = dat[:-1] + '\x00'
    send('1\n')
    send(base64.b64encode(dat))
    r = recv() # podpisane dane
    t = recv() # sign something
    send('2\n')
    send(r)
    print recv(), recv(), recv()
```

I, co zaskakujące, zadziałał za pierwszym razem.


### ENG version
