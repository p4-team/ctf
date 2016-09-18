## Still Broken Box (Crypto, 400p)

###ENG
[PL](#pl-version)

The task was very similar to https://github.com/p4-team/ctf/tree/master/2016-09-16-csaw/broken_box but this time we could not recover all the bits of the key.
We could get only some fraction of LSB bits, but there is a theorem stating that we need only n/4 of the LSB bits to recover full key, as long as `e` is reasonably small.

We used the same code as previously to mine faulty signatures and then to recover some bits of `d`.
Then we applited mentioned theorem to recover the whole key.
The recovery description can be found here: http://honors.cs.umd.edu/reports/lowexprsa.pdf

We used the sage code:

```sage
# partial_d.sage

def partial_p(p0, kbits, n):
    PR.<x> = PolynomialRing(Zmod(n))
    nbits = n.nbits()

    f = 2^kbits*x + p0
    f = f.monic()
    roots = f.small_roots(X=2^(nbits//2-kbits), beta=0.3)  # find root < 2^(nbits//2-kbits) with factor >= n^0.3
    if roots:
        x0 = roots[0]
        p = gcd(2^kbits*x0 + p0, n)
        return ZZ(p)

def find_p(d0, kbits, e, n):
    X = var('X')

    for k in xrange(1, e+1):
        results = solve_mod([e*d0*X - k*X*(n-X+1) + k*n == X], 2^kbits)
        for x in results:
            p0 = ZZ(x[0])
            p = partial_p(p0, kbits, n)
            if p:
                return p


if __name__ == '__main__':
    print "start!"
    n = 123541066875660402939610015253549618669091153006444623444081648798612931426804474097249983622908131771026653322601466480170685973651622700515979315988600405563682920330486664845273165214922371767569956347920192959023447480720231820595590003596802409832935911909527048717061219934819426128006895966231433690709
    e = 97

    beta = 0.5
    epsilon = beta^2/7

    nbits = n.nbits()
    kbits = 300
    d0 = 48553333005218622988737502487331247543207235050962932759743329631099614121360173210513133
    print "lower %d bits (of %d bits) is given" % (kbits, nbits)

    p = find_p(d0, kbits, e, n)
    print "found p: %d" % p
```

Which gave us the modulus factor `p`.
With that we simply decrypted the flag using:

```python
import gmpy2


def long_to_bytes(flag):
    flag = str(hex(flag))[2:-1]
    return "".join([chr(int(flag[i:i + 2], 16)) for i in range(0, len(flag), 2)])

p = 11508259255609528178782985672384489181881780969423759372962395789423779211087080016838545204916636221839732993706338791571211260830264085606598128514985547
n = 123541066875660402939610015253549618669091153006444623444081648798612931426804474097249983622908131771026653322601466480170685973651622700515979315988600405563682920330486664845273165214922371767569956347920192959023447480720231820595590003596802409832935911909527048717061219934819426128006895966231433690709
q = n/p
e = 97

assert p*q == n
d = gmpy2.invert(e, (p-1)*(q-1))
flag = 96324328651790286788778856046571885085117129248440164819908629761899684992187199882096912386020351486347119102215930301618344267542238516817101594226031715106436981799725601978232124349967133056186019689358973953754021153934953745037828015077154740721029110650906574780619232691722849355713163780985059673037
pt = pow(flag, d, n)
print(long_to_bytes(pt))
```

and got `flag{n3v3r_l34k_4ny_51n6l3_b17_0f_pr1v473_k3y}`

###PL version

Zadanie było bardzo podobne do https://github.com/p4-team/ctf/tree/master/2016-09-16-csaw/broken_box ale tym razem nie mogliśmy odzyskać wszystkich bitów klucza.
Mogliśmy dostać jedynie część niskich bitów klucza, niemniej istnieje twierdzenie mówiące że wystarczy nam n/4 najniższych bitów do odzyskania całego klucza, o ile `e` jest względnie małe.

Użyliśmy tego samego kodu co wcześniej aby pobrać błędne sygnatury i odzyskać niskie bity `d`.
Następnie zastosowaliśmy wspomniane twierdzenie aby odzyskać cały klucz.
Opis mechanizmu odzyskiwania klucza można znaleźć tu: http://honors.cs.umd.edu/reports/lowexprsa.pdf

Użyliśmy kodu:

```sage
# partial_d.sage

def partial_p(p0, kbits, n):
    PR.<x> = PolynomialRing(Zmod(n))
    nbits = n.nbits()

    f = 2^kbits*x + p0
    f = f.monic()
    roots = f.small_roots(X=2^(nbits//2-kbits), beta=0.3)  # find root < 2^(nbits//2-kbits) with factor >= n^0.3
    if roots:
        x0 = roots[0]
        p = gcd(2^kbits*x0 + p0, n)
        return ZZ(p)

def find_p(d0, kbits, e, n):
    X = var('X')

    for k in xrange(1, e+1):
        results = solve_mod([e*d0*X - k*X*(n-X+1) + k*n == X], 2^kbits)
        for x in results:
            p0 = ZZ(x[0])
            p = partial_p(p0, kbits, n)
            if p:
                return p


if __name__ == '__main__':
    print "start!"
    n = 123541066875660402939610015253549618669091153006444623444081648798612931426804474097249983622908131771026653322601466480170685973651622700515979315988600405563682920330486664845273165214922371767569956347920192959023447480720231820595590003596802409832935911909527048717061219934819426128006895966231433690709
    e = 97

    beta = 0.5
    epsilon = beta^2/7

    nbits = n.nbits()
    kbits = 300
    d0 = 48553333005218622988737502487331247543207235050962932759743329631099614121360173210513133
    print "lower %d bits (of %d bits) is given" % (kbits, nbits)

    p = find_p(d0, kbits, e, n)
    print "found p: %d" % p
```

Który dał nam czynnik `p` modulusa.
Następnie po prostu zdeszyfrowaliśmy flagę:

```python
import gmpy2


def long_to_bytes(flag):
    flag = str(hex(flag))[2:-1]
    return "".join([chr(int(flag[i:i + 2], 16)) for i in range(0, len(flag), 2)])

p = 11508259255609528178782985672384489181881780969423759372962395789423779211087080016838545204916636221839732993706338791571211260830264085606598128514985547
n = 123541066875660402939610015253549618669091153006444623444081648798612931426804474097249983622908131771026653322601466480170685973651622700515979315988600405563682920330486664845273165214922371767569956347920192959023447480720231820595590003596802409832935911909527048717061219934819426128006895966231433690709
q = n/p
e = 97

assert p*q == n
d = gmpy2.invert(e, (p-1)*(q-1))
flag = 96324328651790286788778856046571885085117129248440164819908629761899684992187199882096912386020351486347119102215930301618344267542238516817101594226031715106436981799725601978232124349967133056186019689358973953754021153934953745037828015077154740721029110650906574780619232691722849355713163780985059673037
pt = pow(flag, d, n)
print(long_to_bytes(pt))
```

i dostalismy `flag{n3v3r_l34k_4ny_51n6l3_b17_0f_pr1v473_k3y}
