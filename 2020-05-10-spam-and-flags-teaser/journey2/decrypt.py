binary = open('admin-tool', 'rb').read()
stream = open('stream.bin', 'rb').read()

def KSA(key):
    keylength = len(key)

    S = list(range(256))

    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % keylength]) % 256
        S[i], S[j] = S[j], S[i]  # swap

    return S


def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]  # swap

        K = S[(S[j] - S[i]) % 256]
        yield K


def RC4(key):
    S = KSA(key)
    return PRGA(S)

key = binary[0x2080:]
keylen = key.index(b'\x00')
key = key[:keylen]

cipher = binary[0x20c0:]
cipher = cipher[:0x70]

out = bytearray()
for b,k,s in zip(cipher, RC4(key), stream):
    assert s^65 == k or s == b'\x00'
    out.append(b^k)
print(out)
