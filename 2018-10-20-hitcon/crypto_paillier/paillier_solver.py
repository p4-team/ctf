import re

from Crypto.Util.number import getPrime

from crypto_commons.asymmetric.asymmetric import paillier_encrypt_simple, paillier_decrypt
from crypto_commons.generic import long_to_bytes, bytes_to_long
from crypto_commons.netcat.netcat_commons import nc, receive_until_match, send
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


def recover_modulus(enc, dec, bitsize):
    for bit in range(bitsize - 1, -1, -1):
        payload = 2 ** bit
        e = enc(long_to_bytes(payload)).decode("hex")
        result = dec(e)
        if result == '00':
            start_bit = bit
            break
    print('start bit', start_bit)
    payload = 2 ** start_bit  # 100000...
    for bit in range(start_bit - 1, 7, -1):
        payload ^= 2 ** bit
        print(bin(payload))
        e = enc(long_to_bytes(payload)).decode("hex")
        result = dec(e)
        if result != '00':  # didn't work, set the bit back
            payload ^= 2 ** bit
    print('almost modulus', payload)
    too_large = payload ^ 0xff
    e = enc(long_to_bytes(too_large)).decode("hex")
    result = int(dec(e), 16)
    for i in range(256):
        potential_n = payload ^ i
        mod = too_large % potential_n
        if mod == result:
            return potential_n


def recover_flag(dec, flag, n, bitsize, known_suffix=''):
    f = ''
    divisor = modinv(2 ** 8, n)
    for last_byte in known_suffix[::-1]:  # strip known suffix
        sub = paillier_encrypt_simple(n - bytes_to_long(last_byte), n + 1, n)
        flag = flag * sub % (n * n)
        flag = pow(flag, divisor, n * n)

    for i in range(14):
        last_byte = dec(long_to_bytes(flag)).decode("hex")
        if last_byte == '':
            return f[::-1] + known_suffix
        f += last_byte
        print(f[::-1] + known_suffix)
        sub = paillier_encrypt_simple(n - bytes_to_long(last_byte), n + 1, n)
        flag = flag * sub % (n * n)
        flag = pow(flag, divisor, n * n)
    return f[::-1] + known_suffix


def main():
    bitsize = 1024
    url = "13.112.92.9"
    port = 21701
    s = nc(url, port)
    data = receive_until_match(s, "cmd:")
    flag = int(re.findall('Here is the flag!\s*(.*)\s*cmd:', data)[0], 16)
    print(flag)
    encryptor = lambda data: enc(s, data)
    decryptor = lambda data: dec(s, data)
    n = recover_modulus(encryptor, decryptor, bitsize)
    print('modulus', n)
    known_flag_suffix = "_paillier!!}\n"
    print(recover_flag(decryptor, flag, n, bitsize, known_flag_suffix))
    pass


main()


def sanity_recover_modulus():
    bitsize = 256
    p = getPrime(bitsize / 2)
    q = getPrime(bitsize / 2)
    n = p * q
    print(n)
    print(bin(n))

    def decryptor(p, q, data):
        data = bytes_to_long(data)
        decrypted = paillier_decrypt(data, [p, q], (p * q) + 1)
        to_bytes = long_to_bytes(decrypted)
        return to_bytes.encode("hex")[-2:]

    def encryptor(p, q, data):
        data = bytes_to_long(data)
        encrypted = paillier_encrypt_simple(data, (p * q) + 1, p * q)
        to_bytes = long_to_bytes(encrypted)
        return to_bytes.encode("hex")

    enc, dec = lambda data: encryptor(p, q, data), lambda data: decryptor(p, q, data)
    recovered = recover_modulus(enc, dec, bitsize)
    print(recovered)
    print(bin(recovered))


# sanity_recover_modulus()


def sanity_recover_flag():
    bitsize = 512
    p = getPrime(bitsize / 2)
    q = getPrime(bitsize / 2)
    n = p * q
    flag = paillier_encrypt_simple(bytes_to_long("hitcon{ala ma kota a sierotka ma rysia}"), n + 1, n)

    def decryptor(p, q, data):
        data = bytes_to_long(data)
        decrypted = paillier_decrypt(data, [p, q], p * q + 1)
        to_bytes = long_to_bytes(decrypted)
        return to_bytes.encode("hex")[-2:]

    print(recover_flag(lambda data: decryptor(p, q, data), flag, n, bitsize, "sierotka ma rysia}"))


# sanity_recover_flag()
