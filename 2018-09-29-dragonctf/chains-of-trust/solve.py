from pwn import *
import struct
from unicorn import *
from unicorn.x86_const import *


r = remote("chains.of.trust.felinae.pl", 7679)
byte = ord(r.recv(1))

def recv(n):
    data = ""
    while len(data) != n:
        data += r.recv(n-len(data))
    return data

def read_decode_binary():
    ln = struct.unpack("<I", r.recv(4))[0]
    data = recv(ln)
    open("/tmp/dump", "wb").write(data)

    # memory address where emulation starts
    ADDRESS = 0x1000000


    rest = {}
    def hook_code64(uc, address, size, user_data):
        rip = uc.reg_read(UC_X86_REG_RIP)
        mem = uc.mem_read(rip, size)
        #print("AAA Tracing instruction at 0x%x, instruction size = 0x%x %s" %(address, size, repr(mem)))
        if mem[0] == 0xe8: # CALL
            rest[0] = struct.unpack("<I", mem[1:])[0] + rip + 5
            uc.emu_stop()



    print("Emulate x86_64 code")
    mu = Uc(UC_ARCH_X86, UC_MODE_64)
    mu.mem_map(ADDRESS, 2 * 1024 * 1024)
    mu.mem_write(ADDRESS, data)

    mu.reg_write(UC_X86_REG_RSP, ADDRESS + 0x200000)

    mu.hook_add(UC_HOOK_CODE, hook_code64)

    mu.emu_start(ADDRESS, ADDRESS + len(data))

    mem = mu.mem_read(ADDRESS, len(data))
    open("/tmp/dec", "wb").write(mem)

    print rest
    return mem, rest[0]


cnt_mmap = 0
ptraced = False
def dispatch(uc, num):
    rdi = uc.reg_read(UC_X86_REG_RDI)
    rsi = uc.reg_read(UC_X86_REG_RSI)
    rip = uc.reg_read(UC_X86_REG_RIP)

    def sendbyte(uc):
        b = rdi & 0xff
        print "Sending byte", b
        r.send(chr(b))
        return 1

    def sendbuf(uc):
        buf = str(uc.mem_read(rdi, rsi))
        print "Sending buf", repr(buf)
        r.send(buf)
        return len(buf)

    def recvbuf(uc):
        buf = recv(rsi)
        uc.mem_write(rdi, buf)
        print "Received buf", repr(buf)
        return len(buf)

    def puts(uc):
        buf = str(uc.mem_read(rdi, 256))
        buf = buf.split("\x00")[0]
        print "puts", buf
        return len(buf)

    def printf(uc):
        buf = str(uc.mem_read(rdi, 256))
        buf = buf.split("\x00")[0]
        print "printf", repr(buf), hex(rsi)
        return len(buf)

    def dlopen(uc):
        buf = str(uc.mem_read(rdi, 256))
        buf = buf.split("\x00")[0]
        print "dlopen", repr(buf)
        return 1

    def msleep(uc):
        print "msleep", rdi
        return 1

    def dlsym(uc):
        buf = str(uc.mem_read(rsi, 256))
        buf = buf.split("\x00")[0]
        print "dlsym", repr(buf)
        if buf == "ptrace":
            return ADDRESS + 0x20000 + 8 * 50

        if buf in ["readlink", "getppid", "environ", "getenv", "strstr", "fopen"]:
            buf = uc.mem_read(ADDRESS, 0x1000)
            f = buf.find("488B4010".decode("hex"))
            print "FOUND AT", f
            f2 = buf.find("488B4010".decode("hex"), f+1)
            assert f != -1
            assert f2 == -1
            print "And kay"
            if buf[f-4] == 0x48:
                f -= 4
            else:
                f -= 7
            uc.reg_write(UC_X86_REG_RIP, ADDRESS + f)
            return 12345
        else:
            print "not n"

        if buf == "getenv":
            return ADDRESS + 0x20000 + 8 * 51
        if buf == "getppid":
            return ADDRESS + 0x20000 + 8 * 52
        if buf == "errno":
            return ADDRESS + 0x20000 + 8 * 53
        
        raise Exception("dlsym")

    def pthread(uc):
        print "pthread"

        return 0

    def mmap(uc):
        global retnext, cnt_mmap
        print "\t\t\tmmap number", cnt_mmap
        buf = uc.mem_read(ADDRESS, 0x1000)
        open("/tmp/xmap_%d" % cnt_mmap, "wb").write(str(buf))

        cnt_mmap += 1
        return ADDRESS+0x40000+cnt_mmap*4096
        """
        retnext = True
        buf = uc.mem_read(ADDRESS, 0x1000)
        open("/tmp/mmap_%d" % cnt_mmap, "wb").write(str(buf))
        if cnt_mmap != 1:
            r.send(struct.pack("<Q", ADDRESS+0x40000+cnt_mmap*4096))

        if cnt_mmap in [6, 7, 8, 9]:
            print "XXX", repr(recv(1))
            print "XXX", repr(recv(8))
        elif cnt_mmap in [10, 11]:
            print "XXX", repr(recv(8))
            for i in range(4):
                print "XXX", repr(recv(8))
        elif cnt_mmap >= 12:
            print "XXX", repr(recv(8))
            print "XXX", repr(recv(8))
            for i in range(4):
                print "XXX", repr(recv(8))
        cnt_mmap += 1
        return 1
        """

    def exitx(uc):
        print "exit"
        raise Exception("exit")

    assert num % 8 == 0
    num /= 8
    try:
        if num == 50: # ptrace
            global ptraced
            if ptraced == False:
                rv = 0
                ptraced = True
            else:
                rv = -1
                errno = 1
                uc.mem_write(ADDRESS + 0x20000 + 8 * 53, struct.pack("<Q", 1))

        elif num == 51: # getenv
            buf = str(uc.mem_read(rdi, 256))
            buf = buf.split("\x00")[0]
            print "getenv", buf
            rv = 0
        elif num == 52: # getppid
            print "getppid"
            rv = 1234
        else:
            rv = [
                    sendbyte, sendbuf, recvbuf, exitx,
                    puts, printf, 0, 0, 
                    0, mmap, msleep, pthread,
                    dlsym, dlopen
            ][num](uc)
        if rv == 12345:
            return "PASS"
        uc.reg_write(UC_X86_REG_RAX, rv)
        return "OK"
    except Exception as e:
        print "Ugh", num, e
        return "STOP"

