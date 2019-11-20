# Primordial (Crypto, 171p, 25 solved)

In the challenge we get [code](primordial_rsa.py) and [output](output.txt).

If we look at the primes generation, some things seems odd:

```python
def gen_prime(nbit):
    while True:
        s = getPrime(36)
        a = primorial(getPrime(random.randint(7, 9)))
        b = primorial(getPrime(random.randint(2, 5)))
        for r in range(10**3, 3*10**3, 2):
            p = s * a // b - r
            if gmpy2.is_prime(p) and len(bin(p)[2:]) == nbit:
                return int(p)
```

Specifically the very small randoms which are used here.
While primorial makes those numbers very big, the entropy is extremely low.

In fact we can easily enumerate all primes which can come from `getPrime(random.randint(7, 9))` and getPrime(random.randint(2, 5)) and it's not that many.
The last loop is also trivial to brute-force, it's just 1000 values to check.

The only real problem is `s = getPrime(36)` since those are 36 bits we don't know.
I suspect it's within brute-force range still, but we used a more reasonable approach.

Let's assume we know `a`, `b` and `r` since we can easily enumerate all possible combinations of those values.
We can then check which of them meet the condition `len(bin(p)[2:]) == nbit`, since we know how many bits `s` has.

This in turn gave us literally 2 options:

```python
current_a = 2 ** 6 - 1
a = []
while len(bin(current_a)[2:]) <= 9:
    current_a = next_prime(current_a)
    a.append(current_a)
print(a)
current_b = 2 ** 1 - 2
b = []
while len(bin(current_b)[2:]) <= 5:
    current_b = next_prime(current_b)
    b.append(current_b)
print(b)
ps = [primorial(p, False) for p in a]
qs = [primorial(q, False) for q in b]
divs = []
for (p, q) in itertools.product(ps, qs):
    divs.append(p / q)
potential_divs = []
for d in divs:
    if 475 < len(bin(d)[2:]) < 478:
        potential_divs.append(d)
print(map(int, potential_divs))
```

From that we get that `a/b` can be only:

```
[157833473171036402557340887861918279894066895152614171872650217971188957505160728753634580242894723692077708152487421472942198886320563361989519L, 265796235513071835939791625686948223290731767183919871953306061941104069201525744225121420707540377151699132081108668768663225519768309440666057L]
```

Still, we need to recover `s` somehow.

Let's create a polynomial `f(x) = x * a/b - r`.
It's obvious that for `x0 = s` this polynomial is `s * a/b - r = p` and therefore it will reduce to `0` mod `p`.

We know that `s` has only 36 bits, while `N` has 1024 bits , `p` and `q` are about 512 bits each and polynomial has degree 1.
This means that we can use Coppersmith theorem here, since `beta=512/1024=0.5` and therefore we could find roots of this polynomial up until `N^(0.5^2/1) = N^0.25` so 256 bits:

```python
def decrypt_flag(N, ct, potential_divs):
    F.<x> = PolynomialRing(Zmod(N), implementation='NTL')
    for d in potential_divs:
        print('testing',d)
        for r in range(10**3, 3*10**3, 2):
            poly = x * d - r
            poly = poly.monic()
            roots = poly.small_roots(beta=0.5,X=2**50)
            if len(roots)>0:
                print(roots)
                p = int(roots[0]*d-r)
                q = int(int(N)/int(p))
                phi = (p-1)*(q-1)
                print(phi)
                d = inverse_mod(65537,phi)
                decrypted = pow(ct,int(d),N)
                print(decrypted)
                return long_to_bytes(int(decrypted))
```

Running this gives us back `ASIS{f4C7OR1ZIn9_PrimoR!4L_pR1m3z_Iz_3A5Y_I5nt_iT?}`

Complete solver [here](solver.sage)
