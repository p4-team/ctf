# coding: utf-8
import hashlib
import string

class SymbolicXor:
    def __init__(self, ops, const=0):
        if isinstance(ops, str):
            ops = [ops]
        self.ops = sorted(ops)
        self.const = const

    def __xor__(self, other):
        if isinstance(other, int):
            return SymbolicXor(self.ops, self.const ^ other)
        elif isinstance(other, SymbolicXor):
            return SymbolicXor(self.setxor(self.ops, other.ops), self.const ^ other.const)

    __rxor__ = __xor__

    def setxor(self, a, b):
        out = list(a)
        for el in b:
            if el in out:
                out.remove(el)
            else:
                out.append(el)
        return out

    def __str__(self):
        if self.const == 0 and not self.ops:
            return '0'
        return '^'.join(str(c) for c in self.ops + ([self.const] if self.const else []))

    __repr__ = __str__

    def __eq__(self, oth):
        return self.ops == oth.ops and self.const == oth.const

def chunks(d, n):
    return [d[i*n:(i+1)*n] for i in range(len(d)/n)]

def xor(a, b):
    return ''.join(chr(ord(ac) ^ ord(bc)) for ac, bc in zip(a, b))

data0 = """
F1 64 72 4A 4F 48 4D BA  77 73 1D 34 F5 AF B8 0F
24 56 11 65 47 A3 2F 73  A4 56 4F 70 4A 13 57 9C
3F 6F 06 61 40 90 AF 39  10 29 34 C3 00 7A 40 3D
4E 3F 0E 2A 2F 20 7F 73  89 7D 4B 1D 09 AA D0 00
21 89 4D 2A 67 7C 18 3B  39 F2 8D 1C A7 71 57 2E
31 14 67 48 3C 7D AF 70  AE 10 31 68 D1 26 05 C8
25 F2 62 F5 5D 38 34 F2  20 0E 7E 9F FB 57 72 26
57 67 15 10 15 13 B9 3E  79 89 5D 24 12 01 98 7B
18 25 E0 DF 7C 24 1B 2D  44 B0 10 3D 57 3D 62 B4
21 1D 3E D1 10 D7 45 74  96 2B 6D 3B ED 10 00 67
31 DF 6C B8 86 1A 7C 6B  64 78 C6 37 76 E6 61 A0
AD BE 4C BA A7 0D
""".replace('\n', '').replace(' ', '').decode('hex')

data1 = """
08 4F FE AB 4E AA B4 03  4D 99 6E A1 48 D0 7D A2
E0 49 38 61 2D BC 5E 2C  5D 62 3F 89 C6 B8 5C 5A
4B 13 41 07 DF BF C2 29  07 64 14 25 32 00 73 69
2D 58 4B 76 15 29 2F A1  00 00 00 00 00 00 00 00
""".replace('\n', '').replace(' ', '').decode('hex')


def encrypt_chunks(data, passw, k, sd, s0, st):
    """
    encrypt chunks with size k
    start with [s0 bytes from front] [k-s0 bytes from back]
    start with s=s0
    after every round add sd to s
    when s == st, change s to s0 again
    """
    buff = [0] * 16
    split = s0
    of = 0
    ob = len(data)
    for i in range(len(data) / k):
        for j in range(split):
            buff[j + k - split] = data[j + of]
        for j in range(k - split):
            buff[j] = data[split + ob - k + j]
        for j in range(k):
            buff[j] ^= passw[j]
        for j in range(split):
            data[j + of] = buff[j]
        for j in range(k - split):
            data[split + ob - k + j] = buff[j + split]
        of += split
        ob -= k - split
        if split == st:
            split = s0
        else:
            split += sd

def decrypt_chunks(data, passw, k, sd, s0, st):
    """
    encrypt chunks with size k
    start with [s0 bytes from front] [k-s0 bytes from back]
    start with s=s0
    after every round add sd to s
    when s == st, change s to s0 again
    """
    buff = [0] * 16
    split = s0
    of = 0
    ob = len(data)
    for i in range(len(data) / k):
        for j in range(split):
            buff[j] = data[j + of]
        for j in range(k - split):
            buff[j + split] = data[split + ob - k + j]
        for j in range(k):
            buff[j] ^= passw[j]
        for j in range(split):
            data[j + of] = buff[j + k - split]
        for j in range(k - split):
            data[split + ob - k + j] = buff[j]
        of += split
        ob -= k - split
        if split == st:
            split = s0
        else:
            split += sd


def decrypt(data, passw):
    pass1 = [passw[2*i+1] for i in range(5)]

    decrypt_chunks(data, passw, 7, 2, 3, 7)
    decrypt_chunks(data, pass1, 5, -1, 5, 1)
    decrypt_chunks(data, passw, 10, 1, 4, 8)
    decrypt_chunks(data, passw, 10, 1, 4, 8)


def encrypt(data, passw):
    pass1 = [passw[2*i+1] for i in range(5)]

    encrypt_chunks(data, passw, 10, 1, 4, 8)
    encrypt_chunks(data, passw, 10, 1, 4, 8)
    encrypt_chunks(data, pass1, 5, -1, 5, 1)
    encrypt_chunks(data, passw, 7, 2, 3, 7)

