## Keep Calm and CTF (forensics, 100p, 1064 solves)
Treść brzmi `My friend sends me pictures before every ctf. He told me this one was special.
Note: this flag doesn't follow the "flag{}" format`
Oprócz tego dostajemy dość przyjemnie wyglądający obrazek.

![](./kc&ctf.jpg)

Pierwszą rzeczą jaką robimy w takich sytuacjach jest przejrzenie hexdumpu, tak na wszelki wypadek. Może na końcu jest dopisany jeszcze jeden plik np. .zip albo .png z flagą. Ja robie to poleceniem `xxd img.jpg | less`.

```
0000000: ffd8 ffe0 0010 4a46 4946 0001 0101 0048  ......JFIF.....H
0000010: 0048 0000 ffe1 0058 4578 6966 0000 4d4d  .H.....XExif..MM
0000020: 002a 0000 0008 0003 0128 0003 0000 0001  .*.......(......
0000030: 0002 0000 0213 0003 0000 0001 0001 0000  ................
0000040: 8298 0002 0000 001d 0000 0032 0000 0000  ...........2....
0000050: 6831 6431 6e67 5f69 6e5f 346c 6d30 7374  h1d1ng_in_4lm0st
0000060: 5f70 6c61 316e 5f73 6967 6837 0000 ffdb  _pla1n_sigh7....
```

I mamy następną flagę.

