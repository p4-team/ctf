#!/usr/bin/env sage
# coding=utf-8

from pubkey import P, n, e
from secret import flag
from os import urandom

R.<a> = GF(2^2049)

def encrypt(m):
    global n
    assert len(m) <= 256
    m_int = Integer(m.encode('hex'), 16)
    m_poly = P(R.fetch_int(m_int))
    c_poly = pow(m_poly, e, n)
    c_int = R(c_poly).integer_representation()
    c = format(c_int, '0256x').decode('hex')
    return c

if __name__ == '__main__':
    ptext = flag + os.urandom(256-len(flag))
    ctext = encrypt(ptext)
    with open('flag.enc', 'wb') as f:
        f.write(ctext)
