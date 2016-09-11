from Crypto.Util.number import *
from gmpy import *

def gen_prime(nbit):
	while True:
		prime = getPrime(nbit)
		if prime % 3 == 2:
			return prime

def add(a, b, n):
    if a == 0:
        return b
    if b == 0:
        return a
    l = ((b[1] - a[1]) * invert(b[0] - a[0], n)) % n
    x = (l*l - a[0] - b[0]) % n
    y = (l*(a[0] - x) - a[1]) % n
    return (x, y)

def double(a, A, n):
    if a == 0:
        return a
    l = ((3*a[0]*a[0] + A) * invert(2*a[1], n)) % n
    x = (l*l - 2*a[0]) % n
    y = (l*(a[0] - x) - a[1]) % n
    return (x, y)

def multiply(point, exponent, A, n):
    r0 = 0
    r1 = point
    for i in bin(exponent)[2:]:
        if i == '0':
            r1 = add(r0, r1, n)
            r0 = double(r0, A, n)
        else:
            r0 = add(r0, r1, n)
            r1 = double(r1, A, n)
    return r0

def gen_keypair(e, nbit):
    p = gen_prime(nbit)
    q = gen_prime(nbit)
    n = p*q
    lcm = (p+1)*(q+1)/GCD(p+1, q+1)
    d = invert(e, lcm)
    pubkey = (n, e)
    privkey = (n, d)
    return pubkey, privkey

def encrypt(msg, pubkey):
    n, e = pubkey
    if msg < n:
        while True:
            r = getRandomRange(1, n)
            m1, m2 = r - msg, r
            if m1 > 0:
                break
        c1, c2 = multiply((m1, m2), e, 0, n)
        return (int(c1), int(c2))
    else:
        return 'Error!!!'
