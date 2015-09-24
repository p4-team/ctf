## FTP (re, 300p, 214 solves)

> We found an ftp service, I'm sure there's some way to log on to it.
> 
> nc 54.172.10.117 12012
> [ftp_0319deb1c1c033af28613c57da686aa7](ftp)

### PL Version
`for ENG version scroll down`

Pobieramy zalinkowany plik i ładujemy do IDY. Jest to faktycznie, zgodnie z opisem, serwer FTP.

W stringach znajdujących się w binarce znajdujemy napis zawierający wszystkie komendy wspierane przez serwer (w helpie):

> USER PASS PASV PORT
> NOOP REIN LIST SYST SIZE
> RETR STOR PWD CWD

Przeglądamy chwilę funkcje znajdujące się w binarce, i najciekawsza wydaje sie ta odpowiadająca "nieudokumentowanej" funkcji RDF:

    mov     [rbp+ptr], rax
    mov     esi, offset aR  ; "r"
    mov     edi, offset filename ; "re_solution.txt"
    call    _fopen
    ; (...)
    mov     rdx, [rbp+stream]
    mov     rax, [rbp+ptr]
    mov     rcx, rdx        ; stream
    mov     edx, 1          ; n
    mov     esi, 28h        ; size
    mov     rdi, rax        ; ptr
    call    _fread
    mov     rax, [rbp+var_18]
    mov     eax, [rax]
    mov     rdx, [rbp+ptr]
    mov     rsi, rdx
    mov     edi, eax
    call    send_string_to_client

Niestety, wywołanie tej funkcji wymaga autentykacji do systemu. Patrzymy więc na funkcje odpowiadającą za zalogowanie.

Wygląda ona mniej więcej tak (po ręcznym przepisaniu do C)

    unsigned hash(char *txt)
    {
      int v = 5381;
      for (int i = 0; txt[i]; ++i )
        v = 33 * v + txt[i];
      return (unsigned)v;
    }

    bool login_ok(char *username, char *password) {
         return strcmp(username, "blankwall") == 0 && hash(password) == 3548828169;
    }

(A przynajmniej to ważne fragmenty z tej funkcji, samo wczytywanie i wysyłanie tekstu do klienta pominęliśmy).

Funkcja hashująca jest jak widać bardzo prosta, więc można było spróbować ją złamać. I nie byłoby to bardzo trudne, ale poszliśmy prostszą drogą - zauważyliśmy że jest "monotoniczna" (czyli każdy kolejny znak w haśle ma coraz mniejszy wpływ na wynik hasha, czyli możemy zgadywać hasło znak po znaku). Napisaliśmy do tego narzędzie:

    int main(int argc, char *argv[]) {
        char c[1000];
        puts("3548828169");
        unsigned rzecz = rzeczy(argv[1]); 
        printf("%u\n", rzecz);
        if (rzecz > 3548828169) {
            puts("2much");
        } else if (rzecz < 3548828169) {
            puts("2low");
        } else {
            puts("just enough");
        }
    }

Przykładowa interakcja z programem (z komentarzami):

    msm@andromeda /cygdrive/c/Users/msm/Code/RE/CTF/2015-09-16 csaw/pwn_300_ftp
    $ ./a.exe Taaaaa
    3548828169
    3538058430
    2low    (czyli `Ta` to za niski prefiks)
    
    msm@andromeda /cygdrive/c/Users/msm/Code/RE/CTF/2015-09-16 csaw/pwn_300_ftp
    $ ./a.exe Tlaaaa
    3548828169
    3551103561
    2much    (czyli `Tl` to za wysoki prefiks)
    
    msm@andromeda /cygdrive/c/Users/msm/Code/RE/CTF/2015-09-16 csaw/pwn_300_ftp
    $ ./a.exe Tkaaaa
    3548828169
    3549917640
    2much    (czyli `Tk` to za wysoki prefiks)
    
    msm@andromeda /cygdrive/c/Users/msm/Code/RE/CTF/2015-09-16 csaw/pwn_300_ftp
    $ ./a.exe Tjaaaa
    3548828169
    3548731719
    2low     (czyli `Tj` to za niski prefiks)
    
    msm@andromeda /cygdrive/c/Users/msm/Code/RE/CTF/2015-09-16 csaw/pwn_300_ftp
    $ ./a.exe TkCaaa
    3548828169
    3548839530
    2much    (czyli `Tk` jednak było ok, teraz próbujemy zmniejszyć trzeci znak)
    
    msm@andromeda /cygdrive/c/Users/msm/Code/RE/CTF/2015-09-16 csaw/pwn_300_ftp
    $ ./a.exe TkBaaa
    3548828169
    3548803593
    2low     (czyli `TkC` jest dobrym strzałem, bo `TkCa` jest za wysokie, `TkBa` już jest za niskie)
    
    (itd, itd)
    
