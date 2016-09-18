## Regexpire (Misc/PPC, 100p)

###ENG
[PL](#pl-version)

Task almost identical to https://github.com/p4-team/ctf/tree/master/2016-06-04-backdoor-ctf/ppc_isolve so we solved it pretty much the same way - with simplified xeger:

```python
import socket
from rstr import xeger


def recvuntil(s, tails):
    data = ""
    while True:
        for tail in tails:
            if tail in data:
                return data
        data += s.recv(1)


def main():
    url = "misc.chal.csaw.io"
    port = 8001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, port))
    task1 = recvuntil(s, "\n")
    print(task1)
    while True:
        task2 = recvuntil(s, "\n")
        print(task2)
        to_solve = task2[:-1]
        if len(to_solve) != 0:
            print("to solve = '%s'" % to_solve)
            solution = xeger(to_solve)
            print("solution  = %s" % solution)
            s.sendall(solution + "\n")
main()
```

With modifications to:

```python

ALPHABETS = {'printable': ['a'],
             'letters': ['a'],
             'uppercase': ['A'],
             'lowercase': ['a'],
             'digits': ['1'],
             'punctuation': [','],
             'nondigits': ['a'],
             'nonletters': ['1'],
             'whitespace': [' '],
             'nonwhitespace': ['a'],
             'normal': ['a'],
             'word': ['a'],
             'nonword': ['#'],
             'postalsafe': string.ascii_letters + string.digits + ' .-#/',
             'urlsafe': string.ascii_letters + string.digits + '-._~',
             'domainsafe': string.ascii_letters + string.digits + '-'
             }
```

because the server did not handle everything.

`flag{^regularly_express_yourself$}`

###PL version

Zadanie prawie identyczne jak https://github.com/p4-team/ctf/tree/master/2016-06-04-backdoor-ctf/ppc_isolve więc rozwiązaliśmy je tak samo, zmodyfikowanym xegerem:

```python
import socket
from rstr import xeger


def recvuntil(s, tails):
    data = ""
    while True:
        for tail in tails:
            if tail in data:
                return data
        data += s.recv(1)


def main():
    url = "misc.chal.csaw.io"
    port = 8001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, port))
    task1 = recvuntil(s, "\n")
    print(task1)
    while True:
        task2 = recvuntil(s, "\n")
        print(task2)
        to_solve = task2[:-1]
        if len(to_solve) != 0:
            print("to solve = '%s'" % to_solve)
            solution = xeger(to_solve)
            print("solution  = %s" % solution)
            s.sendall(solution + "\n")
main()
```

Z modyfikacją dla:

```python
ALPHABETS = {'printable': ['a'],
             'letters': ['a'],
             'uppercase': ['A'],
             'lowercase': ['a'],
             'digits': ['1'],
             'punctuation': [','],
             'nondigits': ['a'],
             'nonletters': ['1'],
             'whitespace': [' '],
             'nonwhitespace': ['a'],
             'normal': ['a'],
             'word': ['a'],
             'nonword': ['#'],
             'postalsafe': string.ascii_letters + string.digits + ' .-#/',
             'urlsafe': string.ascii_letters + string.digits + '-._~',
             'domainsafe': string.ascii_letters + string.digits + '-'
             }
```

Bo serwer nie wszystko dobrze parsował.

`flag{^regularly_express_yourself$}`