## Kiuar (pwn, 200p)

    telnet ctf.sharif.edu 12432

###ENG
[PL](#pl-version)

First thing we receive in this task is request for proof of work - so we had to write a quick script calculating it for us.
After submitting it, we receive some non-ASCII bytes and a message telling us we have 10s to reply.

Saving those unknown bytes to file and checking it using `file` command, we find it's a zlib-compressed data: `Send your
QR code:`.

Sending anything afterwards tells us that we need to send exactly 200 bytes - and if we do it, the message tells us that
the input is not properly compressed. Finally, when we send zlib-compressed string "aaa" padded with zeros to 200 bytes,
we receive `Sorry, no decode delegate for this image :|`. Googling this message tells us that it's a generic ImageMagick
error message - apparently we need to send an image. At this point we were prertty certain it has to be zlib-compressed
image file containing QR code. Sending QR with "aaa" text gives us:
```
Processing the received command...
The output of your command is large, I only send 18 bytes of it :P 
Sorry, command not
```
So probably our text was executed as a command. Sending QR with `ls` confirms that - there was a `flag` file.
We still had to work around limitation of command size (200 bytes limit for QR image) and output limit of 18 bytes.
Finally, using `tail -c 40 flag` we were able to get the flag chunk by chunk.

###PL version

Pierwsze co dostajemy po połączeniu się z serwerem, to prośba o `proof of work`. Napisaliśmy więc skrypt realizujący ją,
po czym otrzymaliśmy trochę bajtów spoza ASCII i wiadomość, że mamy 10s na odpowiedź.

Po zapisaniu tych nieznanych bajtów do pliku i sprawdzeniu ich poleceniem `file` dowiedzieliśmy się, że to dane
skompresowane zlibem: `Send your QR code:`.

Wysłanie czegokolwiek mówi nam, że należy wysłac maksymalnie 200 bajtów. Po wysłaniu takiej właśnie ilości danych,
dowiadujemy się, że dane nie są poprawnie skompresowane. No to wysyłamy skompresowany zlibem tekst "aaa" z dorzuconymi
bajtami zerowymi na koniec, po czym otrzymujemy wiadomość `Sorry, no decode delegate for this image :|`. 
Wygooglanie tego tekstu mówi, że to zwykły błąd ImageMagick - w tym momencie domyśliliśmy się, że należy wysłać
skompresowany obrazek z QR. Wysyłamy więc QR z "aaa":
```
Processing the received command...
The output of your command is large, I only send 18 bytes of it :P 
Sorry, command not
```
Tekst jest więc pewnie wykonywany jako komenda. Potwierdziliśmy to wysyłając QR z `ls` - wylistowaliśmy plik `flag`.
Nadal trzeba było obejść ograniczenie wielkości komendy (200 bajtów na obrazek z QR) i na odpowiedź serwera (18
bajtów). Ostatecznie, używając `tail -c 40 flag` udało nam się kawałek po kawałku wyciągnąć flagę.
