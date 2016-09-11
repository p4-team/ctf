## Secu Prim (PPC, 65p)

###ENG
[PL](#pl-version)

After connecting to the server we get a PoW to solve, and then the task is to provide number of primes and perfect powers in given range.

The ranges are rather small (less than 2000 numbers in between) so we simply iterate over the given range and use `gmpy` to tell us if the number if a probable prime or a perfect power:

```python
def solve_task(start, end):
    print("Range size = " + str(end - start))
    counter = 0
    for i in range(start, end + 1):
        if gmpy2.is_prime(i):
            counter += 1
        elif gmpy2.is_power(i):
            counter += 1
    print("Counted " + str(counter))
    return counter
```

And the whole script with PoW:

```python
import hashlib
import re
import socket

import itertools
import string
import gmpy2


def recvuntil(s, tails):
    data = ""
    while True:
        for tail in tails:
            if tail in data:
                return data
        data += s.recv(1)


def proof_of_work(s):
    data = recvuntil(s, ["Enter X:"])
    x_suffix, hash_prefix = re.findall("X \+ \"(.*)\"\)\.hexdigest\(\) = \"(.*)\.\.\.\"", data)[0]
    len = int(re.findall("\|X\| = (.*)", data)[0])
    print(data)
    print(x_suffix, hash_prefix, len)
    for x in itertools.product(string.ascii_letters + string.digits, repeat=len):
        c = "".join(list(x))
        h = hashlib.sha256(c + x_suffix).hexdigest()
        if h.startswith(hash_prefix):
            return c


def get_task(s):
    sentence = recvuntil(s, ["that: "])
    sentence += recvuntil(s, ["\n"])
    return sentence


def solve_task(start, end):
    print("Range size = " + str(end - start))
    counter = 0
    for i in range(start, end + 1):
        if gmpy2.is_prime(i):
            counter += 1
        elif gmpy2.is_power(i):
            counter += 1
    print("Counted " + str(counter))
    return counter


def main():
    url = "secuprim.asis-ctf.ir"
    port = 42738
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, port))
    x = proof_of_work(s)
    print(x)
    s.sendall(x + "\n")
    data = recvuntil(s, "---\n")
    print(data)
    while True:
        data = recvuntil(s, ["like n such", "corret!", "}"])
        print(data)
        if "ASIS" in data:
            print(data)
        if "corret" in data:
            print("failed")
            break
        else:
            task = get_task(s)
            print(task)
            b, e = re.findall("that: (\d+) <= n <= (\d+)", task)[0]
            start = int(b)
            end = int(e)
            counter = solve_task(start, end)
            s.sendall(str(counter) + "\n")


main()
```

###PL version

Po połączeniu do serwera dostajemy PoW do rozwiązania a następnie zadaniem jest policzyć ile liczb pierwszych oraz doskonałych potęg jest w zadanym przedziale.

Przedziały są dość małe (nie więcej niż 2000 liczb) więc po prostu iterujemy po każdej liczbie i za pomocą `gmpy` sprawdzamy czy liczba jest pierwsza lub czy jest doskonałą potęgą:

```python
def solve_task(start, end):
    print("Range size = " + str(end - start))
    counter = 0
    for i in range(start, end + 1):
        if gmpy2.is_prime(i):
            counter += 1
        elif gmpy2.is_power(i):
            counter += 1
    print("Counted " + str(counter))
    return counter
```

A cały skrypt razem z PoW:

```python
import hashlib
import re
import socket

import itertools
import string
import gmpy2


def recvuntil(s, tails):
    data = ""
    while True:
        for tail in tails:
            if tail in data:
                return data
        data += s.recv(1)


def proof_of_work(s):
    data = recvuntil(s, ["Enter X:"])
    x_suffix, hash_prefix = re.findall("X \+ \"(.*)\"\)\.hexdigest\(\) = \"(.*)\.\.\.\"", data)[0]
    len = int(re.findall("\|X\| = (.*)", data)[0])
    print(data)
    print(x_suffix, hash_prefix, len)
    for x in itertools.product(string.ascii_letters + string.digits, repeat=len):
        c = "".join(list(x))
        h = hashlib.sha256(c + x_suffix).hexdigest()
        if h.startswith(hash_prefix):
            return c


def get_task(s):
    sentence = recvuntil(s, ["that: "])
    sentence += recvuntil(s, ["\n"])
    return sentence


def solve_task(start, end):
    print("Range size = " + str(end - start))
    counter = 0
    for i in range(start, end + 1):
        if gmpy2.is_prime(i):
            counter += 1
        elif gmpy2.is_power(i):
            counter += 1
    print("Counted " + str(counter))
    return counter


def main():
    url = "secuprim.asis-ctf.ir"
    port = 42738
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, port))
    x = proof_of_work(s)
    print(x)
    s.sendall(x + "\n")
    data = recvuntil(s, "---\n")
    print(data)
    while True:
        data = recvuntil(s, ["like n such", "corret!", "}"])
        print(data)
        if "ASIS" in data:
            print(data)
        if "corret" in data:
            print("failed")
            break
        else:
            task = get_task(s)
            print(task)
            b, e = re.findall("that: (\d+) <= n <= (\d+)", task)[0]
            start = int(b)
            end = int(e)
            counter = solve_task(start, end)
            s.sendall(str(counter) + "\n")


main()
```
