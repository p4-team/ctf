from Crypto.Util.number import *

size = 2048
rand_state = getRandomInteger(size // 2)


def keygen(size):
    q = getPrime(size)
    k = 2
    while True:
        p = q * k + 1
        if isPrime(p):
            break
        k += 1
    g = 2
    while True:
        if pow(g, q, p) == 1:
            break
        g += 1
    A = getRandomInteger(size) % q
    B = getRandomInteger(size) % q
    x = getRandomInteger(size) % q
    h = pow(g, x, p)
    return (g, h, A, B, p, q), (x,)


def rand(A, B, M):
    global rand_state
    rand_state, ret = (A * rand_state + B) % M, rand_state
    return ret


def encrypt(pubkey, m):
    g, h, A, B, p, q = pubkey
    assert 0 < m <= p
    r = rand(A, B, q)
    c1 = pow(g, r, p)
    c2 = (m * pow(h, r, p)) % p
    return (c1, c2)


pubkey, privkey = keygen(size)

m = bytes_to_long("flag{alamakota}")
c1, c2 = encrypt(pubkey, m)
c1_, c2_ = encrypt(pubkey, m)

print(pubkey)
print (c1, c2)
print (c1_, c2_)
