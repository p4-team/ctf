# Notice that the action of randgen on the state is linear in GF(2).
# We will thus represent the state as a 4096-dimensional vector in GF(2).
# Calculating the jump is then a simple matrix exponentiation.

# To obtain the matrix, we perform symbolic execution of randgen(), where
# each bit is represented as a vector of coefficients.

# This unoptimised code takes a couple of seconds per byte of plaintext,
# which is perfectly acceptable.

# NOTE: The team member who originally solved this talked something about
# a dumb overnight bruteforce in PyPy. Unfortunately he couldn't be reached
# while we had to write the writeup, so I resolved the challenge, probably
# the more intended way.
s = []
p = 0

def init():
    global s,p
    s = [i for i in range(0,64)]
    p = 0
    return

def randgen():
    global s,p
    a = 3
    b = 13
    c = 37
    s0 = s[p]
    p = (p + 1) & 63
    s1 = s[p]
    res = (s0 + s1) & ((1<<64)-1)
    s1 ^^= (s1 << a) & ((1<<64)-1)
    s[p] = (s1 ^^ s0 ^^ (s1 >> b) ^^ (s0 >> c))    & ((1<<64)-1)
    return res


K = GF(2)
def shl(b, n):
    return b[n:] + (vector((K(0),)*128),) * n
def shr(b, n):
    return (vector((K(0),)*128),) * n + b[:-n]
def xor(a, b):
    return tuple(a + b for a, b in zip(a, b))

def bit(k):
    return vector(K(1) if k == i else K(0) for i in range(128))

def getmat():
    # [[MSB, ... LSB]]
    s0 = tuple(bit(i) for i in range(0, 64))
    s1 = tuple(bit(i) for i in range(64, 128))
    a = 3
    b = 13
    c = 37
    s1 = xor(s1, shl(s1, a))
    out = xor(xor(s1, s0), xor(shr(s1, b), shr(s0, c)))

    M = Matrix(K, [tuple(o) + (0,) * 64*62 for o in out])
    print('crunching matrix')
    rows = identity_matrix(K, 4096).rows()
    rows[64:128] = M.rows()
    rows = rows[64:] + rows[:64]
    return Matrix(rows)


M = getmat()
print('done')

def bits(v):
    return [K(v>>(63-i)) for i in range(64)]
def unbits(v):
    return sum(ZZ(k) << (63 - i) for i, k in enumerate(v))

def jump(to):
    global s, p
    s = s[p:] + s[:p]

    b = []
    for k in s:
        b += bits(k)

    b = M^to * vector(b)
    s = [unbits(b[k:k+64]) for k in range(0, len(b), 64)]
    s = s[-p:] + s[:-p]

def check_jump():
    init()
    jump(10000)
    assert randgen() == 7239098760540678124
    print('assert ok')

    init()
    jump(100000)
    assert randgen() == 17366362210940280642
    print('assert ok')

    init()
    jump(1000000)
    assert randgen() == 13353821705405689004
    print('assert ok')

    init()
    jump(10000000)
    assert randgen() == 1441702120537313559
    print('assert ok')

    init()
    for a in range(31337):randgen()
    for a in range(1234567):randgen()
    buf = randgen()
    for a in range(7890123):randgen()
    buf2 = randgen()
    init()
    jump(31337+1234567)
    print (buf == randgen())
    jump(7890123)
    print (buf2 == randgen())

check_jump()

init()
for a in range(31337):randgen()

flag = open("public/enc.dat", 'rb').read()
assert len(flag) == 256

enc = b""

for x in range(len(flag)):
    buf = randgen()
    sh = x//2
    if sh > 64:sh = 64
    mask = (1 << sh) - 1
    buf &= mask
    jump(buf)
    enc += bytes([ flag[x] ^^ (randgen() & 0xff) ])
    print ("%r" % enc)

#open("enc.dat","wb").write(bytearray(enc))

