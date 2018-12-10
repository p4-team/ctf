import gmpy2

from Crypto.PublicKey import RSA

from crypto_commons.generic import bytes_to_long, long_to_bytes
from crypto_commons.rsa.rsa_commons import modinv


def solve(ct, e, n, padding_len):
    new_ct = ct * pow(modinv(256, n) ** padding_len, e, n)
    new_ct %= n
    for i in range(256):
        potential_pt, is_cube = gmpy2.iroot(new_ct + (n * i), e)
        if is_cube:
            print(i, long_to_bytes(potential_pt))


def main():
    flag_size = len(open("aes.enc", 'rb').read())
    key = RSA.importKey(open('pubkey.txt', 'rb').read())
    ct = open("rsa.enc", 'rb').read()
    solve(bytes_to_long(ct), key.e, key.n, 128 - flag_size)


main()
