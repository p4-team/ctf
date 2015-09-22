## pcapin (forensics, 150p, 41 solves)

> We have extracted a pcap file from a network where attackers were present. We know they were using some kind of file transfer protocol on TCP port 7179. We're not sure what file or files were transferred and we need you to investigate. We do not believe any strong cryptography was employed.
> 
> Hint: The file you are looking for is a png
> pcapin_73c7fb6024b5e6eec22f5a7dcf2f5d82.pcap

Dostajemy [plik .pcap](pcapin.pcap). Jest w nim tylko jeden interesujący stream tcp, więc wyciągamy od razu z niego dane (tylko wysyłane z serwera do klienta, chociaż wygląda na to że klient wysyła dane tym samym protokołem) do [osobnego pliku](rawdata.bin).

W tym momencie rozpoczyna się analiza protokołu. Np. na pierwszy rzut oka widać powtarzający się fragment `00440000073200010000000000` w pierwszej części, a później wariacje na temat `00D423C60732001C00010000`.

Oszczędzimy może analizy krok po kroku (bo była długa i burzliwa), ale kluczowe było zauważenie że dane dzielą się na pakiety, i pierwszy word każdego pakietu to długość tego pakietu. Wtedy możemy podzielić odpowiedź na pakiety, i widzimy dodatkowo że odpowiedź kończy sie zawsze bajtami `END`.

Z tą wiedzą dekodujemy wszystkie pakiety po kolei, używamy trochę domyślności i dochodzimy do takiej oto struktury:

    struct packet {
        uint16_t length;
        uint16_t hash;
        uint16_t magic1;
        uint16_t conn_id;
        uint16_t seq_id;
        uint16_t unk2;
        uint8_t raw[10000];
    };

Napisaliśmy mały tool do dumpowania zawartości poszczególnych pakietów z tej struktury:

    msm@andromeda /cygdrive/c/Users/msm/Code/RE/CTF/2015-09-16 csaw/forensics_200_pcapin
    $ ./a.exe
    PACKET 0
     - size: 68 bytes
     - hash:  0
     - magic1: 732
     - conn_id:  1
     - seq_id:  0
     - unk2:  0
     - calculated hash: f9e9
     - rawdata:
        00 25 f2 a9 8d 96 8a 8c 84 9c 87 8d c7 89 8d 9f
        e9 f9 e9 f9 e9 f9 e9 f9 e9 f9 e9 f9 e9 f9 e9 f9
        e9 f9 e9 f9 e9 f9 e9 f9 e9 f9 e9 f9 e9 f9 e9 f9
        e9 f9 e9 f9 e9 f9 60 00
    PACKET 1
     - size: 68 bytes
     - hash:  0
     - magic1: 732
     - conn_id:  1
     - seq_id:  0
     - unk2:  0
     - calculated hash: f9e9
     - rawdata:
        00 00 28 a9 9a 98 84 89 85 9c c7 8d 80 9f e9 f9
        e9 f9 e9 f9 e9 f9 e9 f9 e9 f9 e9 f9 e9 f9 e9 f9
        e9 f9 e9 f9 e9 f9 e9 f9 e9 f9 e9 f9 e9 f9 e9 f9
        e9 f9 e9 f9 e9 f9 60 00
    PACKET 2
     - size: 68 bytes
     - hash:  0
     - magic1: 732
     - conn_id:  1
     - seq_id:  0
     - unk2:  0
     - calculated hash: f9e9
     - rawdata:
        00 00 15 c1 86 8c 9d 9f 80 95 8c d7 8d 98 9d f9
        e9 f9 e9 f9 e9 f9 e9 f9 e9 f9 e9 f9 e9 f9 e9 f9
        e9 f9 e9 f9 e9 f9 e9 f9 e9 f9 e9 f9 e9 f9 e9 f9
        e9 f9 e9 f9 e9 f9 60 00
    (...)
    PACKET 9
     - size: 212 bytes
     - hash: 4567
     - magic1: 732
     - conn_id: 1c
     - seq_id:  0
     - unk2:  0
     - calculated hash: 3f50
     - rawdata:
        d9 6f 1e 78 5d 35 4a 35 50 3f 50 32 19 77 14 6d
        50 3f 51 78 50 3f 50 28 58 39 50 3f 50 a7 e0 b2
        78 3f 50 3f 56 5d 1b 78 14 3f af 3f af 3f af 9f
        ed 98 c3 3f 50 2a 26 76 14 7e 04 47 cc d2 cd 48
        08 6b 87 89 90 40 63 cb 51 79 0a 2b 4b 2d 33 ef
        40 ce f9 7e ff 9d 32 1e 4a 34 16 9c 96 2d 1b b3
        19 77 14 90 76 5d 28 7b d9 1a 01 cb 4a 5d d9 22
        73 09 7c 67 ff 5d 47 b6 75 9f 72 fe 30 28 75 1d
        70 ed 6b 7c 83 a6 a7 38 63 d8 5e 05 98 3f d3 da
        0d 41 8f 08 8f d8 cc 06 ab a3 e5 08 2b 92 e3 c9
        0a d4 3c 7a da 97 78 3a e5 9f e4 93 dc 2a 6b 48
        e2 5f b3 79 a2 35 5b 86 46 23 1c e4 e7 e1 fa f2
        75 d4 d4 d4 21 4e 68 b2
     (...)

