s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz_{}"


def _l(idx, s):
    return s[idx:] + s[:idx]


def decrypt(ct, k1, k2):
    s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz_{}"
    t = [[_l((i + j) % len(s), s) for j in range(len(s))] for i in range(len(s))]
    i1 = 0
    i2 = 0
    decrypted = ""
    for a in ct:
        for c in s:
            if t[s.find(c)][s.find(k1[i1])][s.find(k2[i2])] == a:
                decrypted += c
                break
        i1 = (i1 + 1) % len(k1)
        i2 = (i2 + 1) % len(k2)
    return decrypted


def encrypt(p, k1, k2):
    t = [[_l((i + j) % len(s), s) for j in range(len(s))] for i in range(len(s))]
    i1 = 0
    i2 = 0
    c = ""
    for a in p:
        c += t[s.find(a)][s.find(k1[i1])][s.find(k2[i2])]
        i1 = (i1 + 1) % len(k1)
        i2 = (i2 + 1) % len(k2)
    return c


def recover_key(known_prefix, ciphertex):
    final_key = ['*'] * 14
    for pos in range(7):
        for c in s:
            partial_candidate_key = ['*'] * 14
            partial_candidate_key[pos] = c
            partial_candidate_key[13 - pos] = c
            key = "".join(partial_candidate_key)
            res = encrypt(known_prefix, key, key[::-1])
            if res[pos] == ciphertex[pos]:
                final_key[pos] = c
                final_key[13 - pos] = c
                print "".join(final_key)
    return "".join(final_key)


def main():
    ciphertext = "POR4dnyTLHBfwbxAAZhe}}ocZR3Cxcftw9"
    key = recover_key("SECCON{", ciphertext)
    flag = decrypt(ciphertext, key, key[::-1])
    print(flag)


main()
