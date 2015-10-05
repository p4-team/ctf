## FTP2 (pwn, 300p, ? solves)

> nc 54.172.10.117 12012
> [ftp_0319deb1c1c033af28613c57da686aa7](ftp)

Pobieramy zalinkowany plik i ładujemy do IDY. Jest to faktycznie, zgodnie z opisem, serwer FTP - ten sam co w zadaniu FTP (re 300).

Wiemy że flaga znajduje się gdzieś na serwerze. Mamy też username i hasło.

Spróbowaliśmy najpierw dorwać się do serwera FTP w cywilizowany sposób - po prostu łącząc się klientem FTP. Niestety, nie wyszło (ani filezilla, ani webowe klienty nie dały rady - jednak widać ten serwer FTP nie był tak kompatybilny jak moglibyśmy liczyć).

Napisaliśmy więc trywialnego klienta FTP, łączącego się z serwerem:

client.py:
```
import socket
import subprocess

HOST = '54.175.183.202' 
s = socket.socket()
s.connect((HOST, 12012))

def send(t):
    print t
    s.send(t)

def recv():
    msg = s.recv(9999)
    print msg
    return msg

recv()
send('USER blankwall\n')
recv()
send('PASS TkCWRy')
recv()
recv()

while True:
    print ">>",
    i = raw_input() + '\n'
    send(i)
    msg = recv()
    if 'PASV succesful' in msg:
        port = int(msg.split()[-1])
        print port
        subprocess.Popen(['python', 'process.py', str(port)])
```

process.py:
```
import socket
import sys

HOST = '54.175.183.202' 

port = int(sys.argv[1])
t = socket.socket()
t.connect((HOST, port))
print t.recv(99999999)
```

I tutaj zdarzyła się dziwna rzecz - wylistowaliśmy katalog po połączeniu się (poleceniem LIST), i widzimy plik o nazwie "flag" w cwd.

Następnie wykonaliśmy polecenie RETR, żeby pobrać ten plik. I... dostaliśmy flagę:

`flag{exploiting_ftp_servers_in_2015}`

Było to bardzo niespodziewane, i albo to jakiś błąd autorów zadania, albo ktoś wyexploitował zadanie "po bożemu" i (nieświadomie?) zostawił flagę w pliku na serwerze czytalnym dla każdego.

Tak czy inaczej, tanie 300 punktów do przodu.
