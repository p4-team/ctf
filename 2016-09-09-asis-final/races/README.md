## Races (Crypto, 189p)

###ENG
[PL](#pl-version)

In the task we get a [source code](RACES.py) of ECC encryption, and also a [file](pubkey_enc.txt) with multiple public keys and flag encrypted using different keys.
The encryption itself is textbook so no vulnerabilities there but if we look at the key generation code we have:

```python
def gen_prime(nbit):
	while True:
		prime = getPrime(nbit)
		if prime % 3 == 2:
			return prime
```

This means that we exclude 2/3 of the primes!
Since we have a lot of public keys we decided to checks if by any chance it didn't happen that two public keys share a common factor.
In such case calculating GCD of those two keys will give us the common prime:

```python
import codecs
import re
import itertools
import gmpy2


def find_repeated_prime():
    with codecs.open("./pubkey_enc.txt") as input_file:
        ns = [re.findall("e\) = \((\d+)", line)[0] for line in input_file]
        for pair in itertools.combinations(ns, 2):
            if gmpy2.gcd(long(pair[0]), long(pair[1])) != 1:
                print(pair)
                return pair


n1, n2 = find_repeated_prime()
p = long(gmpy2.gcd(long(n1), long(n2)))
q1 = long(n1) / p
q2 = long(n2) / p
print(p, q1, q2)
```

And we were lucky, because we got two public keys sharing the same prime, which means we successfully factored those two keys.
Now the only thing left to do was to recover the private key:

```python

n = 145027482789690990262517750951541446221552255560520228703877313431483316741269117323705124775232890171059397344533125793378274261538984168613648947111600523237940505464340771538677343847823054950559536582762094561232606689017946799356626447164268129816358964385649508992872978250974645830516100018108294421843L
p = 13101261334925358356052012802088920395535884660597547763946806535628065670277915852917356305443939004844164299871676780335359374939404036920480708592902391L
q = n / p
assert (p * q == n)
e = 65537
c = (84876076421614376067149365902722288787017939432560112310344060253776893355155004799570079133487890091744927361496759572955051910756381500540609425582325044679541917701176783432330786945586473421496533459046926087433374002572145804591821522550941784213497101941864710192882108942428579695906987627994038160506L, 53075793789885196175396474745354653894462035118379186161754018180061911263633656154635135006901226712322309187026865430527729260554951872682683031998933681813562644904853338601687712543027240467179318352856177931746928027694032725413016073749325323908751643659718884095101708806519753380797321211563244283733L)
lcm = gmpy2.lcm((p+1), (q+1))
d = gmpy2.invert(e, lcm)
print(d)
```

And use it to decrypt the flag:


```python
p0, p1 = multiply(c, d, n)
print long_to_bytes(p1 - p0)
```

###PL version

W zadaniu dostajemy [kod](RACES.py) szyfrowania metodą krzywych eliptycznuch oraz [plik](pubkey_enc.txt) z zestawem kluczy publicznych oraz flag szyfrowanych różnymi kluczami.
Kod szyfrowania jest książkowy więc nie spodziewaliśmy się tam podatności, ale algorytm generacji klucza jest ciekawy:

```python
def gen_prime(nbit):
	while True:
		prime = getPrime(nbit)
		if prime % 3 == 2:
			return prime
```

To oznacza ze odrzucamy 2/3 liczb pierwszych z zakresu!
Ponieważ mamy pod ręką dużo kluczy publicznych postawiliśmy sprawdzić czy może akurat przypadkiem dwa z nich nie współdzielą czynnika.
W takiej sytuacji licząc największy wspólny dzielnik tych dwóch kluczy uzyskamy wspólny czynnik pierwszy:

```python
import codecs
import re
import itertools
import gmpy2


def find_repeated_prime():
    with codecs.open("./pubkey_enc.txt") as input_file:
        ns = [re.findall("e\) = \((\d+)", line)[0] for line in input_file]
        for pair in itertools.combinations(ns, 2):
            if gmpy2.gcd(long(pair[0]), long(pair[1])) != 1:
                print(pair)
                return pair


n1, n2 = find_repeated_prime()
p = long(gmpy2.gcd(long(n1), long(n2)))
q1 = long(n1) / p
q2 = long(n2) / p
print(p, q1, q2)
```

Mieliśmy szczęście, bo faktycznie dwa klucze publiczne współdzieliły czynnik pierwszy, co oznacza, że z powodzeniem dokonaliśmy faktoryzacji tych kluczy.
Teraz pozostało jedynie odzyskać klucz prywatny:

```python

n = 145027482789690990262517750951541446221552255560520228703877313431483316741269117323705124775232890171059397344533125793378274261538984168613648947111600523237940505464340771538677343847823054950559536582762094561232606689017946799356626447164268129816358964385649508992872978250974645830516100018108294421843L
p = 13101261334925358356052012802088920395535884660597547763946806535628065670277915852917356305443939004844164299871676780335359374939404036920480708592902391L
q = n / p
assert (p * q == n)
e = 65537
c = (84876076421614376067149365902722288787017939432560112310344060253776893355155004799570079133487890091744927361496759572955051910756381500540609425582325044679541917701176783432330786945586473421496533459046926087433374002572145804591821522550941784213497101941864710192882108942428579695906987627994038160506L, 53075793789885196175396474745354653894462035118379186161754018180061911263633656154635135006901226712322309187026865430527729260554951872682683031998933681813562644904853338601687712543027240467179318352856177931746928027694032725413016073749325323908751643659718884095101708806519753380797321211563244283733L)
lcm = gmpy2.lcm((p+1), (q+1))
d = gmpy2.invert(e, lcm)
print(d)
```

I użyć go do deszyfrowania flagi:


```python
p0, p1 = multiply(c, d, n)
print long_to_bytes(p1 - p0)
```
