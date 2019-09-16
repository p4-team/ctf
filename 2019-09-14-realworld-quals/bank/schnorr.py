import hashlib
import binascii
import unittest

from Crypto.Random import random

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)

# back-ports for python2 from https://stackoverflow.com/questions/16022556/has-python-3-to-bytes-been-back-ported-to-python-2-7
def to_bytes(n, length, byteorder='big'):
    h = hex(n)[2:].rstrip('L')
    print 'h', h
    s = ('0'*(len(h) % 2) + h).zfill(length*2).decode('hex')
    return s if byteorder == 'big' else s[::-1]

def from_bytes(s, byteorder='big'):
    return int(s.encode('hex'), 16)

def point_add(p1, p2):
    if (p1 is None):
        return p2
    if (p2 is None):
        return p1
    if (p1[0] == p2[0] and p1[1] != p2[1]):
        return None
    if (p1 == p2):
        lam = (3 * p1[0] * p1[0] * pow(2 * p1[1], p - 2, p)) % p
    else:
        lam = ((p2[1] - p1[1]) * pow(p2[0] - p1[0], p - 2, p)) % p
    x3 = (lam * lam - p1[0] - p2[0]) % p
    return (x3, (lam * (p1[0] - x3) - p1[1]) % p)

def point_mul(p, n):
    r = None
    for i in range(256):
        if ((n >> i) & 1):
            r = point_add(r, p)
        p = point_add(p, p)
    return r

def bytes_point(p):
    return (b'\x03' if p[1] & 1 else b'\x02') + to_bytes(p[0], 32, byteorder="big")

def sha256(b):
    return from_bytes(hashlib.sha256(b).digest(), byteorder="big")

def on_curve(point):
    return (pow(point[1], 2, p) - pow(point[0], 3, p)) % p == 7

def jacobi(x):
    return pow(x, (p - 1) // 2, p)

def schnorr_sign(msg, seckey):
    k = sha256(to_bytes(seckey, 32, byteorder="big") + msg)
    R = point_mul(G, k)
    if jacobi(R[1]) != 1:
        k = n - k
    e = sha256(to_bytes(R[0], 32, byteorder="big") + bytes_point(point_mul(G, seckey)) + msg)
    return to_bytes(R[0], 32, byteorder="big") + to_bytes(((k + e * seckey) % n), 32, byteorder="big")

def schnorr_verify(msg, pubkey, sig):
    if (not on_curve(pubkey)):
        return False
    r = from_bytes(sig[0:32], byteorder="big")
    s = from_bytes(sig[32:64], byteorder="big")
    if r >= p or s >= n:
        return False
    e = sha256(sig[0:32] + bytes_point(pubkey) + msg)
    R = point_add(point_mul(G, s), point_mul(pubkey, n - e))
    if R is None or jacobi(R[1]) != 1 or R[0] != r:
        return False
    return True

def generate_keys():
    privKey = random.randint(5, p-1)
    pubKey = point_mul(G, privKey)
    return privKey, pubKey

def create_input(private_key, public_key, message, signature):
    return dict(
            private_key=private_key,
            public_key=public_key,
            message=bytearray.fromhex(message),
            signature=bytearray.fromhex(signature))


