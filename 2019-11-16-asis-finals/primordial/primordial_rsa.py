#!/usr/bin/env python

import gmpy2
from Crypto.Util.number import *
import random
from flag import flag

def primorial(p):
    q = 1
    s = 1
    while q < p:
        r = gmpy2.next_prime(q)
        if r <= p:
            s *= r
            q = r
        else:
            break
    return s

def gen_prime(nbit):
    while True:
        s = getPrime(36)
        a = primorial(getPrime(random.randint(7, 9)))
        b = primorial(getPrime(random.randint(2, 5)))
        for r in range(10**3, 3*10**3, 2):
            p = s * a // b - r
            if gmpy2.is_prime(p) and len(bin(p)[2:]) == nbit:
                return int(p)

p, q = gen_prime(512), gen_prime(512)
e, n = 65537, p * q
flag = bytes_to_long(flag)
enc = pow(flag, e, n)
print 'n =', n
print 'enc =', enc