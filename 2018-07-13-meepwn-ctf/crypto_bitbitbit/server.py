#!/usr/bin/env python2

from flag import FLAG
from gmpy2 import next_prime, powmod
from random import randint, getrandbits
from hashlib import sha512, sha256
from os import urandom

introduction = """
 .--.     .-------------------------------.
 | _|     |                               |
 | O O   <  Hey man, wanna mid some bit ? |
 |  |  |  |                               |
 || | /   `-------------------------------'
 |`-'|
 `---'
Whoever says live is simple, is the one never actually live. :)) 
"""


def pad(num, length):
    result = bin(num).lstrip('0b').strip('L')
    result = result + '0' * (length - len(result))
    return int(result, 2)


def xor(a, b):
    return ''.join(chr(ord(i) ^ ord(j)) for i, j in zip(a, b))


def gen_key():
    t1 = randint(768, 928)
    t2 = 1024 - t1

    if t1 > t2:
        t1, t2 = t2, t1
    assert t1 < t2

    p2 = pad(getrandbits(1024 - t2) << t2, 1024)
    p0 = pad(getrandbits(t1), t1)

    q2 = pad(getrandbits(1024 - t2) << t2, 1024)
    q0 = pad(getrandbits(t1), t1)

    r = pad(getrandbits(t2 - t1) << t1, t2)

    p = next_prime((p2 ^ r ^ p0))
    q = next_prime((q2 ^ r ^ q0))

    N = p * q

    return N, t2 - t1, p0 - q0 


def proof_of_shit():
    """
    This function has very special purpose 
    :)) Simply to screw you up
    """
    raw = urandom(6)
    print 'prefix = {}'.format(raw.encode('hex'))
    challenge = raw_input('Challenge: ')
    temp = sha256(raw + challenge).hexdigest()
    if temp.startswith('25455'):
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        assert proof_of_shit() == True
        N, delta, gamma = gen_key()

        m = int(FLAG.encode('hex'), 16)
        c = powmod(m, 0x10001, N)

        print introduction
        print 'N = {}'.format(N)
        print 'delta = {}'.format(delta)
        print 'gamma = {}'.format(gamma)
        print 'ciphertext = {}'.format(c)

    except AssertionError:
        print "Take your time and think of the inputs."
