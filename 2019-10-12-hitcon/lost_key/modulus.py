import random

from crypto_commons.generic import bytes_to_long, multiply, factor, long_to_bytes
from crypto_commons.netcat.netcat_commons import nc, receive_until_match, receive_until, send
from crypto_commons.rsa.rsa_commons import gcd_multi


def prepare_values():
    prefix = bytes_to_long("X: ")
    factors, _ = factor(prefix)
    random.shuffle(factors)
    base1 = multiply(factors[:len(factors) / 2])
    base2 = multiply(factors[len(factors) / 2:])
    assert base1 * base2 == prefix

    shift = 5
    x = base1 * 256 ** shift + 0
    y = base2 * 256 ** shift + 0
    z = base1 * 256 ** shift + 1
    v = base2 * 256 ** shift + 1

    A = x * y
    B = z * v
    C = x * v
    D = y * z
    assert (A * B == C * D == x * y * z * v)

    for x in [A, B, C, D]:
        assert (long_to_bytes(x)[:3] == 'X: ')
        assert (len(long_to_bytes(x)) < 16)
    return A, B, C, D


def get_kn():
    host = "3.115.26.78"
    port = 31337
    s = nc(host, port)
    receive_until_match(s, "! ")
    flag_ct = receive_until(s, "\n")[:-1]
    plaintexts = [long_to_bytes(x)[3:] for x in prepare_values()]
    results = []
    for pt in plaintexts:
        receive_until_match(s, ": ")
        send(s, pt.encode("hex"))
        res = receive_until(s, "\n")[:-1]
        results.append(res)
    s.close()

    CTA = int(results[0], 16)
    CTB = int(results[1], 16)
    CTC = int(results[2], 16)
    CTD = int(results[3], 16)

    kn = (CTA * CTB) - (CTD * CTC)
    print("Got k*N", kn)
    return kn


def main():
    kns = [get_kn() for i in range(5)]
    possible_n = gcd_multi(kns)
    print('possible n', possible_n)


main()


def sanity():
    from Crypto.Util.number import getPrime
    e = 65537
    p = getPrime(512)
    q = getPrime(512)
    n = p * q

    A, B, C, D = prepare_values()

    CTA = pow(A, e, n)
    CTB = pow(B, e, n)
    CTC = pow(C, e, n)
    CTD = pow(D, e, n)

    assert ((CTA * CTB) % n == (CTD * CTC) % n)
    assert ((CTA * CTB) - (CTD * CTC)) % n == 0

# sanity()
