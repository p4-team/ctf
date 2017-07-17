#!/usr/bin/env python3
from Crypto.Util import number
from binascii import hexlify, unhexlify
from gmpy2 import next_prime, powmod, gcdext, gcd
from itertools import count
from random import randint


class MPRSA(object):
    def __init__(self):
        self.public_key = None
        self.secret_key = None

    def key_gen(self, bits, prime_numbers=4):
        delta = randint(5, 15)
        bit_prime = int(bits // prime_numbers)

        P = [next_prime(number.getPrime(bit_prime) + 1)]
        for i in range(1, prime_numbers):
            P.append(next_prime(P[i - 1] * delta))

        n = self.__compute_module(P)
        phi = self.__compute_phi(P)

        for d_next in count(int(pow(P[0] // 2, 0.5)), -1):
            g, e, __ = gcdext(d_next, phi)
            if (1 < e < n) and (g == 1) and (gcd(phi, e) == 1):
                d = d_next
                break

        self.public_key = (e, n)
        self.secret_key = (d, n)

    def import_keys(self, public_key, secret_key):
        self.public_key = public_key
        self.secret_key = secret_key

    def export_keys(self):
        return self.public_key, self.secret_key

    @staticmethod
    def __compute_module(primes):
        n = 1
        for prime in primes:
            n *= prime
        return n

    @staticmethod
    def __compute_phi(primes):
        phi = 1
        for prime in primes:
            phi *= (prime - 1)
        return phi

    @staticmethod
    def __encode_message(data):
        return int(hexlify(data), 16)

    @staticmethod
    def __decode_message(data):
        return unhexlify(format(data, "x"))

    def encryption(self, ptext):
        data = self.__encode_message(ptext)
        return powmod(data, self.public_key[0], self.public_key[1])

    def decryption(self, ctext):
        data = powmod(ctext, self.secret_key[0], self.secret_key[1])
        return MPRSA.__decode_message(data)
