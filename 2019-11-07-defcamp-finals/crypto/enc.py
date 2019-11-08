#!/usr/bin/python
import binascii
import hashlib
import os


def rotl(num, bits=64):
    bit = num & (1 << (bits - 1))
    num <<= 1
    if (bit):
        num |= 1
    num &= (2 ** bits - 1)
    return num


def rotr(num, bits=64):
    num &= (2 ** bits - 1)
    bit = num & 1
    num >>= 1
    if (bit):
        num |= (1 << (bits - 1))
    return num


def encrypt(data, key):
    encrypted = []
    a, b, c = (int(key[i:i + 8], 16) for i in range(0, len(key), 8))
    for index, d in enumerate(data):
        keystream = (b & 0xff) ^ (c & 0xff)
        # print(keystream)
        # print(a & 0xff)
        d = (ord(d) - (a & 0xff)) ^ keystream
        d = d & 0xff
        encrypted.append(chr(d))
        a = rotr(a)
        b = rotl(b)
        c = rotl(c)
        print(index, hex(a & 0xff), hex(keystream))
    return hashlib.sha1(data).hexdigest() + "".join(encrypted).encode('hex')


def main():
    secret = 'DCTF{...}'
    key = binascii.b2a_hex(os.urandom(12))
    encrypted = encrypt(secret, key)
    print(encrypted)
    ct = 'a22d0fb9f707b153ab68472082d1f3e977a23f3dc0de469388ec3a56131943eba1873071f7fc01b5fc31b5335056286f5d7634735f35776a74'


main()
