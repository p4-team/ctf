from Crypto.Util.number import *

p = getPrime(157)
q = getPrime(157)
n = p * q
e = 31415926535897932384

flag = open('flag').read().strip()
assert len(flag) == 50

m = int(flag.encode('hex'), 16)
c = pow(m, e, n)
print 'n =', n
print 'e =', e
print 'c =', c
