#!/usr/bin/env python3
from random import randrange
from Crypto.Cipher import AES

p = 2**128 - 33227

i = lambda x: pow(x, p-2, p)

def add(A, B):
    (u, v), (w, x) = A, B
    assert u != w or v == x
    if u == w: m = (3*u*w + 4*u + 1) * i(v+x)
    else: m = (x-v) * i(w-u)
    y = m*m - u - w - 2
    z = m*(u-y) - v
    return y % p, z % p

def mul(t, A, B=0):
    if not t: return B
    return mul(t//2, add(A,A), B if not t&1 else add(B,A) if B else A)

x = randrange(p)
aes = AES.new(x.to_bytes(16, 'big'), AES.MODE_CBC, bytes(16))
flag = open('flag.txt').read().strip()
cipher = aes.encrypt(flag.ljust((len(flag)+15)//16*16).encode())
print(*mul(x, (4, 10)), cipher.hex(), file=open('flag.enc', 'w'))

