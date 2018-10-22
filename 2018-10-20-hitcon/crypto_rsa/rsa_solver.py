import gmpy2
import itertools
import re

from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes

from crypto_commons.netcat.netcat_commons import send, receive_until_match, nc
from crypto_commons.oracle.lsb_oracle import lsb_oracle_from_bits
from crypto_commons.rsa.rsa_commons import modinv


def command(s, data, command):
    send(s, command)
    res = receive_until_match(s, "input: ")
    send(s, data.encode("hex"))
    res = receive_until_match(s, ".*\n")
    return re.findall("(.*)\s+", res)[0]


def enc(s, data):
    return command(s, data, 'A')


def dec(s, data):
    return command(s, data, 'B')


def recover_flag(enc, dec, flag, n):
    flag = int(flag, 16)
    x = flag
    bits = []
    lastchar = int(dec(long_to_bytes(flag)), 16)
    prev = lastchar
    multiplier = int(enc(long_to_bytes(2 ** 8)), 16)
    for i in range(128):
        x = x * multiplier
        expected_value = int(dec(long_to_bytes(x)), 16)
        real_x = prev
        for configuration in itertools.product([0, 1], repeat=8):
            res = real_x % 256
            for bit in configuration:
                res = res * 2
                if bit == 1:
                    res = res - n
            res = res % 256
            if res == expected_value:
                print(configuration)
                bits.extend(configuration)
                break
        prev = expected_value
    return long_to_bytes(lsb_oracle_from_bits(n, iter(bits)))[:-1] + chr(lastchar)


def recover_pubkey(enc):
    two = int(enc('\x02'), 16)
    three = int(enc('\x03'), 16)
    power_two = int(enc('\x04'), 16)
    power_three = int(enc('\x09'), 16)
    n = gmpy2.gcd(two ** 2 - power_two, three ** 2 - power_three)
    while n % 2 == 0:
        n = n / 2
    while n % 3 == 0:
        n = n / 3
    return n


def main():
    url = '18.179.251.168'
    # url = 'localhost'
    port = 21700
    s = nc(url, port)
    data = receive_until_match(s, "cmd:")
    flag = re.findall('Here is the flag!\s*(.*)\s*cmd:', data)[0]
    print(flag)
    encryptor = lambda data: enc(s, data)
    decryptor = lambda data: dec(s, data)
    n = recover_pubkey(encryptor)
    print(n)
    print(recover_flag(encryptor, decryptor, flag, n))


main()


def sanity_recover_pubkey():
    bitsize = 512
    p = getPrime(bitsize / 2)
    q = getPrime(bitsize / 2)
    e = 2 ** 20 - 1
    n = p * q
    phi = (p - 1) * (q - 1)
    d = modinv(e, phi)
    print(e, n)

    def encryptor(data):
        return long_to_bytes(pow(bytes_to_long(data), e, n)).encode("hex")

    recovered_n = recover_pubkey(lambda data: encryptor(data))
    print(recovered_n == n)


# sanity_recover_pubkey()


def sanity_recover_flag():
    bitsize = 512
    p = getPrime(bitsize / 2)
    q = getPrime(bitsize / 2)
    e = 65537
    n = p * q
    phi = (p - 1) * (q - 1)
    d = modinv(e, phi)
    flag = long_to_bytes(pow(bytes_to_long("alamakota"), e, n)).encode("hex")

    def encryptor(data):
        return long_to_bytes(pow(bytes_to_long(data), e, n)).encode("hex")

    def decryptor(data):
        return long_to_bytes(pow(bytes_to_long(data), d, n)).encode("hex")[-2:]

    dec = lambda data: decryptor(data)
    enc = lambda data: encryptor(data)
    print(recover_flag(enc, dec, flag, n))

# sanity_recover_flag()