Co się rzuca w oczy bardzo - powtarzający sie padding na początku (e9f9). Dalej, wiemy że dane to plik .png - pierwszy pakiet z danymi to packet 9 (domyślamy się tego, bo jest w odpowiedzi na drugi request od klienta, oraz ma troche inną strukture niż peirwsze pakiety - przypominające headery jakieś).

Więc, kierowani intuicją, xorujemy pierwsze bajty pakietu 9 z nagłówkiem .png:

    >>> ' d9 6f 1e 78 5d 35 4a 35 50 3f 50 32 19 77 14 6d'.replace(' ', '')
    'd96f1e785d354a35503f50321977146d'
    >>> ' d9 6f 1e 78 5d 35 4a 35 50 3f 50 32 19 77 14 6d'.replace(' ', '').decode('hex')
    '\xd9o\x1ex]5J5P?P2\x19w\x14m'
    >>> raw = ' d9 6f 1e 78 5d 35 4a 35 50 3f 50 32 19 77 14 6d'.replace(' ', '').decode('hex')
    >>> png = '89504E470D0A1A0A0000000D49484452'.decode('hex')
    >>> def xor(a, b):
    ...     return ''.join(chr(ord(ac) ^ ord(bc)) for ac, bc in zip(a, b))
    ...
    >>> xor(raw, png)
    'P?P?P?P?P?P?P?P?'
    >>> xor(raw, png).encode('hex')
    '503f503f503f503f503f503f503f503f'

W tym momencie możemy uścisnąć sobie dłonie - praktycznie rozwiązaliśmy zadanie. Pozostaje pytanie, skąd bierze się liczba z którą xorujemy - nie jest to stała, niestety. Ale kierowani znowu intuicją, domyślamy się że 'padding' z pierwszych pakietów to xorowane null bajty (długość się zgadza).

Ale od czego zależy ta liczba? W pakiecie mamy ciekawą daną z której jeszcze nie skorzystaliśmy - oznaczoną w mojej strukturze jako 'hash'. Kiedy ta liczba jest równa 0, xorujemy dane z e9f9. Kiedy ta liczba jest równa 4567 xorujemy z 503f. W jaki sposób może być wyprowadzany wynikowy hash? Zgadnijmy...:

    >>> hex(0x503f + 0x4567)
    '0x95a6'

Jest to proste dodawanie wartości w polu 'hash' oraz magicznej stałej. Zaiste silne szyfrowanie ;).

Pozostaje dopracować nasz parser, i mamy wynik:

    msm@andromeda /cygdrive/c/Users/msm/Code/RE/CTF/2015-09-16 csaw/forensics_200_pcapin
    $ ./a.exe -tc
    PACKET 0
     - size: 68 bytes
     - hash:  0
     - magic1: 732
     - conn_id:  1
     - seq_id:  0
     - unk2:  0
     - calculated hash: f9e9
     - rawdata:
        e9 dc 1b 50 64 6f 63 75 6d 65 6e 74 2e 70 64 66   ...Pdocument.pdf
        00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
        00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
        00 00 00 00 00 00 89 f9                           ........
    PACKET 1
     - size: 68 bytes
     - hash:  0
     - magic1: 732
     - conn_id:  1
     - seq_id:  0
     - unk2:  0
     - calculated hash: f9e9
     - rawdata:
        e9 f9 c1 50 73 61 6d 70 6c 65 2e 74 69 66 00 00   ...Psample.tif..
        00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
        00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
        00 00 00 00 00 00 89 f9                           ........
    (...)
    PACKET 9
     - size: 212 bytes
     - hash: 4567
     - magic1: 732
     - conn_id: 1c
     - seq_id:  0
     - unk2:  0
     - calculated hash: 3f50
     - rawdata:
        89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
        00 00 01 47 00 00 00 17 08 06 00 00 00 98 b0 8d   ...G............
        28 00 00 00 06 62 4b 47 44 00 ff 00 ff 00 ff a0   (....bKGD.......
        bd a7 93 00 00 15 76 49 44 41 54 78 9c ed 9d 77   ......vIDATx...w
        58 54 d7 b6 c0 7f 33 f4 01 46 5a 14 1b 12 63 d0   XT....3..FZ...c.
        10 f1 a9 41 af a2 62 21 1a 0b 46 a3 c6 12 4b 8c   ...A..b!..F...K.
        49 48 44 af 26 62 78 44 89 25 51 f4 1a 62 89 1d   IHD.&bxD.%Q..b..
        23 36 2c 58 af 62 17 89 25 a0 22 c1 60 17 25 22   #6,X.b..%.".`.%"
        20 d2 3b 43 d3 99 f7 07 33 e7 0e 3a c8 00 83 e5    .;C....3..:....
        5d 7e df 37 df e7 9c 39 fb 9c b5 37 7b ad b3 f6   ]~.7...9...7{...
        5a eb 6c 45 8a a8 28 05 b5 a0 b4 ac 8c 15 3b 77   Z.lE..(.......;w
        b2 60 e3 46 f2 0a 0b b9 16 1c 4c db b7 de aa cd   .`.F......L.....
        25 eb 84 eb 71 71 38 8d                           %...qq8.

Jak widać wszystkie dane z png zostały pięknie przeczytane. Pozostaje zapisać pakiety od 9 do końca w pliku i odczytać znajdujacy się tam [obrazek png](pcapin.png).

Zadanie rozwiązane.

Źródła całego dekodera (nie wiem po co napisanego, skoro prawdopodobnie żaden program na świecie nie używa takiego formatu do komunikacji, ale lubimy pisać parsery :P) znajdują się w pliku [parser.c](parser.c)
