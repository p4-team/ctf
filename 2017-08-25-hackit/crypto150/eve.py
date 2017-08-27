from z3 import *


def encrypt(data, lfsr, poly):
    result = [ord(c) for c in data]
    for i in range(len(data)):
        for j in range(7, -1, -1):
            lsb = lfsr & 1
            result[i] ^= (lsb << j)
            lfsr >>= 1
            if lsb:
                lfsr ^= poly
    return "".join([chr(c) for c in result])


def recover_key(known_plaintext_part, ciphertext):
    lfsr = z3.BitVec('x', 32)
    x = lfsr
    poly = z3.BitVec('y', 32)
    y = poly
    s = Solver()
    for i in range(len(known_plaintext_part)):
        for j in range(7, -1, -1):
            lsb = ((ord(known_plaintext_part[i]) ^ ord(ciphertext[i])) & (1 << j)) >> j
            s.add(lfsr & 1 == lsb)
            lfsr = LShR(lfsr, 1)
            if lsb:
                lfsr ^= poly
    print(s.check())
    return int(str(s.model()[x])), int(str(s.model()[y]))


def main():
    with codecs.open("message.txt", "rb") as input_file:
        ciphertext = input_file.read()
        input_data = 'Hello, Alice!'
        p, k = recover_key(input_data, ciphertext)
        print(p, k)
        print(encrypt(ciphertext, p, k))


main()
