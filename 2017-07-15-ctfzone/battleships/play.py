from rc4 import RC4
from pwn import *
import sys, hashlib, string

def find(a, b):
    alph = string.letters+string.digits
    for x1 in alph:
        for x2 in alph:
            for x3 in alph:
                for x4 in alph:
                    s=a+x1+x2+x3+x4
                    sh=hashlib.sha256(s).hexdigest()
                    if sh == b:
                        return s

key="g\306isQ\377J\354)\315\272\253\362\373\343F|\302T\370\33\350\347\215vZ.c3\237\311\232f2\r\2671X\243Z%]\5\27X\351^\324\253\262\315\306\233\264T\21\16\202tA!=\334\207p\351>\241A\341\374g>\1~\227\352\334k\226\2178\\*\354\260;\3732\257<T\354\30\333\\\2\32\376C\373\372\252:\373)\321\346\5<|\224u\330\276a\211\371\\\273\250\231\17\225\261\353\361\263\5\357\367\0\351\241:\345\312\v\313\320HGd\275\37#\36\250\34{d\305\24sZ\305^Kyc;pd$\21\236\t\334\252\324\254\362\33\20\257;3\315\343PHG\25\\\273o\"\31\272\233}\365\v\341\32\34\177#\370)\370\244\33\23\265\312N\350\23028\340yM=4\274_Nw\372\313l\5\254\206!+\252\32U\242\276p\265s;\4\\\3236\224\263\257\342\360\344\236O2\25I\375\202N\251"

rem = remote("82.202.212.28", 1337)
a = rem.recvline()
a = a.split("'")[1].split("*")[0]
b = rem.recvline().split("= ")[1].strip()
c = find(a, b)
rem.send(c)
rem.recvuntil("OK")
rem.send("CLIENT_HELLO\0"+key)

key=[ord(c) for c in key]
r = RC4(key)

def cry(a):
    s = ""
    for c,d in zip(a, r):
        s+=chr(ord(c) ^ d)
    return s

print cry(rem.recv())
rem.send(cry("PvQvRvSvTvUvVvWvXvYv"))
print cry(rem.recv())

shot = {}
k=0
hit=0
mis=0
X=14
Y=7
while True:
    times=0
    while True:
        x = random.randint(0, X-1)
        y = random.randint(0, Y-1)
        if (x,y) not in shot:
            break
        else:
            times+=1
            if times>10000 and shot[(x,y)] == 'v':
                break

    rem.send(cry("SHOOT" + chr(x*16+y)))
    q = cry(rem.recv())
    print q
    if "WIN" in q:
        open("/tmp/loggg", "a").write("hurra %s %d/%d\n" %(q,hit,hit+mis))
        rem.interactive()
    elif "MIS" in q:
        shot[(x,y)] = "."
        mis+=1
    else:
        def do(a,b,c='o'):
            global mis
            if a>=0 and a<=X and b>=0 and b<=Y:
                if (a,b) not in shot:
                    shot[(a,b)] = c
                    mis+=1
        do(x-1, y)
        do(x+1, y)
        do(x, y-1)
        do(x, y+1)
        if 0:
            do(x-1, y-1, 'v')
            do(x+1, y+1, 'v')
            do(x+1, y-1, 'v')
            do(x-1, y+1, 'v')
        shot[(x,y)] = "x"
        hit+=1
    rem.send(cry("NEXT"))
    x=cry(rem.recv())
    print x
    if "LOS" in x:
        open("/tmp/loggg", "a").write("%d/%d\n" %(hit,hit+mis))
        break
    print len(shot)
    for i in range(X):
        for j in range(Y):
            if (i,j) not in shot:
                print " ",
            else:
                print shot[(i,j)],
        print
                




