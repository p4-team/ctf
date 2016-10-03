#!/usr/bin/env python3
import gmpy2
from Crypto.Hash import SHA256

e = 65537
order = 'Give me the flag. This is an order!'

def sqrt(n, p):
    if p % 4 != 3: raise NotImplementedError()
    return pow(n, (p + 1) // 4, p) if pow(n, (p - 1) // 2, p) == 1 else None

# just elliptic-curve addition, nothing to see here
def add(q, a, b, P, Q):
    if () in (P, Q):
        return (P, Q)[P == ()]
    (Px, Py), (Qx, Qy) = P, Q
    try:
        if P != Q: lam = (Qy - Py) * gmpy2.invert(Qx - Px, q) % q
        else: lam = (3 * Px ** 2 + a) * gmpy2.invert(2 * Py, q) % q
    except ZeroDivisionError:
        return ()
    Rx = (lam ** 2 - Px - Qx) % q
    Ry = (lam * Px - lam * Rx - Py) % q
    return int(Rx), int(Ry)

# just elliptic-curve scalar multiplication, nothing to see here
def mul(q, a, b, n, P):
    R = ()
    while n:
        if n & 1: R = add(q, a, b, R, P)
        P, n = add(q, a, b, P, P), n // 2
    return R

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

