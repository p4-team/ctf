import gmpy2
import hashlib
from Crypto.Util.number import size, getRandomRange, GCD, getStrongPrime, inverse, getRandomInteger
from crypto_commons.netcat.netcat_commons import nc, send


class RemoteOracle:
    def __init__(self):
        url = "ppc2.chal.ctf.westerns.tokyo"
        port = 38264
        self.s = nc(url, port)

    def get_lsb(self, payload):
        send(self.s, hex(long(payload))[2:-1])
        data = self.s.recv(9999)
        if data[0] != '1' and data[0] != '0':
            print("WTF", data)
        return data[0]


def LCM(x, y):
    return x * y // GCD(x, y)


def L(x, n):
    return (x - 1) // n


def encrypt(m, g, n, n2):
    r = getRandomRange(1, n2)
    c = pow(g, m, n2) * pow(r, n, n2) % n2
    return c


def decrypt(c, sk1, sk2, n, n2):
    return L(pow(c, sk1, n2), n) * sk2 % n


def recover_high_bits(low, oracle, n, n2, g, ct):
    print('cracking high bits')
    mbits = size(n)
    b = mbits // 2
    result_bits = []
    subtractor = n - low
    sub = encrypt(subtractor, g, n, n2)
    ct_sub = (ct * sub) % n2
    for i in range(b):
        divisor = inverse(2 ** i, n)
        payload = pow(ct_sub, divisor, n2)
        lsb = oracle.get_lsb(payload)
        result_bits.append(str(lsb))
    return "".join(result_bits[::-1])


def recover_low_bits(oracle, n, n2, g, ct):
    print('cracking low bits')
    mbits = size(n)
    bits_to_recover = mbits // 2
    result_bits = []
    initial_state = oracle.get_lsb(ct)
    for i in range(bits_to_recover):
        filling = ['0' if known_bit == '1' else '1' for known_bit in result_bits]
        add = int("".join(filling + ['1']), 2) << (bits_to_recover - i - 1)
        payload = (ct * encrypt(add, g, n, n2)) % n2
        lsb = oracle.get_lsb(payload)
        if lsb != initial_state:
            result_bits.append('1')
        else:
            result_bits.append('0')
    result = "".join(result_bits)
    return result


def main():
    pass
    print('cracking...')
    n = 0xadd142708d464b5c50b936f2dc3a0419842a06741761e160d31d6c0330f2c515b91479f37502a0e9ddf30f7a18c71ef1eba993bdc368f7e90b58fb9fdbfc0d9ee0776dc629c8893a118e0ad8fc05633f0b9b4ab20f7c6363c4625dbaedf5a8d8799abc8353cb54bbfeab829792eb57837030900d73a06c4e87172599338fd5b1
    n2 = 0x76047ed9abf5e8f5fc2a2f67162eb2bc0359c3ffa3585ba846de7181d815dba75738c65f79d8923c061b55933fbd391e48da3cd94ab6c5b09f7c9e80dea0b5848a8cf74cd27e429ca3d4647d81d4deae1ec76ffd732124c0e31fe6fbed1103135f19f3fcc2ec04a9f694c4468597b12e1c0020d478b82a21ca899e76f6f28d32cef1eea558fd8fddf1a870ceae356809cf567c1627fdcbb967e4c5996cf15119ab5c058d8bf4280efc5eff7659d717ccfa08169681a2445a17874099e448278fdf7e99b7df1a2e309592e2dc3c6a762a97d46e4b8a5e2824e52e30a241bdce7aa67f788866e41b2a2282f7d2c5fa606ad4541a5e46a22bab53e33786f41e0461
    g = 0x676ae3e2f70e9a5e35b007a70f4e7e113a77f0dbe462d867b19a67839f41b6e66940c02936bb73839d98966fc01f81b2b79c834347e71de6d754b038cb83f27bac6b33bf7ebd25de75a625ea6dd78fb973ed8637d32d2eaf5ae412b5222c8efea99b183ac823ab04219f1b700b207614df11f1f3759dea6d722635f45e453f6eae4d597dcb741d996ec72fe3e54075f6211056769056c5ad949c8becec7e179da3514c1f110ce65dc39300dfdce1170893c44f334a1b7260c51fb71b2d4dc6032e907bbaeebff763665e38cdfe418039dc782ae46f80e835bfd1ef94aeaba3ab086e61dab2ff99f600eb8d1cd3cf3fc952b56b561adc2de2097e7d04cb7c556
    ct = 0x2ab54e5c3bde8614bd0e98bf838eb998d071ead770577333cf472fb54bdc72833c3daa76a07a4fee8738e75eb3403c6bcbd24293dc2b661ab1462d6d6ac19188879f3b1c51e5094eb66e61763df22c0654174032f15613a53c0bed24920fd8601d0ac42465267b7eba01a6df3ab14dd039a32432003fd8c3db0501ae2046a76a8b1e56f456a2d40e2dd6e2e1ab77a8d96318778e8a61fe32d03407fc6a7429ec1fb66fc68c92e33310b3a574bde7818eb7089d392a30d07c85032a3d34fd589889ff6053fb19592dbb647a38063c5b403d64ee94859d9cf9b746041e5494ab7413f508d814c4b3bba29bca41d4464e1feb2bce27b3b081c85b455e035a138747L
    oracle = RemoteOracle()
    low_bits = recover_low_bits(oracle, n, n2, g, ct)
    print(low_bits)
    high_bits = recover_high_bits(int(low_bits, 2), oracle, n, n2, g, ct)
    print(high_bits)
    print(len(low_bits + high_bits))
    print(high_bits + low_bits)
    message = int(high_bits + low_bits, 2)
    print(message)
    print("TWCTF{" + hashlib.sha1(str(message).encode("ascii")).hexdigest() + "}")


