import hashlib, binascii, struct, time

def le(num):
    num=hex(num)[2:].strip("L")
    while len(num)<8:
        num="0"+num
    return int("".join([num[i*2:i*2+2] for i in range(4)][::-1]),16)

def check(sm):
    sm^=0x1f9933d
    sm^=0xc7fffffa
    #print hex(sm)
    ll=le(sm)
    #print hex(ll)
    ll=hex(ll)[2:].strip("L")
    if len(ll)%2==1:
        ll="0"+ll
    txt=binascii.unhexlify(ll)
    m=int(hashlib.md5(txt).hexdigest()[:8], 16)
    #print hex(m)
    md=le(m)
    #print hex(md)
    md^=0x86f4fa3f
    return md==0x5bffffff, hashlib.md5(txt).hexdigest()

found=None
h=None
for i in xrange(256*0x35):
    c=check(i)
    if c[0]:
        print i
        found=i
        h=c[1]
print i, h
h=binascii.unhexlify(h)

values=[int(x,16) for x in open("values").readlines()]
key="".join([struct.pack("<I",v) for v in values])

flag=""
for k, c in zip(h*10, key):
    flag+=chr(ord(k)^ord(c))
print "And the flag is..."
time.sleep(1)
print flag
