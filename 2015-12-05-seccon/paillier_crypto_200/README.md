##Find the prime numbers (Crypto, 200p)

###PL
[ENG](#eng-version)

Dostajemy [kod](paillier.txt) skryptu pracującego na serwerze. Skrypt szyfruje pewną wiadomość za pomocą szyfru Pailliera a następnie podaje nam zaszyfrowaną wiadomość oraz kilka innych parametrów. Naszym zadaniem jest złamać szyfr.
Szyfr jest lekko zbliżony do szyfrowania metodą RSA i jego łamanie przebiega w dość podobny sposób. Pierwszym krokiem do złamania szyfru jest uzyskanie informacji o liczbie `n` która jest podstawą dla operacji reszty z dzielenia podczas szyfrowania. Wykorzystujemy tutaj informacje przychodzące z serwera:

```python
	while 1:
		x = pow(random.randint(1000000000, 9999999999), n, (n * n))
		o = (pow(n + 1, 1, n * n) * x) % (n * n)
		y = (((pow(o, l, n * n) - 1) // n) * d) % n
		if y == 1:
			break
	c = (pow(n + 1, int(v["num"]), n * n) * x) % (n * n)
	h = (c * o) % (n * n)
	q = "%019d + %019d = %019d" % (c, o, h)
	print q
```

Jak widać serwer za każdym razem wypisuje nam 3 liczby, z których każda jest resztą z dzielenia przez `n^2`. Dzięki temu możemy szybko ustalić pewne dolne ograniczenie dla liczby `n`, ponieważ liczba `n^2` nie może być większa niż największa z liczb którą dostaniemy z serwera. Dodatkowo wiemy, że

`h = (c * o) % (n * n)`

więc możemy wykorzystać tą zależność do testowania czy aktualnie testowane `n` jest szukaną liczbą.

Operacje pozyskiwania liczby `n` przeprowadzamy skryptem:

```python
lower_bound = 0
bound_lock = threading.Lock()


def seed_collector():
    global bound_lock
    global lower_bound
    while True:
        url = "http://pailler.quals.seccon.jp/cgi-bin/pq.cgi"
        data = str(requests.get(url).content)
        c, o, h = map(int, re.findall("\d+", data))
        potential_n = int(math.sqrt(max([c, o, h])))
        bound_lock.acquire()
        if potential_n > lower_bound:
            lower_bound = potential_n
            print("new lower bound " + str(lower_bound))
        bound_lock.release()
        print(c, o, h)
        sleep(3)


def bruter():
    global lower_bound
    global bound_lock
    bound = 1
    while True:
        bound_lock.acquire()
        current = max([bound, lower_bound])
        lower_bound = current
        if valid_n(lower_bound):
            print("n=" + str(lower_bound))
            return
        else:
            lower_bound += 1
        bound_lock.release()
```

Skrypt opiera się na dwóch wątkach. Pierwszy odpytuje serwer o kolejne trójki liczb i szuka największego dolnego ograniczenia dla liczby `n`. 
Drugi iteruje po kolejnych możliwych liczbach `n` i na podstawie jednego z równań pozyskanych z serwera sprawdza czy jest poprawna.
W ten sposób uzyskujemy `n = 2510510339` które faktoryzujemy do `p = 42727` i `q = 58757`. Dysponując tymi wartościami możemy przejść bezpośrednio do dekodowania wiadomości. Zgodnie z opisem na wikipedii wyliczamy parametry `lambda` oraz `mi` i za ich pomocą dekodujemy wiadomość:

```python
lbd = 1255204428  # lcm(p-1, q-1)
g = n + 1
x = L(pow(g, lbd, n * n), n)
mi = int(modinv(n, x))
c = 2662407698910651121  # example ciphertext from server
m = L(pow(c, lbd, n * n), n) * pow(mi, 1, n)
print(m % n)
```

Co daje nam: `1510490612` a umieszczenie tej liczby na serwerze daje flagę: `SECCON{SECCoooo_oooOooo_ooooooooN}`

Kompletny użyty skrypt znajduje sie [tutaj](crypto_paillier.py)

### ENG version

We get the [source code](paillier.txt) of a script that is used on the server. The cipher encodes a certain message using Paillier cipher and the returns to us the encoded message and some parameters. Our task is to break the code.
The cipher is a bit like RSA and the approach to break it is very similar. First step is to get the `n` number which is the basis for all modulo operations in the cipher. For this we use data we get from server:

```python
	while 1:
		x = pow(random.randint(1000000000, 9999999999), n, (n * n))
		o = (pow(n + 1, 1, n * n) * x) % (n * n)
		y = (((pow(o, l, n * n) - 1) // n) * d) % n
		if y == 1:
			break
	c = (pow(n + 1, int(v["num"]), n * n) * x) % (n * n)
	h = (c * o) % (n * n)
	q = "%019d + %019d = %019d" % (c, o, h)
	print q
```

As can be seen, the server prints 3 numbers, each one is a reminder after division by `n^2`. This means we can quickly make a lower bound for `n` since `n^2` can't be bigger than the biggest number we get from server. On top of that we know that:

`h = (c * o) % (n * n)`

so we can use this equation to quickly test if the `n` we are testing is the number we are looking for.

Recovery of `n` is done with script:

```python
lower_bound = 0
bound_lock = threading.Lock()


def seed_collector():
    global bound_lock
    global lower_bound
    while True:
        url = "http://pailler.quals.seccon.jp/cgi-bin/pq.cgi"
        data = str(requests.get(url).content)
        c, o, h = map(int, re.findall("\d+", data))
        potential_n = int(math.sqrt(max([c, o, h])))
        bound_lock.acquire()
        if potential_n > lower_bound:
            lower_bound = potential_n
            print("new lower bound " + str(lower_bound))
        bound_lock.release()
        print(c, o, h)
        sleep(3)


def bruter():
    global lower_bound
    global bound_lock
    bound = 1
    while True:
        bound_lock.acquire()
        current = max([bound, lower_bound])
        lower_bound = current
        if valid_n(lower_bound):
            print("n=" + str(lower_bound))
            return
        else:
            lower_bound += 1
        bound_lock.release()
```

The script uses two threads. First one queries the server for triplets and looks for bigger lower bound for `n`.
The second iterates over possible `n` and using one of the equations from the server it is checking if the currently tested value is the real `n`.
This way almost instantly we get `n = 2510510339` which we factor into `p = 42727` and `q = 58757`.
With those two values we can recover the private key and start decoding the cipher. We follow the decription on wikipedia to calculate the `lambda` and `mi` parameters and we use them to decode the message:

```python
lbd = 1255204428  # lcm(p-1, q-1)
g = n + 1
x = L(pow(g, lbd, n * n), n)
mi = int(modinv(n, x))
c = 2662407698910651121  # example ciphertext from server
m = L(pow(c, lbd, n * n), n) * pow(mi, 1, n)
print(m % n)
```

Which gives us: `1510490612` and placing this number on the server gives the flag: `SECCON{SECCoooo_oooOooo_ooooooooN}`

Whole script is available [here](crypto_paillier.py)
