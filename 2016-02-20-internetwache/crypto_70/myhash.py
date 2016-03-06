#!/usr/bin/python2
import binascii
import textwrap

def tb(s): # to binary
	return bin(int(binascii.hexlify(s),32/2)).lstrip("0b")

def te(s): # pad to 128 bits
	p = 2 << 6
	return s + "0" * (p-len(s)%p)

def tk(s): # split into 64 bit blocks
	return textwrap.wrap(s, 2<<5) #64

def tj(s): # split into 16 bit blocks
	return textwrap.wrap(s, 2<<3) #16

def ti(l):
	return int(l,2)

def tr(x,y): # hash
	return (x<< y) or (x >> (16-y));

def th(x):
	return "{0:#0{1}x}".format(x,8)

def tp(x,y):
	s = th(x) + th(y)
	s = s.replace("0x","")
	return s

def myhash(text):

	b = tb(text)

	p = te(b)

	bl = tk(p)

	t11 = 3
	q2 = 5

	tu = [ y**2 for y in range(2<<4>>1)] # Squares up to 225
	to = [2, 7, 8, 2, 5, 3, 7, 8, 9, 4, 11, 13, 5, 8, 14, 15]
	for i in bl:
		t1 = t11
		t2 = q2

		tl = tj(i)
		tq = map(ti, tl)

		for j in range(16):
			if(j >= 12 ):
				tz = (tq[0] & tq[1]) | ~tq[2] 
			elif(j >= 8):
				tz = (tq[3] | tq[2])
			elif(j >= 4):
				tz = (~tq[2] & tq[0]) & (tq[1] | ~tq[0])
			elif(j >= 0):
				tz = (tq[0] | ~tq[2]) | tq[1]
			else:
				pass

			t1 = t1 + tr(tz + tu[j] + tq[j%(16>>2)],to[j])
			t2 = t1 + tr(t2,to[j]) %t1

		t11 += t1
		q2 += t2

	t11 = t11 % 0xFF # Should be 0xFFFFFFFF, right?
	q2 = q2 % 0xFF # Same here... 0xFFFFFFFF

	return tp(t11,q2)
# t11=68
# q2=7d


i=1000000000000000000
while True:
    s=myhash(str(i))
    if i%10000==0:
        print i,s
    if s=="00006800007d":
        print i
        break
    i+=1
