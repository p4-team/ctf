import binascii, hashlib, time, string, sys, zlib, qrcode
from pwn import *

context.log_level="debug"

r=remote("ctf.sharif.edu", 12432)
time.sleep(0.5)
r.recvline()
r.recvline()
s=r.recvline()
s=s[-24:-2]
r.recvline()

wanted=s
i=0
while True:
    i+=1
    s=hex(i)[2:]
    s=(8-len(s))*"0"+s
    dig=bin(int(hashlib.md5(s).hexdigest()[:6], 16))[2:]
    dig="0"*(24-len(dig))+dig
    if dig[:22]==wanted:
        c=hex(i)[2:]
        r.send( (8-len(c))*"0"+c )
        break
    if i%500000==0:
        pass
        print i

print r.recvline()
#print s[:16]
#key=s[16:-53]
#print repr(key)
#print s[-53:]
data=r.recv()
print "Decompressed input:"
print zlib.decompress(data)

qr=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=1, border=1)
qr.add_data(sys.argv[1])
qr.make()
qr.make_image().save("test.png")

data=zlib.compress(open("test.png","rb").read(), 9)

r.send(data+"\x00"*(200-len(data)))
time.sleep(0.5)

print r.recv()
