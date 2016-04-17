from Crypto.Util.number import getPrime, getRandomRange, GCD

def getBlumPrime(nbits):
    p = getPrime(nbits)
    while p % 4 != 3:
        p = getPrime(nbits)
    return p

def genKey(nbits):
    p = getBlumPrime(nbits/2)
    q = getBlumPrime(nbits/2)
    N = p * q

    return ((p,q), N)

def randQR(N):
    return pow(getRandomRange(1, N), 2, N)

def encrypt(m, N):
    return pow(m, 2, N)

def legendreSymbol(a, p):
    return pow(a, (p-1)/2, p)

def decrypt(c, p, q):
    if GCD(c, p*q) != 1:
        return None
    if legendreSymbol(c, p) != 1:
        return None
    if legendreSymbol(c, q) != 1:
        return None
    return pow(c, ((p-1)*(q-1) + 4) / 8, p*q)
