##randBox (crypto, 120p)

###PL
[ENG](#eng-version)

`nc randBox-iw8w3ae3.9447.plumbing 9447`

```
Alphabet is '0123456789abcdef', max len is 64
You need to send a string that encrypts to '787fadc8d1944a35b3ed9d1433a9060f'
Guess 0/21 (Round 1/10)
```

Zadanie polegało na połączeniu się z serwerem a następnie na złamaniu 10 szyfrów (w praktyce tylko 7 było unikalnych), przy użyciu nie więcej niż 21 prób.
Złamanie każdego szyfru należało udowodnić poprzez wysłanie wiadomości, która po zakodowaniu da wylosowany przez serwer ciąg znaków.
Kod całego rozwiązania znajduje sie [tutaj](randBox.py) a sesja rozwiązująca [tutaj](session.txt)

####Szyfr 1

Pierwszy szyfr to standardowy szyfr Cezara, więc do jego złamania potrzeba nam informacji o `przesunięciu`. Uzyskujemy ją, poprzez wysłanie na serwer pojedyńczego znaku `0`.

```python
def breakLevel1(ct, s):
    # caesar cipher
    send_via_nc(s, "0")
    data = s.recv(1024)[:-1]
    shift = int(data, 16)
    result = "".join([format((int(letter, 16) - shift) % 16, "x") for letter in ct])
    send_via_nc(s, result)
```

####Szyfr 2

Drugi szyfr to cykliczne przesunięcie wejściowego ciągu o losową liczbę pozycji, zależną od długości wejścia, więc do jego złamania potrzebujemy informacji o tym o ile pozycji nastąpi przeunięcie. Informacje uzyskujemy poprzez wysłanie ciągu `0` oraz jednej `1` (o długości takiej jak oczekiwany ciphertext) a następnie policzenie o ile została przesunięta `1`.

```python
def breakLevel2(ct, s):
    # circular shifting input by some random number
    send_via_nc(s, "1" + ("0" * (len(ct) - 1)))
    data = s.recv(1024)[:-1]
    shift = data.index("1")
    result = ct[shift:] + ct[:shift]
    send_via_nc(s, result)
```

####Szyfr 3,4,5

Szyfry 3,4,5 to szyfry podstawieniowe i do ich złamania potrzebujemy pobrać z serwera informacje o tym, jak wygląda tablica zamian. Robimy to poprzez wysłanie całego alfabetu i odczytanie jak zostały zamienione znaki.

```python
def breakLevel3(ct, s):
    # substitution cipher
    initial = "0123456789abcdef"
    send_via_nc(s, initial)
    data = s.recv(1024)[:-1]
    decoder = {data[i]: initial[i] for i in range(len(initial))}
    result = "".join([decoder[letter] for letter in ct])
    send_via_nc(s, result)
```

####Szyfr 6

Szyfr 6 przypomina szyfr Cezara, ale przesunięcie jest liczone per znak a nie dla całego ciągu identycznie. Więc np. pierwszy znak tekstu jest przesunięty o X, drugi o Y, trzeci o Z. Przesunięcia uzyskujemy wysyłając ciąg 0 o długości ciphertextu i z niego odczytujemy przesuniecia dla każdej pozycji.

```python
def breakLevel6(ct, s):
    # shifting each number by some distance
    initial = "0" * len(ct)
    send_via_nc(s, initial)
    data = s.recv(1024)[:-1]
    shifts = [int(data[i], 16) for i in range(len(ct))]
    result = "".join([format((int(ct[i], 16) - shifts[i]) % 16, "x") for i in range(len(ct))])
    send_via_nc(s, result)
```

####Szyfr 7

Szyfr 7 został przez nas zwyczajnie zbrutowany, bo nie mieliśmy pomysłu na regułę. Szyfr wyliczał kolejny element ciphertextu na podstawie dwóch poprzednich elementów plaintextu (z losowym elementem na pozycji -1), w większości sytuacji poprzez ich dodanie/odjęcie. Niemniej zasada kiedy odejmować a kiedy dodawać nie była dla nas oczywista, więc wysłaliśmy do serwera zapytania postaci `000102030405...`, `10111213141516...`, `20212223242526...` i na podstawie wyników odczytaliśmy mapę wszystkich możliwych podstawień - tzn. dla każdej `poprzedniej` liczby wiedzieliśmy na co zostanie zamieniony każdy symbol. Jedyna brakująca informacja to wartość losowa na pozycji -1 która jest wykorzystywana aby wyliczyć 1 znak ciphertextu. Odzyskujemy ją poprzez wysłanie `0` a potem odczytanie na podstawie wyniku dla jakiego `poprzednika` mogliśmy uzyskać taki wynik.

```python
    initial = "0"
    send_via_nc(s, initial)
    data = s.recv(1024)
    data = data[:data.index("\n")]
    current_number = find_start_number(cracking_map, data)
    result = ""
    for letter in ct:
        generator = find_generator(cracking_map, current_number, letter)
        result += generator
        current_number = generator
    send_via_nc(s, result)
```

####Szyfr 8

Szyfr 8 polegał na sumowaniu poprzednich wyrazów modulo 16, z losową wartością na pozycji -1. Losową wartość odzyskujemy wysyłając 0 a następnie odczytując ją bezpośrednio z wyniku. Następnie kodujemy dane licząc jakiej wartości `brakuje` nam aby uzyskać spodziewany znak ciphertextu po dodaniu jej do poprzedniej modulo 16.

```python
def breakLevel8(ct, s):
    # adding current number to previous modulo 16
    initial = "0"
    send_via_nc(s, initial)
    data = s.recv(1024)
    data = data[:data.index("\n")]
    previous = int(data, 16)
    result = ""
    for number in ct:
        current = int(number, 16)
        missing = (current - previous) % 16
        result += format(missing, "x")
        previous = current
    send_via_nc(s, result)
```

####Szyfr 9

Szyfr 9 byl szyfrem podstawieniowym ze zmianą kolejności bajtów w słowie. Jeśli np. X kodowany był przez 1 a Y przez 0 to zakodowanie XY dawało 01. Aby odczytać mapę podstawień wysyłaliśmy cały alfabet a następnie odczytywaliśmy podstawienia zamieniając pary miejscami.

```python
def breakLevel9(ct, s):
    # substitution with byte swap, x->1, y->2, xy -> 21
    initial = "0123456789abcdef"
    send_via_nc(s, initial)
    data = s.recv(1024)
    data = data[:data.index("\n")]
    substitution = {}
    for i in range(0, len(initial) - 1, 2):
        substitution[initial[i + 1]] = data[i]
        substitution[initial[i]] = data[i + 1]
    result = ""
    for i in range(0, len(ct) - 1, 2):
        first = ct[i]
        second = ct[i + 1]
        result += substitution[second] + substitution[first]
    send_via_nc(s, result)
```

W trakcie trwania konkursu kolejność szyfrów w zadaniu uległa przemieszaniu a niektóre szyfry były użyte kilkukrotnie stąd unikalnych szyfrów jest tylko 7 a nie 10.

```
You need to send a string that encrypts to 'd689c1a78e419dc1043ff07a0afc01d8'
Guess 18/21 (Round 10/10)

ciphertext = d689c1a78e419dc1043ff07a0afc01d8
sending 0
sending 17f6ab16e045c1dcc8b4bbc66c3ffe3b
Guess 19/21 (Round 10/10)
d689c1a78e419dc1043ff07a0afc01d8
You got it!
9447{crYpt0_m4y_n0T_Be_S0_haRD}
```
	
### ENG version

`nc randBox-iw8w3ae3.9447.plumbing 9447`

```
Alphabet is '0123456789abcdef', max len is 64
You need to send a string that encrypts to '787fadc8d1944a35b3ed9d1433a9060f'
Guess 0/21 (Round 1/10)
```

The task was to connect with the server and break 10 ciphers (in fact only 7 were unique), using no more than 21 tries.
Breaking each cipher was proven by sending a message that would encode to the ciphertext selected by server.
Whole solution is [here](randBox.py) and winning session [here](session.txt)

####Cipher 1

First cipher was a standard Caesar cipher, so we need only the information about the `shift`. We get is by sending a single `0` to the server and we get shift as an answer.

```python
def breakLevel1(ct, s):
    # caesar cipher
    send_via_nc(s, "0")
    data = s.recv(1024)[:-1]
    shift = int(data, 16)
    result = "".join([format((int(letter, 16) - shift) % 16, "x") for letter in ct])
    send_via_nc(s, result)
```

####Cipher 2

Second cipher was a cyclic shift of the input by a random number of positions, dependent on the length of input, so to break it we need to know how many places will the shift be. We get this by sending data with all `0` and a single `1` (with length the same as expected output ciphertext) and the couting how many places the `1` has moved.

```python
def breakLevel2(ct, s):
    # circular shifting input by some random number
    send_via_nc(s, "1" + ("0" * (len(ct) - 1)))
    data = s.recv(1024)[:-1]
    shift = data.index("1")
    result = ct[shift:] + ct[:shift]
    send_via_nc(s, result)
```

####Cipher 3,4,5

Ciphers 3,4,5 were all substitution ciphers and to break them we need to get the substitution table from the server. We do this by sending whole alphabet and reading how each character changed.

```python
def breakLevel3(ct, s):
    # substitution cipher
    initial = "0123456789abcdef"
    send_via_nc(s, initial)
    data = s.recv(1024)[:-1]
    decoder = {data[i]: initial[i] for i in range(len(initial))}
    result = "".join([decoder[letter] for letter in ct])
    send_via_nc(s, result)
```

####Cipher 6

Cipher 6 is similar to Caesar cipher but the shifts are per position in the plaintext rather than constant for whole text. For example first character is shifted by X, second by Y etc. To get the shifts information we send data with `0` (the same length as expected ciphertext) and we read the shifts on each position directly.

```python
def breakLevel6(ct, s):
    # shifting each number by some distance
    initial = "0" * len(ct)
    send_via_nc(s, initial)
    data = s.recv(1024)[:-1]
    shifts = [int(data[i], 16) for i in range(len(ct))]
    result = "".join([format((int(ct[i], 16) - shifts[i]) % 16, "x") for i in range(len(ct))])
    send_via_nc(s, result)
```

####Cipher 7

Cipher 7 was simply brute-forced by us, because we couldn't figure out the rule. The cipher was calculating next ciphertext element by last two plaintext elements (with random value at position -1), for the most part this was either by adding or subtracting them. However, we couldn't figure out when to add and when to subtract so we simply extracted this from server.
We sent requests `000102030405...`, `10111213141516...`, `20212223242526...` and from answers we created a substitution table - for each `previous` value, for each `current` value we knew what will be the ciphertext element. The only missing part was the random value at position -1, which we got by sending `0` and checking which `previous` value would give us the result we got.

```python
    initial = "0"
    send_via_nc(s, initial)
    data = s.recv(1024)
    data = data[:data.index("\n")]
    current_number = find_start_number(cracking_map, data)
    result = ""
    for letter in ct:
        generator = find_generator(cracking_map, current_number, letter)
        result += generator
        current_number = generator
    send_via_nc(s, result)
```

####Cipher 8

Cipher 8 was adding all previous values of plaintext modulo 16, with random value at position -1. The random value we extract by sendind `0` and taking them directly from result. For the solution we simply encode data, couting how much we are `missing` to get the proper ciphertext value.

```python
def breakLevel8(ct, s):
    # adding current number to previous modulo 16
    initial = "0"
    send_via_nc(s, initial)
    data = s.recv(1024)
    data = data[:data.index("\n")]
    previous = int(data, 16)
    result = ""
    for number in ct:
        current = int(number, 16)
        missing = (current - previous) % 16
        result += format(missing, "x")
        previous = current
    send_via_nc(s, result)
```

####Cipher 9

Cipher 9 was a substitution cipher with shifting bytes in two-byte words. If X was encoded by 1 and Y by 0 then XY would give 01. To get the substitution map we sent whole alphabet and read the substitutions by shifting bytes in pairs.

```python
def breakLevel9(ct, s):
    # substitution with byte swap, x->1, y->2, xy -> 21
    initial = "0123456789abcdef"
    send_via_nc(s, initial)
    data = s.recv(1024)
    data = data[:data.index("\n")]
    substitution = {}
    for i in range(0, len(initial) - 1, 2):
        substitution[initial[i + 1]] = data[i]
        substitution[initial[i]] = data[i + 1]
    result = ""
    for i in range(0, len(ct) - 1, 2):
        first = ct[i]
        second = ct[i + 1]
        result += substitution[second] + substitution[first]
    send_via_nc(s, result)
```

During the competition the ordering of ciphers was changed and some ciphers were used multiple times, hence there were only 7 unique ciphers, not 10.

```
You need to send a string that encrypts to 'd689c1a78e419dc1043ff07a0afc01d8'
Guess 18/21 (Round 10/10)

ciphertext = d689c1a78e419dc1043ff07a0afc01d8
sending 0
sending 17f6ab16e045c1dcc8b4bbc66c3ffe3b
Guess 19/21 (Round 10/10)
d689c1a78e419dc1043ff07a0afc01d8
You got it!
9447{crYpt0_m4y_n0T_Be_S0_haRD}
```