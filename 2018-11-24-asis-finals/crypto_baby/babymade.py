#!/usr/bin/env python

from secret import exp, key

def encrypt(exp, num, key):
    assert key >> 512 <= 1
    num = num + key
    msg = bin(num)[2:][::-1]
    C, i = 0, 1
    for b in msg:
        C += int(b) * (exp**i + (-1)**i)
        i += 1
    try:
        enc = hex(C)[2:].rstrip('L').decode('hex')
    except:
        enc = ('0' + hex(C)[2:].rstrip('L')).decode('hex')
    return enc

#-----------------------------
# Encryption:
#-----------------------------

flag = open('flag.png', 'r').read()
msg = int(flag.encode('hex'), 16)
enc = encrypt(exp, msg, key)

f = open('flag.enc', 'w')
f.write(enc)
f.close()