def make_sympad(syms):
    passw = [SymbolicXor('v'+str(i)) for i in range(16)]
    pad = map(ord, '\0' * syms)
    decrypt(pad, passw)
    return pad

def permute(data):
    perm = map(ord, data)
    decrypt(perm, [0]*16)
    return ''.join(map(chr, perm))

def transform(data, maps):
    maps = expand_maps(maps)

    # pad - zaszyfrowane i spermutowane zera - czyli sam "one time pad" wygenerowany z hasła
    pad = make_sympad(len(data))

    # perm - permutacja zaszyfrowanych danych tak, żeby były w oryginalnej kolejnosci
    perm = permute(data)

    #for i in range(len(data)):
    #    a = pad[i]
    #    print perm[i].encode('hex'), a

    out = ''
    for i in range(len(data)):
        a = pad[i]
        #print perm[i].encode('hex'),
        for con, sym in maps:
            if sym == a:
                #print chr(ord(perm[i]) ^ con).encode('hex'), a
                #print chr(ord(perm[i]) ^ con), a
                c = chr(ord(perm[i]) ^ con)
                if c not in string.printable:
                    return None
                out += c
                break
        else:
            #print '?', a
            out += '?'
    return out

def expand_maps(maps):
    while True:
        maps2 = list(maps)
        changed = False
        for iv0, sym0 in maps:
            for iv1, sym1 in maps:
                m2 = iv0^iv1, sym0^sym1
                if m2 not in maps2:
                    maps2.append(m2)
                    changed = True
        if not changed:
            syms = set()
            for c, s in maps2:
                syms.add(str(s))
            if len(syms) != len(maps2):
                raise RuntimeError('Unconsistent maps')
            return maps2
        maps = maps2

passw = map(ord, 'satan loves you and your children and your cat')
encrypt(passw, range(16))
data_test = ''.join(chr(c) for c in passw)

#maps = [
#    (0, SymbolicXor([])),
#    (7, SymbolicXor(['v2', 'v5'])),
#    (1, SymbolicXor(['v2', 'v3'])),
#]
#transform(passw, maps)
#exit(0)

#maps0 = [
#    (0, SymbolicXor([])),
#    ((0x55 ^ 0x0d), SymbolicXor(['v5', 'v2'])),  # push rbp
#    ((0x48 ^ 0x48), SymbolicXor(['v2', 'v3'])),  # mov rbp, rsp
#    ((0x89 ^ 0xf5), SymbolicXor(['v1', 'v8'])),  
#    ((0xe5 ^ 0xaf), SymbolicXor(['v3', 'v9'])),
#    ((0x48 ^ 0x4d), SymbolicXor(['v0', 'v3', 'v5', 'v9'])),  # lea rdi [stuff]
#    ((0x8d ^ 0xad), SymbolicXor(['v1', 'v3', 'v5', 'v6'])),  
#    ((0x3d ^ 0xbe), SymbolicXor(['v2', 'v5', 'v6', 'v7'])),  
#]
#transform(data0, maps)
#exit(0)

def known_plaintext(data, what):
    syms = make_sympad(len(data))
    perm = permute(data)

    for i in range(len(data) - len(what)):
        try:
            maps = [
                (0, SymbolicXor([])),    
            ]
            for j in range(len(what)):
                maps.append( (ord(what[j]) ^ ord(perm[i+j]), syms[i+j]) )

            t = transform(data, maps)
            print i, 'ok', t
        except RuntimeError:
            print i, 'inconsistent'

def known_plaintext2(data, what, what1):
    syms = make_sympad(len(data))
    perm = permute(data)

    for i in range(len(data) - len(what)):
        maps = [
            (0, SymbolicXor([])),    
        ]
        for j in range(len(what)):
            maps.append( (ord(what[j]) ^ ord(perm[i+j]), syms[i+j]) )

        maps0 = list(maps)
        for i2 in range(i+len(what), len(data) - len(what1)):
            try:
                maps = list(maps0)
                for j in range(len(what1)):
                    maps.append((ord(what1[j]) ^ ord(perm[i2+j]), syms[i2+j]))

                t = transform(data, maps)
                print i, i2, 'ok', t
            except RuntimeError:
                print i, 'inconsistent'

#known_plaintext(data_test, 'satan lov')
#known_plaintext2(data_test, 'satan', 'lov')
#exit(0)
#known_plaintext(data1, 'FLAG{')
known_plaintext2(data1, 'FLAG{', 'cat')
exit(0)

transform(data1, [
    (0, SymbolicXor([])),    
    #(ord('F') ^ 0x00, SymbolicXor(['v2', 'v5'])),
    #(ord('L') ^ 0xAA, SymbolicXor(['v2', 'v3'])),
    #(ord('A') ^ 0x48, SymbolicXor(['v1', 'v8'])),
    #(ord('G') ^ 0xd0, SymbolicXor(['v3', 'v9'])),
])
