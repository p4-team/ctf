# hiecss (Crypto 150)

###ENG
[PL](#pl-version)

In the task we get [source code](hiecss.py) of some elliptic curve - based encryption scheme.
The most important part is:

```python
e = 65537
order = 'Give me the flag. This is an order!'

def decode(bs):
    if len(bs) < 0x40:
        return None
    s, m = int(bs[:0x40], 16), bs[0x40:]
    if s >= q:
        print('\x1b[31mbad signature\x1b[0m')
        return None
    S = s, sqrt(pow(s, 3, q) + a * s + b, q)
    if S[1] is None:
        print('\x1b[31mbad signature:\x1b[0m {:#x}'.format(S[0]))
        return None
    h = int(SHA256.new(m.encode()).hexdigest(), 16)
    if mul(q, a, b, e, S)[0] == h:
        return m
    else:
        print('\x1b[31mbad signature:\x1b[0m ({:#x}, {:#x})'.format(*S))

if __name__ == '__main__':

    q, a, b = map(int, open('curve.txt').read().strip().split())

    for _ in range(1337):
        m = decode(input())
        if m is not None and m.strip() == order:
            print(open('flag.txt').read().strip())
            break
```

We can see that curve params come from the file and we don't know them.
We can also query the server many times in a single session.
The point is to provide input for which the `decode` function will return a string which stripped of spaces matches given string.

The `decode` function splits our input using first 64 bytes as hex-encoded integer `s` and the rest as string `m` from wich sha256 hash value is calculated.
In the end the second part of our input is returned if all conditions are met, therefore this value has to match the given messsage (but may contain some additional whitespaces at the end).

First condition is that our integer `s` has to be smaller than `q` the program takes from curve definition file.
In case we fail we get a nice error message.
If we succeed we move to next condition, which has a different error message upon failure!

We can exploit this in order to get `q` value precisely - we can use binary search based on the length or error message:

```python
def form_payload_from_number(q):
    payload = hex(q)[2:]
    if "L" in payload:
        payload = payload[:-1]
    payload = ('0' * (64 - len(payload))) + payload
    return payload


def get_q(s, msg):
    max_q = 2 ** 256 - 1
    min_q = 0
    q = 0
    while True:
        q = (max_q - min_q) / 2 + min_q
        print(hex(q), max_q, min_q)
        payload = form_payload_from_number(q)
        s.sendall(payload + msg + "\n")
        result = s.recv(9999)
        if len(result) == 23:  # our q too big
            max_q = q
        else:  # our q was too small
            min_q = q
        print(result)
        if max_q == q or min_q == q:
            print("Found q", q)
            break
    return q
```

With this we recover `q = 0x247ce416cf31bae96a1c548ef57b012a645b8bff68d3979e26aa54fc49a2c297L`

We proceed to the next condition.
Here we basically need to make sure our value `s` is actually `x` coordinate of a point `S` on the elliptic curve.
It would be easier if we knew the said curve.
There are however some trivial values which can get us past this check.

The last check verifies if point on the curve with `x` coordinate equal to sha256 hash of the message we privided (let's call the point `H`) is equal to `S*e` on the curve.
Again if we fail we get a nice error message, and this time it actually contains the `S` point for which we provided only the `x` coordiante.

This way we provide `s` and we get `sqrt(pow(s, 3, q) + a * s + b, q)`.
We exploit this to recover `a` and `b`:

By sending `s = 0` we get as a result `sqrt(pow(0,3,q) + a*0 + b, q) = sqrt(b, q)`
We only need to square the value mod q to recover `b mod q`:

```python
b = pow(0x18aae6ca595e2b030870f49d1aa143f4b46864eceab492f6f5a0f0efc9c90e51, 2, q)
```

By sending `s = 2` we get as a result `sqrt(pow(2,3,q) + a*2 + b, q) = sqrt(2*a + 8 + b, q)`
Again we just need a square and simple subtraction to recover `a mod q`:

```python
a = (((pow(0x20d599b9106e16f43d0c0a54e78517f5834bf15ef0206a5ce37080e4cad4f359, 2, q) - b - 8) % q) / 2) 
```

Now we have all curve parameters and we need to get such point `S` that `H` = `S*e`.
For this we need a multiplicative inverse of `e` on the curve, because then `H*inverse_e = S*e*inverse_e = S`.
We know `H`, or at least we can brute-force the message value so that hash from it will point to `x` coordinate on the curve, so we can get `H`.

To calculate the inverse we need to know the number of points on the curve (the order/cardinality).
For this we used Sage:

```
E = EllipticCurve(GF(q),[a,b])
E.cardinality()
```

Which gave us `order = 16503925798136106726026894143294039201930439456987742756395524593191976084900` as curve order.

Now we just had to calculate `inverse_e = modinv(e, order)` and multiply some `H` on the curve by this value to get our point `S`:

```python
def compute_point(a, b, q, field_order, msg):
    e = 65537
    hx = int(hashlib.sha256(msg.encode()).hexdigest(), 16)
    hy = sqrt(pow(hx, 3, q) + a * hx + b, q)
    e_inv = gmpy2.invert(e, field_order)
    S = mul(q, a, b, e_inv, (hx, hy))
    check = mul(q, a, b, e, S)
    assert check[0] == hx
    return S[0]
```

We test this on messages with appended more and more whitespaces and we get a hit after we add 4 spaces to the message -> `msg = 'Give me the flag. This is an order!    '`

Now we only need to send the `x` coordinate from the `S` point along with the message padded with 4 spaces and we get the flag in return:

```python
def main():
    msg = 'Give me the flag. This is an order!    '
    url = "130.211.200.153"
    port = 25519
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, port))
    sleep(1)
    # q = get_q(s, msg)
    q = 0x247ce416cf31bae96a1c548ef57b012a645b8bff68d3979e26aa54fc49a2c297L
    field_order = 16503925798136106726026894143294039201930439456987742756395524593191976084900
    b = pow(0x18aae6ca595e2b030870f49d1aa143f4b46864eceab492f6f5a0f0efc9c90e51, 2, q)
    a = (((pow(0x20d599b9106e16f43d0c0a54e78517f5834bf15ef0206a5ce37080e4cad4f359, 2,
               q) - b - 8) % q) / 2)
    p = compute_point(a, b, q, field_order, msg)
    payload = form_payload_from_number(p)
    payload += msg
    print(payload)
    s.sendall(payload + "\n")
    print(s.recv(9999))
```

And we get `hxp{H1dd3n_Gr0uP_0rD3rz_4r3_5uPP0s3D_t0_B3_k3p7_h1DD3n!}`

###PL version

W zadaniu dostajemy [kod źródłowy](hiecss.py) szyfrowania opartego o krzywe eliptyczne.
Najważniejsza część to:

```python
e = 65537
order = 'Give me the flag. This is an order!'

def decode(bs):
    if len(bs) < 0x40:
        return None
    s, m = int(bs[:0x40], 16), bs[0x40:]
    if s >= q:
        print('\x1b[31mbad signature\x1b[0m')
        return None
    S = s, sqrt(pow(s, 3, q) + a * s + b, q)
    if S[1] is None:
        print('\x1b[31mbad signature:\x1b[0m {:#x}'.format(S[0]))
        return None
    h = int(SHA256.new(m.encode()).hexdigest(), 16)
    if mul(q, a, b, e, S)[0] == h:
        return m
    else:
        print('\x1b[31mbad signature:\x1b[0m ({:#x}, {:#x})'.format(*S))

if __name__ == '__main__':

    q, a, b = map(int, open('curve.txt').read().strip().split())

    for _ in range(1337):
        m = decode(input())
        if m is not None and m.strip() == order:
            print(open('flag.txt').read().strip())
            break
```

Widać, że parametry krzywej czytane są z pliku i nie są nam znane.
Możemy także odpytywać serwer wielokrotnie w jednej sesji.
Naszym zadaniem jest podanie takich danych na wejście, aby wynik działania funkcji `decode` na nich, po usunięciu spacji pasował do podanego stringa.

Funkcja `decode` dzieli dane biorąc pierwsze 64 bajty jako hex-encoded integer `s` a pozostałą część jako string `m` z którego następnie liczony jest hash sha256.
Na koniec, jeśli spełnimy kilka warunków, jako wynik funkcji odsyłana jest wartość `m` więc ta wartość musi pasować do podanej w programie wiadomości (ale może zawierać na końcu dodatkowe białe znaki).

Pierwszy warunek wymusza żeby integer `s` był mniejszy niż `q` które program bierze z pliku.
Jeśli warunek nie jest spełniony dostajemy ładny komunikat błędu.
Jeśli nam się powiedzie ale nie uda się kolejny warunek dostajemy inny komunikat błędu!

Możemy wykorzystać to jako wyrocznie aby odzyskać wartość `q` - możemy użyć szukania binarnego bazując na długości wiadomości błędu:

```python
def form_payload_from_number(q):
    payload = hex(q)[2:]
    if "L" in payload:
        payload = payload[:-1]
    payload = ('0' * (64 - len(payload))) + payload
    return payload


def get_q(s, msg):
    max_q = 2 ** 256 - 1
    min_q = 0
    q = 0
    while True:
        q = (max_q - min_q) / 2 + min_q
        print(hex(q), max_q, min_q)
        payload = form_payload_from_number(q)
        s.sendall(payload + msg + "\n")
        result = s.recv(9999)
        if len(result) == 23:  # our q too big
            max_q = q
        else:  # our q was too small
            min_q = q
        print(result)
        if max_q == q or min_q == q:
            print("Found q", q)
            break
    return q
```

W ten sposób odzyskujemy `q = 0x247ce416cf31bae96a1c548ef57b012a645b8bff68d3979e26aa54fc49a2c297L`

Przechodzimy do następnego warunku.
Tutaj musimy generalnie upewnić się, że wartość `s` jest współrzędną `x` punktu `S` na krzywej eliptycznej.
Byłoby prościej gdybyśmy wiedzieli co to za krzywa.
Są jednak pewne trywialne punkty dla których możemy przejść ten warunek.

Ostatni warunek sprawdza czy punkt na krzywej ze współrzędną `x` równą sha256 z naszej wiadomości (nazwijmy ten punkt `H`) jest równy `S*e` na krzywej.
Znów jeśli nam się nie uda dostajemy błąd, tym razem zawierający współrzędne punktu `S` dla którego podaliśmy `x`.

To oznacza że podajemy `s` a dostajemy `sqrt(pow(s, 3, q) + a * s + b, q)`.
Wykorzystujemy to aby odzyskać `a` oraz `b`:

Wysyłając `s = 0` dostajemy jako wynik `sqrt(pow(0,3,q) + a*0 + b, q) = sqrt(b, q)`
Musimy to teraz tylko podnieść do kwadratu modulo q aby uzyskać `b mod q`:

```python
b = pow(0x18aae6ca595e2b030870f49d1aa143f4b46864eceab492f6f5a0f0efc9c90e51, 2, q)
```

Wysyłając `s = 2` dostajemy jako wynik `sqrt(pow(2,3,q) + a*2 + b, q) = sqrt(2*a + 8 + b, q)`
Znów musimy tylko podnieść do kwadratu i wynikać odejmowanie stałych aby dostać `a mod q`:

```python
a = (((pow(0x20d599b9106e16f43d0c0a54e78517f5834bf15ef0206a5ce37080e4cad4f359, 2, q) - b - 8) % q) / 2) 
```

Teraz mamy już wszystkie parametry krzywej i potrzebujemy znaleźć punkt `S` taki że `H` = `S*e`.
Do tego potrzebujemy liczbę odwrotną dla `e` na krzywej, ponieważ `H*inverse_e = S*e*inverse_e = S`.
Znamy `H`, a przynajmniej możemy je uzyskać metodą brute-force szukając stringa z podanym prefixem i spacjami na końcu, który hashuje się do `x` leżącego na krzywej, więc możemy poznać odpowiednie `H`.

Aby policzyć liczbę odwrotną potrzebujemy znać liczbe punktów na krzywej.
Do tego użyliśmy sage:

```
E = EllipticCurve(GF(q),[a,b])
E.cardinality()
```

Co dało nam: `order = 16503925798136106726026894143294039201930439456987742756395524593191976084900` jako liczność punktów na krzywej.

Teraz potrzebujemy jedynie policzyć `inverse_e = modinv(e, order)` i pomnożyć przez jakieś `H` na krzywej aby dostać szukaną wartość punktu `S`:

```python
def compute_point(a, b, q, field_order, msg):
    e = 65537
    hx = int(hashlib.sha256(msg.encode()).hexdigest(), 16)
    hy = sqrt(pow(hx, 3, q) + a * hx + b, q)
    e_inv = gmpy2.invert(e, field_order)
    S = mul(q, a, b, e_inv, (hx, hy))
    check = mul(q, a, b, e, S)
    assert check[0] == hx
    return S[0]
```

Testujemy tak koljne wiadomości dodając spacje aż przy dodanych 4 spacjach trafiamy na punkt na krzywej -> `msg = 'Give me the flag. This is an order!    '`

Teraz pozostaje jedynie wysłać na serwer współrzędna `x` punktu `S` razem z wiadomością powiększoną o 4 spacje aby dostać flagę:

```python
def main():
    msg = 'Give me the flag. This is an order!    '
    url = "130.211.200.153"
    port = 25519
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, port))
    sleep(1)
    # q = get_q(s, msg)
    q = 0x247ce416cf31bae96a1c548ef57b012a645b8bff68d3979e26aa54fc49a2c297L
    field_order = 16503925798136106726026894143294039201930439456987742756395524593191976084900
    b = pow(0x18aae6ca595e2b030870f49d1aa143f4b46864eceab492f6f5a0f0efc9c90e51, 2, q)
    a = (((pow(0x20d599b9106e16f43d0c0a54e78517f5834bf15ef0206a5ce37080e4cad4f359, 2,
               q) - b - 8) % q) / 2)
    p = compute_point(a, b, q, field_order, msg)
    payload = form_payload_from_number(p)
    payload += msg
    print(payload)
    s.sendall(payload + "\n")
    print(s.recv(9999))
```

I dostajemy `hxp{H1dd3n_Gr0uP_0rD3rz_4r3_5uPP0s3D_t0_B3_k3p7_h1DD3n!}`
