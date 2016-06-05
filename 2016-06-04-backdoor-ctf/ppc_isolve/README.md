## ISolve (PPC)

###ENG
[PL](#pl-version)

The task was pretty obvious: the server provides us with a regular expression and we need to supply a string which can be matched by this regex.
Since we're lazy we checked if someone has not done this already, and of course they did: https://bitbucket.org/leapfrogdevelopment/rstr/

So we simply write a short parser for the communication with server, and use `xeger` to get answers.
We had to modify the xeger code a bit because it was generating `\n` in place of whitespace placeholders and the server was not handling this well, so we forced the library to use `\t` always for `\s`.
There was also some issue with non-alphanumeric characters so we also forced those to a single chosen character.
Rest was just the communication with the server:

```python
import rstr
import socket
import re
from time import sleep

def recvuntil(s, pattern, tryouts):
    data = ""
    for i in range(tryouts):
        sleep(1)
        data += s.recv(9999)
        if pattern in data:
            return data
    return data


def main():
    url = "hack.bckdr.in"
    port = 7070
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, port))
    while True:
        task = recvuntil(s, "Pass your solution:", 10)
        print(task)
        to_solve = re.findall("Your regex:\s+(.*)\s+Pass your solution", task)
        if len(to_solve) == 0:
            print(task)
        else:
            print("to solve = '%s'" % to_solve[0])
            solution = rstr.xeger(to_solve[0])
            print("solution  = %s" % solution)
            s.sendall(solution + "\n")


main()
```

Which gave:

```
Passed regex! Way to go.
################################
#######     ROUND 47        #####
################################


Your regex:
ab*


Pass your solution:

to solve = 'ab*'
solution  = ab
Passed regex! Way to go.
Congratulations, you can now say ISOLVE
flag{...}
```

###PL version

Zadanie było dość oczywiste koncepcyjnie: serwer podaje nam wyrażenie regularne a my mamy zwrócić ciąg znaków, który będzie przez to wyrażenie przyjęty.
Jako, że jesteśmy leniwi z natury, sprawdziliśmy czy ktoś już czegoś podobnego nie napisał i oczywiście ktoś taki się znalazł: https://bitbucket.org/leapfrogdevelopment/rstr/

W związku z tym napisalismy krótki parser do komunikacji z serwerem i użylismy `xegera` do uzyskiwania odpowiedzi.
Musieliśmy lekko zmodyfikować kod biblioteki ponieważ generowała znaki `\n` jako białe znaki, a serwer sobie z tym nie radził zbyt dobrze, w związku z tym wymusiliśmy używanie `\t` zawsze dla `\s`.
Były też jakieś problemy ze znakami nie-alfanumerycznymi i te także sprowadziliśmy do jednego wybranego znaku.
Reszta to już tylko komunikacja z serwerem:

```python
import rstr
import socket
import re
from time import sleep

def recvuntil(s, pattern, tryouts):
    data = ""
    for i in range(tryouts):
        sleep(1)
        data += s.recv(9999)
        if pattern in data:
            return data
    return data


def main():
    url = "hack.bckdr.in"
    port = 7070
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, port))
    while True:
        task = recvuntil(s, "Pass your solution:", 10)
        print(task)
        to_solve = re.findall("Your regex:\s+(.*)\s+Pass your solution", task)
        if len(to_solve) == 0:
            print(task)
        else:
            print("to solve = '%s'" % to_solve[0])
            solution = rstr.xeger(to_solve[0])
            print("solution  = %s" % solution)
            s.sendall(solution + "\n")


main()
```

Co dało:

```
Passed regex! Way to go.
################################
#######     ROUND 47        #####
################################


Your regex:
ab*


Pass your solution:

to solve = 'ab*'
solution  = ab
Passed regex! Way to go.
Congratulations, you can now say ISOLVE
flag{...}
```