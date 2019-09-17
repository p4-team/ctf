# During CTF we reversed encryption using z3 to solve round-by-round.
#
# The decryptor below has been implemented after CTF as an excercise.


def int64(value):
    return value & 0xffffffffffffffff


def rol64(value, shift):
    return (value << shift) | (value >> (0x40 - shift))


def key_schedule(key):
    key_A, key_B = key
    yield key_A
    for round in xrange(0x1f):
        key_B = int64(round ^ (key_A + rol64(key_B, 0x38)))
        key_A = int64(key_B ^ rol64(key_A, 3))
        yield key_A


def encrypt(key, plaintext):
    data_A, data_B = plaintext
    for round_key in key_schedule(key):
        data_B = int64(round_key ^ (data_A + rol64(data_B, 0x38)))
        data_A = int64(data_B ^ rol64(data_A, 3))
    ciphertext = data_A, data_B
    return ciphertext


def decrypt(key, ciphertext):
    data_A, data_B = ciphertext
    for round_key in reversed(list(key_schedule(key))):
        data_A = int64(rol64(data_A ^ data_B, 0x3d))
        data_B = int64(rol64(int64((data_B ^ round_key) - data_A), 8))
    plaintext = data_A, data_B
    return plaintext