retnext = False
while True:
    mem, rest = read_decode_binary()
    ADDRESS = 0x1000000
    rest -= ADDRESS

    def hook_code64(uc, address, size, user_data):
        global retnext
        rip = uc.reg_read(UC_X86_REG_RIP)
        if retnext and rip < ADDRESS + 0x20000 -1:
            retnext = False
            buf = uc.mem_read(rip, 0x1000)
            f = buf.find("\xc9\xc3")
            f += rip
            print hex(rip), "FOUND AT", f-ADDRESS
            assert f != -1
            uc.reg_write(UC_X86_REG_RIP, f)
            return
        mem = uc.mem_read(rip, size)
        rsp = uc.reg_read(UC_X86_REG_RSP)
        if rsp == ADDRESS + 0x200000 and mem[0] == 0xc3:
            uc.emu_stop()
            return

        if rip >= ADDRESS + 0x20000:
            res = dispatch(uc, rip - (ADDRESS+0x20000))
            if res == "STOP":
                uc.emu_stop()
                return
            if res != "PASS":
                rip = uc.reg_write(UC_X86_REG_RIP, ADDRESS+0x20000-1)

        #print(">>> Tracing instruction at 0x%x, instruction size = 0x%x %s" %(address, size, repr(mem)))

    print("Emulate x86_64 code")
    mu = Uc(UC_ARCH_X86, UC_MODE_64)
    mu.mem_map(ADDRESS, 2 * 1024 * 1024)
    mu.mem_write(ADDRESS, str(mem))

    mu.reg_write(UC_X86_REG_RSP, ADDRESS + 0x200000)

    mu.mem_write(ADDRESS+0x20000-1, "\xc3")
    buf = ""
    for i in range(100):
        buf += struct.pack("<Q", ADDRESS+0x20000+i*8)

    mu.mem_write(ADDRESS + 0x10000, buf)
    mu.reg_write(UC_X86_REG_RDI, ADDRESS + 0x10000)
    mu.reg_write(UC_X86_REG_RSI, byte)

    mu.hook_add(UC_HOOK_CODE, hook_code64)

    mu.emu_start(ADDRESS+rest, ADDRESS + len(mem))

    byte = mu.reg_read(UC_X86_REG_RAX) & 0xff
    print "byte", hex(byte)
