import gmpy2
import re

from Crypto.Cipher import AES

from MTRecover import MT19937Recover
from crypto_commons.generic import factor, long_to_bytes, chunk, bytes_to_long
from crypto_commons.netcat.netcat_commons import nc, receive_until_match, send
from crypto_commons.oracle.lsb_oracle import lsb_oracle_from_bits


def unpad(s):
    n = ord(s[-1])
    return s[:-n]


def aes_decrypt(s, aeskey):
    iv = s[:16]
    aes = AES.new(aeskey, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(s[16:]))


def lsb_oracle(encrypted_data, multiplicator, upper_bound, oracle_fun):
    def bits_provider():
        ciphertext = encrypted_data
        for i in range(895):  # 1024 - 128 = 896
            ciphertext = multiplicator(ciphertext)
            yield 0
        while True:
            ciphertext = multiplicator(ciphertext)
            yield oracle_fun(ciphertext)

    return lsb_oracle_from_bits(upper_bound, bits_provider())


def oracle(s, ct):
    send(s, '2')
    print(receive_until_match(s, 'input hexencoded cipher text: '))
    payload = long_to_bytes(ct).encode("hex")
    print("Sending payload", payload)
    send(s, payload)
    r = receive_until_match(s, 'RSA: .*\n')
    receive_until_match(s, '4: get encrypted key\n')
    bit = int(re.findall('RSA: (.*)\n', r)[0], 16) & 1
    return bit


def recover_aes_key(n, s):
    send(s, '4')
    r = receive_until_match(s, "here is encrypted key :\)\n.+\n")
    encrypted_aes_key = re.findall("here is encrypted key :\)\n(.*)\n", r)[0]
    print('aes key', encrypted_aes_key)
    decrypted_aes_key = lsb_oracle(int(encrypted_aes_key, 16), lambda ct: ct * pow(2, 65537, n) % n, n, lambda ct: oracle(s, ct))
    decrypted_aes_key = long_to_bytes(int(decrypted_aes_key))
    return decrypted_aes_key


def recover_n(s):
    send(s, '1')
    print(receive_until_match(s, "input plain text: "))
    send(s, '\2')
    r = receive_until_match(s, "4: get encrypted key\n")
    print(r)
    pow2e = int(re.findall('RSA: (.*)\n', r)[0], 16)
    send(s, '1')
    print(receive_until_match(s, "input plain text: "))
    send(s, '\3')
    r = receive_until_match(s, "4: get encrypted key\n")
    print(r)
    pow3e = int(re.findall('RSA: (.*)\n', r)[0], 16)
    n = gmpy2.gcd(2 ** 65537 - pow2e, 3 ** 65537 - pow3e)
    n = factor(n)[1]
    assert pow(2, 65537, n) == pow2e
    return n


def get_iv(s):
    send(s, '1')
    print(receive_until_match(s, "input plain text: "))
    send(s, 'A')
    r = receive_until_match(s, "4: get encrypted key\n")
    print(r)
    aes_iv = re.findall('AES: (.*)\n', r)[0][:32].decode("hex")
    return aes_iv


def collect_outputs(s):
    out = []
    for i in range(160):
        aes_iv = get_iv(s)
        out.extend(map(bytes_to_long, chunk(aes_iv, 4))[::-1])
    return out


def recover_next_iv(s):
    outputs = collect_outputs(s)
    mtr = MT19937Recover()
    r2 = mtr.go(outputs)
    iv = long_to_bytes(r2.getrandbits(16 * 8))
    sanity = get_iv(s)
    assert sanity == iv
    return long_to_bytes(r2.getrandbits(16 * 8)).encode("hex")


def main():
    url = "crypto.chal.ctf.westerns.tokyo"
    port = 5643
    s = nc(url, port)
    print(receive_until_match(s, "4: get encrypted key"))

    n = recover_n(s)
    print('n', n)

    decrypted_aes_key = recover_aes_key(n, s)
    print('aes key', decrypted_aes_key.encode("hex"))

    next_iv_hex = recover_next_iv(s)
    print('next iv', next_iv_hex)

    send(s, '3')
    r = receive_until_match(s, "4: get encrypted key\n")
    flag_ct = re.findall("another bulldozer is coming!\n(.*)\n", r)[0][32:]

    print('encrypted flag', next_iv_hex + flag_ct)

    print(aes_decrypt((next_iv_hex + flag_ct).decode("hex"), decrypted_aes_key))
    s.close()


main()