W ten sposób trafiamy na hasło - TkCWRy. Przy wpisywaniu go do nc trzeba pamiętać żeby zakończyć wpisywanie za pomocą C-d zamiast entera, bo inaczej hash liczy się ze znakiem nowej linii i wychodzi błędny.

Więc mamy hasło i usera, wystarczy wykonać komendę pobierającą flagę:

    $ nc -vv 54.172.10.117 12012
    Connection to 54.172.10.117 12012 port [tcp/*] succeeded!
    Welcome to FTP server
    USER blankwall
    Please send password for user blankwall
    PASS TkCWRylogged in
    RDF
    flag{n0_c0ok1e_ju$t_a_f1ag_f0r_you}

Gotowe.

### ENG Version

We download linked file and we load it with IDA. It is, in fact, a FTP server, just as described.

In the strings in the binary we find all the commands supported by server (in help):

> USER PASS PASV PORT
> NOOP REIN LIST SYST SIZE
> RETR STOR PWD CWD

We look around the functions in the binary and the most interesting one seems to be the "undocumented" RDF function:

    mov     [rbp+ptr], rax
    mov     esi, offset aR  ; "r"
    mov     edi, offset filename ; "re_solution.txt"
    call    _fopen
    ; (...)
    mov     rdx, [rbp+stream]
    mov     rax, [rbp+ptr]
    mov     rcx, rdx        ; stream
    mov     edx, 1          ; n
    mov     esi, 28h        ; size
    mov     rdi, rax        ; ptr
    call    _fread
    mov     rax, [rbp+var_18]
    mov     eax, [rax]
    mov     rdx, [rbp+ptr]
    mov     rsi, rdx
    mov     edi, eax
    call    send_string_to_client

Unfortunately, calling this function requires authentication. Therefore we check the login function.
It looks like this (after re-writing it to C):

    unsigned hash(char *txt)
    {
      int v = 5381;
      for (int i = 0; txt[i]; ++i )
        v = 33 * v + txt[i];
      return (unsigned)v;
    }

    bool login_ok(char *username, char *password) {
         return strcmp(username, "blankwall") == 0 && hash(password) == 3548828169;
    }

(Those are at lest the important parts, without the I/O operations).

As can be seen the hash function is very simple so we could try to break it. It would not be very difficult, however we decided to take an even easier path - we noticed that the hash function is "monotonic" (every next character in the password has smaller influence on the ouput hash, so we can guess the password character by character). We prepared a tool for this:

    int main(int argc, char *argv[]) {
        char c[1000];
        puts("3548828169");
        unsigned rzecz = rzeczy(argv[1]); 
        printf("%u\n", rzecz);
        if (rzecz > 3548828169) {
            puts("2much");
        } else if (rzecz < 3548828169) {
            puts("2low");
        } else {
            puts("just enough");
        }
    }

An example of interaction with the script (with comments):

    msm@andromeda /cygdrive/c/Users/msm/Code/RE/CTF/2015-09-16 csaw/pwn_300_ftp
    $ ./a.exe Taaaaa
    3548828169
    3538058430
    2low    (so `Ta` is too low for a prefix)
    
    msm@andromeda /cygdrive/c/Users/msm/Code/RE/CTF/2015-09-16 csaw/pwn_300_ftp
    $ ./a.exe Tlaaaa
    3548828169
    3551103561
    2much    (so `Tl` is too high for a prefix)
    
    msm@andromeda /cygdrive/c/Users/msm/Code/RE/CTF/2015-09-16 csaw/pwn_300_ftp
    $ ./a.exe Tkaaaa
    3548828169
    3549917640
    2much    (so `Tk` is too high for a prefix)
    
    msm@andromeda /cygdrive/c/Users/msm/Code/RE/CTF/2015-09-16 csaw/pwn_300_ftp
    $ ./a.exe Tjaaaa
    3548828169
    3548731719
    2low    (so `Tj` is too low for a prefix)
    
    msm@andromeda /cygdrive/c/Users/msm/Code/RE/CTF/2015-09-16 csaw/pwn_300_ftp
    $ ./a.exe TkCaaa
    3548828169
    3548839530
    2much    (so `Tk` was in fact OK, so now we try to lower the third character)
    
    msm@andromeda /cygdrive/c/Users/msm/Code/RE/CTF/2015-09-16 csaw/pwn_300_ftp
    $ ./a.exe TkBaaa
    3548828169
    3548803593
    2low     (so `TkC` is a good guess, since `TkCa` is too high and `TkBa` is too low)
    
    (etc, etc)
    
This was we get the password - TkCWRy. It's worth noting to provide the input via nc and end it with C-d instead of Enter, otherwise the hash will include newline character and we get a wrong password.

So we have a password and username, we just need to issue a command to get the flag:

    $ nc -vv 54.172.10.117 12012
    Connection to 54.172.10.117 12012 port [tcp/*] succeeded!
    Welcome to FTP server
    USER blankwall
    Please send password for user blankwall
    PASS TkCWRylogged in
    RDF
    flag{n0_c0ok1e_ju$t_a_f1ag_f0r_you}

Done.
