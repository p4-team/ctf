def mult(a, b):
    rows_a = len(a)
    cols_a = len(a[0])
    rows_b = len(b)
    cols_b = len(b[0])

    if cols_a != rows_b:
        print "cannot multiply the two matrices. Incorrect dimensions:", cols_a, rows_b
        return

    c = [[0 for row in range(cols_b)] for col in range(rows_a)]

    for i in range(rows_a):
        for j in range(cols_b):
            c[i][j] = sum(a[i][k] * b[k][j] for k in range(cols_a)) & 1
    return c


def transpose(mat):
    return [[mat[y][x] for y in range(len(mat))] for x in range(len(mat[0]))]

assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]


def make_matrix(w, h, data):
    return [[data[i*w+j] for j in range(w)] for i in range(h)]

assert make_matrix(2, 3, [1, 2, 3, 4, 5, 6]) == [[1, 2], [3, 4], [5, 6]]


def unmake_matrix(w, h, data):
    return [data[i/w][i%w] for i in range(w*h)]

assert unmake_matrix(2, 3, [[1, 2], [3, 4], [5, 6]]) == [1, 2, 3, 4, 5, 6]


def chunks(data, n, pad_obj=0):
    pad = list(data) + [pad_obj] * (n-1)
    return [pad[i*n:(i+1)*n] for i in range(len(pad)/n)]

assert chunks([1, 2, 3, 4, 5], 3) == [[1, 2, 3], [4, 5, 0]]


def helical_interleave_part(w, h, dat):
    mat = make_matrix(w, h, dat)
    conv = [[mat[(y+x) % h][x] for x in range(w)] for y in range(h)]
    return unmake_matrix(w, h, conv)

assert helical_interleave_part(2, 3, [1, 2, 3, 4, 5, 6]) == [1, 4, 3, 6, 5, 2]


def helical_interleave(w, h, dat):
    return sum((helical_interleave_part(w, h, part) for part in chunks(dat, w*h)), [])

assert helical_interleave(2, 3, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]) == [1, 4, 3, 6, 5, 2, 7, 10, 9, 12, 11, 8]


def helical_deinterleave_part(w, h, dat):
    mat = make_matrix(w, h, dat)
    conv = [[mat[(y-x) % h][x] for x in range(w)] for y in range(h)]
    return unmake_matrix(w, h, conv)

assert helical_deinterleave_part(2, 3, [1, 4, 3, 6, 5, 2]) == [1, 2, 3, 4, 5, 6]


def helical_deinterleave(w, h, dat):
    return sum((helical_deinterleave_part(w, h, part) for part in chunks(dat, w*h)), [])


def encode_helix(g, data):
    h, w = len(g), len(g[0])
    return transpose(sum((transpose(mult([chunk], g)) for chunk in chunks(data, h)), []))[0]


def decode_helix(g, data):
    h, w = len(g), len(g[0])
    return sum((chunk[:h] for chunk in chunks(data, w)), [])


def get_wrong_bit(h, dec):
    for i, row in enumerate(transpose(h)):
        if row == dec:
            return i

def decode_helix_ec(g_mat, h_mat, data):
    h, w = len(g_mat), len(g_mat[0])
    result = []
    for chunk in chunks(data, w):
        dec = transpose(mult(h_mat, transpose([chunk])))[0]
        if not all(b == 0 for b in dec):
            bit = get_wrong_bit(h_mat, dec)
            chunk[bit] = 1 - chunk[bit]
        result += chunk[:h]
    return result

def decode_helix_or_die_trying(g_mat, h_mat, data):
    h, w = len(g_mat), len(g_mat[0])
    result = []
    for chunk in chunks(data, w):
        dec = transpose(mult(h_mat, transpose([chunk])))[0]
        if not all(b == 0 for b in dec):
            chunk = [0] * h
        result += chunk[:h]
    return result

