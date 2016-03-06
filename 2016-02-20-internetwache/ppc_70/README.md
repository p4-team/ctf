## A numbers game II (PPC/Crypto, 70p)

	Description: Math is used in cryptography, but someone got this wrong. Can you still solve the equations? 
	Hint: You need to encode your answers. 
	
###ENG
[PL](#pl-version)

Server sends input as:

	Hi, I like math and cryptography. Can you talk to me?!
	Level 1.: 4.4.5.3.3.3.3.3.3.3.6.4.3.3.3.3.3.4.3.4.3.4.3.3.3.3.3.3.3.4.6.4.3.3.3.3.3.3.6.4.3.4.4.5
	
And we are also given the encryption code:

```python
    def encode(self, eq):
        out = []
        for c in eq:
            q = bin(self._xor(ord(c),(2<<4))).lstrip("0b")
            q = "0" * ((2<<2)-len(q)) + q
            out.append(q)
        b = ''.join(out)
        pr = []
        for x in range(0,len(b),2):
            c = chr(int(b[x:x+2],2)+51)
            pr.append(c)
        s = '.'.join(pr)
        return s
```

The goal is to decrypt the task, solve it and then send encrypted answer.
First we split the encryption into two functions (one loop in each) and then wrote decryption for each one of them.
We replaced constants like (2<<4) for their numeric values for readibility.

First part of the encryption function takes each character of the input, xors it with static key 32, converts this to binary and add 0 padding so that this binary representation has always 8 digits.

Therefore for the decryption we can simply slice the input to get 8-digit long binary strings, then we treat each one of them as integers in base-2 (this gets rid of 0 padding) and xor with static key 32 (since `a xor b xor b = a`).

```python
def encode1(eq):
    out = []
    for c in eq:
        q = bin((ord(c) ^ 32)).lstrip("0b")
        q = "0" * (8 - len(q)) + q
        out.append(q)
    b = ''.join(out)
    return b


def decode1(b):
    result = []
    for i in range(0, len(b), 8):
        q = b[i:i + 8]
        q = chr(int(q, 2) ^ 32)
        result.append(q)
    return "".join(result)
```

Second part of encryption takes the binary string we got from the first part, then slices it into 2-digit parts, treats each one as integer in baes-2, adds 51 and casts this to char. Then all chars are concatenated with dot as separator.

Therefore the decryption of this part splits the input by dot to get characters, then casts the char to integer and subtracts 51, converts the result to 2-digit long binary number and then joins all those numbers into a single string.

```python
def encode2(b):
    pr = []
    for x in range(0, len(b), 2):
        c = chr(int(b[x:x + 2], 2) + 51)
        pr.append(c)
    s = '.'.join(pr)
    return s


def decode2(task):
    return "".join("{0:02b}".format((ord(c) - 51)) for c in task.split("."))
```

With this we can now decode the input, which turns out to be exactly the same as for previous task `A numbers game`, so we use the same procedure to solve the tasks, and we use the provided `encrypt()` function to send responses. Complete code is in [here](decrypter.py)

After 100 tasks we get the flag: `IW{Crypt0_c0d3}`

###PL version

Serwer przysyła dane w formacie:

	Hi, I like math and cryptography. Can you talk to me?!
	Level 1.: 4.4.5.3.3.3.3.3.3.3.6.4.3.3.3.3.3.4.3.4.3.4.3.3.3.3.3.3.3.4.6.4.3.3.3.3.3.3.6.4.3.4.4.5
	
Dostajemy też kod procedury szyfrującej:

```python
    def encode(self, eq):
        out = []
        for c in eq:
            q = bin(self._xor(ord(c),(2<<4))).lstrip("0b")
            q = "0" * ((2<<2)-len(q)) + q
            out.append(q)
        b = ''.join(out)
        pr = []
        for x in range(0,len(b),2):
            c = chr(int(b[x:x+2],2)+51)
            pr.append(c)
        s = '.'.join(pr)
        return s
```

Zadanie polega na zdekodowaniu wejścia, rozwiązaniu problemu a następnie wysłaniu zakodowanej odpowiedzi.
Na początku podzieliliśmy funkcje szyfrującą na kawalki (jedna pętla w kawałku) a następnie napisaliśmy kod odwracajacy te funkcje.
Podmieniliśmy stałe jak (2<<4) na ich wartość numeryczną dla poprawnienia czytelności.

Pierwsza część szyfrowania bierze każdy znak z wejścia, xoruje go ze statycznym kluczem 32, zamienia uzyskaną liczbę na binarną i dodaje padding 0 tak żeby liczba zawsze miała 8 cyfr.

W związu z tym deszyfrowanie polega na podzieleniu wejścia na 8-cyfrowe ciągi binarne, potraktowanie każdego jako integer o podstawie 2 (to automatycznie załatwia sprawę paddingu) i xorowaniu tej liczby z 32 (ponieważ `a xor b xor b = a`).

```python
def encode1(eq):
    out = []
    for c in eq:
        q = bin((ord(c) ^ 32)).lstrip("0b")
        q = "0" * (8 - len(q)) + q
        out.append(q)
    b = ''.join(out)
    return b


def decode1(b):
    result = []
    for i in range(0, len(b), 8):
        q = b[i:i + 8]
        q = chr(int(q, 2) ^ 32)
        result.append(q)
    return "".join(result)
```

Druga część szyfrowania bierze binarny ciąg uzyskany w części pierwszej, dzieli go na 2-cyfrowe fragmenty, traktuje każdy jako integer o podstawie 2, dodaje 51 i rzutuje to na char. Następnie wszystkie chary są sklejane z kropką jako separatorem.

W związku z tym deszyfrowanie tej części polega na podzieleniu wejścia po kropkach aby uzyskać chary, następnie rzutowanie tych charów na integery, odjęciu od nich 51, zamiany wyniku na 2-cyfrową liczbę binarną a następnie sklejenie tych liczb w jeden ciąg.

```python
def encode2(b):
    pr = []
    for x in range(0, len(b), 2):
        c = chr(int(b[x:x + 2], 2) + 51)
        pr.append(c)
    s = '.'.join(pr)
    return s


def decode2(task):
    return "".join("{0:02b}".format((ord(c) - 51)) for c in task.split("."))
```

Dzięki temu możemy teraz odkodować wejście, które okazuje się mieć taki sam format jak w zadaniu `A numbers game`, więc wykorzystujemy identyczny kod do rozwiązania problemu a wynik przesyłamy szyfrując go daną metodą `encrypt()`. Cały kod rozwiązania znajduje się [tutaj](decrypter.py).

Po 100 zadaniach dostajemy flagę: `IW{Crypt0_c0d3}`
