from tab import tab


def doit(n, ops):
    for op, arg in ops:
        if op == 0:
            n += arg
        elif op == 1:
            n = (n << arg) | (n >> (8 - arg))
        elif op == 2:
            n ^= arg
        else:
            assert False
        n &= 0xff
    return n


def inv_one(op):
    o, a = op
    if o == 0:
        return (0, (256 - a) % 256)
    if o == 1:
        return (1, (8 - a) % 8)
    if o == 2:
        return op


def inv(ops):
    return [inv_one(op) for op in ops[::-1]]


SWAP = [(0, 254), (1, 7), (0, 1), (1, 1)]
def get_swappy_sequence(a, b):
    if a == b:
        return []
    if a > b:
        a, b = b, a

    return tab[(a, b)] + SWAP + inv(tab[(a, b)])


def get_perm_sequence(perm):
    seq = []
    perm = perm[:]
    for i in range(256):
        j = perm.index(i)
        seq += get_swappy_sequence(i, j)
        perm[i], perm[j] =  perm[j], perm[i]
    return seq

pt = 'GoodCipher'

from pwn import *
import itertools

charset = string.letters + string.digits

def connect(h, p):
    r = remote(h, p)
    l = r.readline()
    suf = l.split("+")[1].split(")")[0]
    exp = l.split("==")[1].strip()
    for c in itertools.product(charset, repeat = 4):
        s = "".join(c)
        if s[1:] == 'aaa':
            print s
        if hashlib.sha256(s + suf).hexdigest() == exp:
            r.sendline(s)
            break
    return r

r = connect("47.75.4.252", 10001)
for i in range(3):
    r.recvuntil("ciphertext is ")
    ct = r.recvline().strip().decode("hex")
    print ct.encode("hex")


    perm = range(256)
    for p, c in zip(pt, ct):
        p, c = ord(p), ord(c)
        j = perm.index(c)
        print p, c, j
        perm[p], perm[j] = c, perm[p]

    seq = get_perm_sequence(perm)
    for s in seq:
        r.send(str(s[0]) + " " + str(s[1]))
        print s, r.recvline().strip()
    r.send("\n")

r.interactive()
