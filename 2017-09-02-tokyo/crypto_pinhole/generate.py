# Python 3
from Crypto.Util.number import *
from hashlib import sha1

bits = 1024

def LCM(x, y):
    return x * y // GCD(x, y)

def L(x, n):
    return (x - 1) // n

p = getStrongPrime(bits/2)
q = getStrongPrime(bits/2)
n = p*q
n2 = n*n

k = getRandomRange(0, n)
g = (1 + k*n) % n2

sk1 = LCM(p - 1, q - 1)
sk2 = inverse(L(pow(g, sk1, n2), n), n)

message = getRandomInteger(bits - 1)
with open("message", "w") as f:
    f.write(hex(message))
with open("flag", "w") as f:
    f.write("TWCTF{" + sha1(str(message).encode("ascii")).hexdigest() + "}\n")

with open("secretkey", "w") as f:
    f.write(hex(sk1) + "\n")
    f.write(hex(sk2) + "\n")

with open("publickey", "w") as f:
    f.write(hex(n) + "\n")
    f.write(hex(n2) + "\n")
    f.write(hex(g) + "\n")

def encrypt(m):
    r = getRandomRange(1, n2)
    c = pow(g, m, n2) * pow(r, n, n2) % n2
    return c

ciphertext = encrypt(message)
with open("ciphertext", "w") as f:
    f.write(hex(ciphertext) + "\n")

