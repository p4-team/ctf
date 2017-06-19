import numpy as np
import math, string

def calc(p):
    r=ord(p)*math.pi/180
    c=math.cos(r)
    s=math.sin(r)
    m = np.matrix([[c,-s,0], [s,c,0], [0,0,1]])
    pt = np.matrix([1024,0,0]).T
    res=m*pt
    res+=np.matrix([2048,2048,0]).T
    return res

def extend(e):
    r=e^0x5f208c26
    for i in range(15, 32, 3):
        f=e<<i
        r^=f
    return r

def hash_alpha(p):
    res=calc(p)
    return extend(int(res[0]))

def hash_beta(p):
    res=calc(p)
    return extend(int(res[1]))

def main(idx, pw, unkbyte):
    if idx&1 == 0:
        final = hash_alpha(pw[idx/2])
    else:
        final = hash_beta(pw[idx/2])
    for i in range(0, 32, 6):
        final^=idx<<i
        final&=0xffffFFFF
    h=0x5a
    if 0:
        for i in range(32):
            p=pw[i]
            r=(i*3)&7
            p=(p<<r)|(p>>(8-r))
            p=p&0xff
            h^=p
    h^=unkbyte
    final^=h
    final^=h<<8
    final^=h<<16
    final^=h<<24
    return final

data="30c7ead97107775969be4ba00cf5578f1048ab1375113631dbb6871dbe35162b1c62e982eb6a7512f3274743fb2e55c818912779ef7a34169a838666ff3994bb4d3c6e14ba2d732f14414f2c1cb5d3844935aebbbe3fb206343a004e18a092daba02e3c0969871548ed2c372eb68d1af41152cb3b61f300e3c1a8246108010d282e16df8ae7bff6cb6314d4ad38b5f9779ef23208efe3e1b699700429eae1fa93c036e5dcbe87d32be1ecfac2452ddfdc704a00ea24fbc2161b7824a968e9da1db756712be3e7b3d3420c8f33c37dba42072a941d799ba2eebbf86191cb59aa49a80ebe0b61a79741888cb62341259f62848aad44df2b809383e09437928980f"
dwords=[]
for i in range(len(data)/8):
    dwords.append(int(data[i*8:i*8+8], 16))

if 0:
    unkbyte=-1
    for i in range(256):
        for j in range(256):
            m=main(0, chr(i), j)
            if m == dwords[0]:
                unkbyte=j
unkbyte=53

s = ""
candidates = []
for i in range(len(dwords)/2):
    candidates.append([])
    for c in range(256):
        ss = " " * i + chr(c)
        m = main(i*2, ss, unkbyte)
        m2 = main(i*2+1, ss, unkbyte)
        if m == dwords[i*2]:
            print "a", i, chr(c)
            if chr(c) in string.printable:
                s+=chr(c)
        #if m2 == dwords[i*2+1]:
        #    print "b", i, chr(c)
print repr(s)
