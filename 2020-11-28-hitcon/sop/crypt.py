import struct

# 05352: r6 = INPUT1
# 05464: r7 = INPUT2
# 05576: r8 = 0
# 32 times do:
# 	05624: r8 += C9
# 	06136: r6 += (r7 + r8) ^ ((r7 >> 5) + C3) ^ ((r7 << 4) + C2)
#	06648: r7 += (r6 + r8) ^ ((r6 >> 5) + C5) ^ ((r6 << 4) + C4)

def encrypt(r6, r7, C2, C3, C4, C5, C9):
    r8 = 0
    for i in range(32):
        r8 += C9
        r6 += (r7 + r8) ^ ((r7 >> 5) + C3) ^ ((r7 << 4) + C2)
        r6 &= 0xffffFFFF
        r7 += (r6 + r8) ^ ((r6 >> 5) + C5) ^ ((r6 << 4) + C4)
        r7 &= 0xffffFFFF
    return r6, r7


def decrypt(r6, r7, C2, C3, C4, C5, C9):
    r8 = C9 * 32
    for i in range(32):
        r7 -= (r6 + r8) ^ ((r6 >> 5) + C5) ^ ((r6 << 4) + C4)
        r7 += 2**32
        r7 &= 0xffffFFFF
        r6 -= (r7 + r8) ^ ((r7 >> 5) + C3) ^ ((r7 << 4) + C2)
        r6 += 2**32
        r6 &= 0xffffFFFF
        r8 -= C9
        r8 += 2**32
        r8 &= 0xffffFFFF
    return r6, r7


C2, C3, C4, C5, C9 = 123,345,567,876,432
r6,r7 = 4836596,373759

x,y = encrypt(r6,r7,C2,C3,C4,C5,C9)
a,b = decrypt(x, y, C2,C3,C4,C5,C9)
print(r6,r7)
print(a,b)

expected = [0x152ceed2,0xd6046dc3,0x4a9d3ffd,0xbb541082,0x632a4f78,0xa9cb93d,0x58aae351,0x92012a14]

keys = [
0x69a33fff,
0x468932dc,
0x2b0b575b,
0x1e8b51cc,
0x51fdd41a,

0x32e57ab6,
0x7785df55,
0x688620f9,
0x8df954f3,
0x5c37a6db,

0xaca81571,
0x2c19574f,
0x1bd1fc38,
0x14220605,
0xb4f0b4fb,

0x33f33fe0,
0xf9de7e36,
0xe9ab109d,
0x8d4f04b2,
0xd3c45f8c]

b = b""
for i in range(4):
    r6,r7 = expected[i*2:i*2+2]
    c2,c3,c4,c5,c9 = keys[i*5:i*5+5]
    x,y = decrypt(r6,r7,c2,c3,c4,c5,c9)
    b += struct.pack("<I", x)
    b += struct.pack("<I", y)

print(b)