def decode_helix_brute(g_mat, h_mat, data):
    h, w = len(g_mat), len(g_mat[0])
    result = []
    for chunk in chunks(data, w):
        dec = transpose(mult(h_mat, transpose([chunk])))[0]
        if not all(b == 0 for b in dec):
            chunk = [0] * h
        result += chunk[-h:]
    return result


#        dec = transpose(mult(h, transpose(cod)))
#        assert all(d == 0 for d in dec[0])
#        for i in range(3):
#            dec[0][i] = 1 - dec[0][i]
#            assert not all(d == 0 for d in dec[0])
#            dec[0][i] = 1 - dec[0][i]
g = [
    [1 ,0 ,0 ,0 ,1 ,1 ,1],
    [0 ,1 ,0 ,0 ,0 ,1 ,1],
    [0 ,0 ,1 ,0 ,1 ,0 ,1],
    [0 ,0 ,0 ,1 ,1 ,1 ,0],
]

h = [
    [1, 0, 1, 1, 1, 0, 0],
    [1, 1, 0, 1, 0, 1, 0],
    [1, 1, 1, 0, 0, 0, 1],
]

raw = [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
enc = encode_helix(g, raw)
assert decode_helix(g, enc) == raw

enc2 = list(enc)
enc2[2] = 1 - enc2[2]
assert decode_helix_ec(g, h, enc2) == raw
assert raw == decode_helix(g, encode_helix(g, raw))
#print h

dat = [[1, 0, 1, 1]]
#print dat
cod = mult(dat, g)
#print cod
cod[0][1] = 1
dec = transpose(mult(h, transpose(cod)))
#print dec
#print get_wrong_bit(h, dec)

def validate_helix(g, h):
    N = 1000
    import random
    for i in range(N):
        dat = [[random.randint(0, 1) for i in range(len(g))]]
        cod = mult(dat, g)
        dec = transpose(mult(h, transpose(cod)))
        assert all(d == 0 for d in dec[0])
        for i in range(3):
            dec[0][i] = 1 - dec[0][i]
            assert not all(d == 0 for d in dec[0])
            dec[0][i] = 1 - dec[0][i]

validate_helix(g, h)

mat_g = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0], 
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0], 
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], 
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0], 
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1], 
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], 
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1], 
]

mat_h = [
    [1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0],
    [1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
]

validate_helix(mat_g, mat_h)

data = open('data.txt').read().strip()
data = [int(c) for c in data]

result = []

for w in range(1, 30):
    print w, ':',
    for h in range(1, 30):
        print h,
        fail = 0

        helix = helical_deinterleave(w, h, data)
        cs = chunks(helix, 31)
        for c in cs:
            hamming_check = mult(mat_h, transpose([c]))
            hamming_check = transpose(hamming_check)
            if not all(n == 0 for n in hamming_check[0]):
                fail += 1
        
        result.append((fail, w, h))
    print

def safe(s):
    return ''.join(c if 32 <= ord(c) <= 127 else '.' for c in s)

result = sorted(result)

fail, w, h = result[0]

print 'fail', fail, 'w', w, 'h', h


#for i in range(len(cs)):
#    c = cs[i]
#    hamming_check = mult(mat_h, transpose([c]))
#    hamming_check = transpose(hamming_check)
#    if not all(n == 0 for n in hamming_check[0]):
#        for j in range(len(c)):
#            helix[i*len(c)+j] = 1

helix = helical_deinterleave(w, h, data)
helix = decode_helix_brute(mat_g, mat_h, helix)
dat = chunks(helix, 8)
decr = [int(''.join(str(c) for c in chunk), 2) for chunk in dat]
decr_hex = ''.join(chr(c) for c in decr).encode('hex')
decr_bin = bin(int(decr_hex, 16))[2:]
#print decr_bin

for i in range(8):
    data = repr(''.join([chr(int(''.join(chunk), 2)) for chunk in chunks(decr_bin[i:], 8, '0')]))
    if 'SharifCTF' in data:
        print data

#print safe(''.join(chr(c) for c in decr))
#print helix