# main()


def sanity():
    bits = 1024
    p = getStrongPrime(bits / 2)
    q = getStrongPrime(bits / 2)
    n = p * q
    n2 = n * n
    k = getRandomRange(0, n)
    g = (1 + k * n) % n2
    sk1 = LCM(p - 1, q - 1)
    sk2 = inverse(L(pow(g, sk1, n2), n), n)
    pt = getRandomInteger(bits - 1)

    ct = encrypt(pt, g, n, n2)
    mult = 123
    ct20 = pow(ct, mult, n2)
    print(decrypt(ct20, sk1, sk2, n, n2) == (mult * pt) % n)
    divisor = 123
    ct_2 = pow(ct, inverse(divisor, n), n2)
    print(divisor * decrypt(ct_2, sk1, sk2, n, n2) % n == pt)
    add = 123
    ct_add = ct * encrypt(add, g, n, n2)
    print(decrypt(ct_add, sk1, sk2, n, n2) == (pt + add) % n)
    sub = 123
    ct_sub = ct * encrypt(n - sub, g, n, n2)
    print(decrypt(ct_sub, sk1, sk2, n, n2) == (pt - sub) % n)
    ct_comb = pow(ct * encrypt(sub, g, n, n2), mult, n2)
    print(decrypt(ct_comb, sk1, sk2, n, n2) == (mult * (pt + sub)) % n)
    ct_comb2 = pow(ct, mult, n2) * encrypt(sub, g, n, n2)
    print(decrypt(ct_comb2, sk1, sk2, n, n2) == (mult * pt + sub) % n)


# sanity()


class LocalOracle:
    def __init__(self, sk1, sk2, n, n2, b):
        self.sk1 = sk1
        self.sk2 = sk2
        self.n = n
        self.n2 = n2
        self.b = b

    def get_lsb(self, payload):
        decrypted = decrypt(payload, self.sk1, self.sk2, self.n, self.n2)
        return (decrypted >> self.b) & 1


def testing_full(i):
    print('running full test %d times' % i)
    bits = 128
    for i in range(100):
        p = gmpy2.next_prime(2 ** (bits / 2))
        q = gmpy2.next_prime(p)
        n = p * q
        n2 = n * n
        mbits = size(n)
        b = mbits // 2
        k = getRandomRange(0, n)
        g = (1 + k * n) % n2
        sk1 = LCM(p - 1, q - 1)
        sk2 = inverse(L(pow(g, sk1, n2), n), n)
        pt = getRandomInteger(bits - 1)
        ct = encrypt(pt, g, n, n2)

        assert decrypt(encrypt(pt, g, n, n2), sk1, sk2, n, n2) == pt

        print(pt)
        print(bin(pt)[2:])
        low = recover_low_bits(LocalOracle(sk1, sk2, n, n2, b), n, n2, g, ct)
        print(low)
        high = recover_high_bits(int(low, 2), LocalOracle(sk1, sk2, n, n2, b), n, n2, g, ct)
        print(high)
        result = int(high + low, 2)
        print(result)
        assert result == pt

# testing_full(100)
