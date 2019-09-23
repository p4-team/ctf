import os
import gmpy2

flag = int(open('flag.txt').read().encode("hex"), 16)

def genPrime(bits):
    data = os.urandom(bits/8)
    number = int(data.encode("hex"), 16)
    return gmpy2.next_prime(number)


e = 1667


# rsa1: p - 700 bits q - 1400 bits

p = genPrime(700)
q = genPrime(1400)

n = p*q
phi = (p-1)*(q-1)
d = gmpy2.powmod(e, -1, phi)

rsa1 = (n, d)


# rsa2: p - 700 bits, q - 700 bits, r = 700 bits

p = genPrime(700)
q = genPrime(700)
r = genPrime(700)

n = p*q*r
phi = (p-1)*(q-1)*(r-1)
d = gmpy2.powmod(e, -1, phi)

rsa2 = (n, d)

# rsa3: p - 700 bits, q - 700 bits, r = 700 bits

p = genPrime(700)
q = genPrime(700)

n = p*q*r
phi = (p-1)*(q-1)*(r-1)
d = gmpy2.powmod(e, -1, phi)

rsa3 = (n, d)

# rsa4: p - 700 bits, q - 700 bits

p = genPrime(700)
q = genPrime(700)

n = p*q*q
phi = (p-1)*(q-1)*q
d = gmpy2.powmod(e, -1, phi)

rsa4 = (n, d)

rsa = sorted([rsa1, rsa2, rsa3, rsa4])


for n, d in rsa:
    print 'pubkey:', n, d % (2**1050)
    flag = pow(flag, e, n)

print 'encrypted flag', flag
