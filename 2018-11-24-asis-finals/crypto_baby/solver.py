import itertools
from multiprocessing import freeze_support

from crypto_commons.brute.brute import brute
from crypto_commons.generic import bytes_to_long, get_primes, factor_p, multiply, long_to_bytes


def encrypt(exp, num, key):
    assert key >> 512 <= 1
    num = num + key
    blinded_bits = bin(num)[2:][::-1]
    C, i = 0, 1
    print(blinded_bits)
    for b in blinded_bits:
        C += int(b) * (exp ** i + (-1) ** i)
        i += 1
    try:
        enc = hex(C)[2:].rstrip('L').decode('hex')
    except:
        enc = ('0' + hex(C)[2:].rstrip('L')).decode('hex')
    return enc


def subsets(s):
    for cardinality in range(len(s) + 1):
        for c in itertools.combinations(s, cardinality):
            yield c


def recover_bits(encrypted_flag, exp):
    bits = []
    while True:
        if encrypted_flag == 0:
            return bits
        encrypted_flag = encrypted_flag / exp
        bit = encrypted_flag % exp
        if bit != 0 and bit != 1:
            return None
        else:
            bits.append(bit)


def factor_worker(data):
    flag, i, primes = data
    factors, residue = factor_p(flag, primes)
    print('factors', i, factors)
    for potential_exp in subsets(factors):
        if len(potential_exp) == 0:
            continue
        exp = multiply(potential_exp)
        bits = recover_bits(flag, exp)
        if bits is not None:
            data = int("".join(map(str, bits[::-1])), 2)
            data = long_to_bytes(data)
            if "IHDR" in data and "PNG" in data:
                print("FOUND!", i, flag, data)
                save_png(data, i, exp)
                return data


def save_png(result, i, exp):
    if result is not None:
        png_trailer = "00 00 00 00 49 45 4e 44 ae 42 60 82 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
        png_trailer = png_trailer.replace(" ", "").decode("hex")
        result = result[:-14] + png_trailer
        f = open("out" + str(i) + "_" + str(exp) + ".png", 'wb')
        f.write(result)
        f.close()


def decrypt_paralell(file):
    exp_range = 2  # was testing 22
    diff = 18  # was testing 1024
    ct = open(file, 'rb').read()
    encrypted_flag = bytes_to_long(ct)
    print(encrypted_flag)
    primes = get_primes(2 ** exp_range)
    dataset = [(encrypted_flag + i, i, primes) for i in range(-diff, diff)]
    results = brute(factor_worker, dataset, processes=6)
    return results


def main():
    decrypt_paralell('flag.enc')


if __name__ == '__main__':
    freeze_support()
    main()
