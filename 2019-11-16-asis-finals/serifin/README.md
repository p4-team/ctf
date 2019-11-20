# Serifin (Crypto, 140p, 33 solved)

In the challenge we get [code](serifin.py) and [output](output.txt).

The important part here is the primes generation:

```python
def genPrime(nbit):
    while True:
        p = getPrime(512)
        if p % 9 == 1 and p % 27 >= 2:
            q = gmpy2.next_prime(serifin(p, 3) + serifin(p, 9) + serifin(p, 27))
            if q % 9 == 1 and q % 27 >= 2:
                return int(p), int(q)
```

I don't really know what exactly `serifin` does, but quick blackbox analysis shows that it produces value like `0x2735822f94f13d0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000089`.

This means that in reality only a few high bytes are unknown, rest are 0 and there is some small value at the lowest bits.
From quick tests we can figure that lower 350 bits should be 0.

We create a polynomial `f(x) = x *(2**350) + i`.
The part `*(2**350)` is simply to shift the `x` value to high bits.
`i` should be a small number, which comes from calling `next_prime`, and we can iterate over this.

This polynomial will reduce to `0` mod `q` if we find the `x` such that `x *(2**350) + i = q`.
Polynomial has degree 1 and both `p` and `q` are of similar bitlength (`q` is a bit bigger), of about `N^0.5`.
From Coppersmith theorem we know we can find roots of such polynomial assuming the root is smaller than `beta^2/d`, so for us `0.5^2/1 = 0.25`.
We're looking for far less bits, so it should work just fine:

```python
def find_factors(N):
    F.<x> = PolynomialRing(Zmod(N), implementation='NTL')   
    i = 0
    while True:
        poly = x*(2**350)+i
        poly = poly.monic()
        roots = poly.small_roots(beta=0.5)
        if roots:
            for root in roots:
                if root != 0:
                    q = int(root)*(2**350)+i
                    p = int(N)/int(q)
                    return p,q
        i=i+1
```

Now that we have `p` and `q`, we can try to decrypt the flag.
But it turns out there is a twist -> `gcd(phi, e) == 3` so we can't just do RSA decryption.

We actually need to calculate the cubic root over composite value `N` instead.
But we have the factorization, so it's not such a big problem.

We need to:

1. Calculate the roots over each of the prime factors of N
2. Combine the solutions using CRT

```python
def cubic_root_prime(c,p):
    F.<x> = PolynomialRing(Zmod(p), implementation='NTL')
    poly = x^3 - c
    return poly.roots()
        
def cubic_composite_root(c, p, q):
    return cubic_root_prime(c,p), cubic_root_prime(c, q)
```

The last part is simply to take every possible combination of the roots and check if it's the right flag:

```python
    c = 78643169701772559588799235367819734778096402374604527417084323620408059019575192358078539818358733737255857476385895538384775148891045101302925145675409962992412316886938945993724412615232830803246511441681246452297825709122570818987869680882524715843237380910432586361889181947636507663665579725822511143923
    rootsp, rootsq = cubic_composite_root(c,p,q)
    print('roots', rootsp, rootsq)
    for rp, rq in itertools.product(rootsp, rootsq):
        solution = CRT([int(rp), int(rq)],[p,q])
        flag = long_to_bytes(solution)
        if "ASIS" in flag:
            print(flag)
```

From this we get `ASIS{h0W_D0_3-th_R0Ot___3XtR4cT10n___AL90r17Hm_iN_Fq!!!?}`.

Complete solver [here](solver.sage)
