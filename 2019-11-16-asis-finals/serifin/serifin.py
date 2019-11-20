#!/usr/bin/env python

from Crypto.Util.number import *
from flag import flag
import gmpy2

def serifin(a, l):
    S, s = a, a
    while True:
        S += float(a)/float(l)
        if S - s < .0001:
            return int(S) + 1
        else:
            s, a = S, float(a)/float(l)

def genPrime(nbit):
    while True:
        p = getPrime(512)
        if p % 9 == 1 and p % 27 >= 2:
            q = gmpy2.next_prime(serifin(p, 3) + serifin(p, 9) + serifin(p, 27))
            if q % 9 == 1 and q % 27 >= 2:
                return int(p), int(q)

def encrypt(m, n):
    m = bytes_to_long(m)
    assert m < n
    return pow(m, 3, n)

nbit = 512
p, q = genPrime(nbit)
n = p * q
c = encrypt(flag, n)

print 'c =', c
print 'n =', n