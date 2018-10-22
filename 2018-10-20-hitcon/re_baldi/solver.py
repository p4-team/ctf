import socket
import telnetlib
from keystone import *
from capstone import *
from unicorn import *
from unicorn.x86_const import *
from unicorn.arm_const import *
from unicorn.arm64_const import *
from unicorn.mips_const import *

import riscv_asm
import riscv_dis
import wasmlib
from crypto_commons.netcat.netcat_commons import receive_until_match, receive_until
from ppclib import ppc_execute
from risclib import risc_execute

last_stage = False
s = socket.socket()

Ks(KS_ARCH_PPC, KS_MODE_PPC32 + KS_MODE_BIG_ENDIAN)


def interactive(s):
    t = telnetlib.Telnet()
    t.sock = s
    t.interact()


def level():
    challenge = receive_until_match(s, r'Press the Enter key to start the challenge...')
    print(challenge)
    s.send("\n")
    code = receive_until_match(s, r'Answer:')
    print 'code', code
    raw_code = '\n'.join(code.split('\n')[1:-1])
    print 'raw_code', raw_code
    if '|   | |___    | | |_| | |   |___ ' in challenge:
        arch = 'i386'
        ks = (KS_ARCH_X86, KS_MODE_32)
        cs = (CS_ARCH_X86, CS_MODE_32)
        uc = (UC_ARCH_X86, UC_MODE_32)
        uc_result = UC_X86_REG_EAX
        uc_stack = UC_X86_REG_ESP
    elif "`.  `'    .'  / /       \ '  /  ' _   \\" in challenge:
        arch = 'x64'
        ks = (KS_ARCH_X86, KS_MODE_64)
        cs = (CS_ARCH_X86, CS_MODE_64)
        uc = (UC_ARCH_X86, UC_MODE_64)
        uc_result = UC_X86_REG_RAX
        uc_stack = UC_X86_REG_RSP
    elif ' |_   _|   | || |  |_   __ \   | || |   /  ___  |  |' in challenge:
        arch = 'mips'
        ks = (KS_ARCH_MIPS, KS_MODE_MIPS32 + KS_MODE_BIG_ENDIAN)
        cs = (CS_ARCH_MIPS, CS_MODE_MIPS32 + CS_MODE_BIG_ENDIAN)
        uc = (UC_ARCH_MIPS, UC_MODE_MIPS32 + UC_MODE_BIG_ENDIAN)
        uc_result = UC_MIPS_REG_V0
        uc_stack = UC_MIPS_REG_29
    elif '/ /\ \     / /\ \    ) (__) )   / /      \ (__) /   / /      ( (__) (_' in challenge:
        arch = 'aarch64'
        ks = (KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN)
        cs = (CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
        uc = (UC_ARCH_ARM64, UC_MODE_ARM)
        uc_result = UC_ARM64_REG_X0
        uc_stack = UC_ARM64_REG_SP
    elif '|____| |____||____| |___||_____||_____' in challenge:
        arch = 'arm'
        ks = (KS_ARCH_ARM, KS_MODE_ARM)
        cs = (CS_ARCH_ARM, CS_MODE_ARM)
        uc = (UC_ARCH_ARM, UC_MODE_ARM)
        uc_result = UC_ARM_REG_R0
        uc_stack = UC_ARM_REG_SP
    elif '|_|  \_\_____|_____/ \_____|      \/ ' in challenge:  # risc
        arch = 'risc'
        response = riscv_asm.asm(raw_code).encode('base64').replace('\n', '')
        global last_stage
        last_stage = True
    elif last_stage:
        arch = 'wasm'
        response = wasmlib.asm(raw_code).encode('base64').replace('\n', '')
    else:
        # assume PPC32
        arch = 'ppc32'
        ks = (KS_ARCH_PPC, KS_MODE_PPC32 + KS_MODE_BIG_ENDIAN)
        cs = (CS_ARCH_PPC, CS_MODE_32 + CS_MODE_BIG_ENDIAN)
        for i in range(32):
            raw_code = raw_code.replace("r" + str(i), str(i))
    print 'architecture:', arch
    if arch != 'risc' and arch!='wasm':
        ks = Ks(ks[0], ks[1])
        encoding, count = ks.asm(raw_code)
        if arch == 'mips':
            encoding = encoding[:-4]  # untestedy yet
        response = ''.join(map(chr, encoding)).encode('base64').replace('\n', '')
    print 'response', response
    s.send(response + '\n')
    print(receive_until(s, '\n'))
    out = receive_until(s, '\n')
    print(out)
    if arch == 'risc':
        code = out.decode('base64')
        result = riscv_dis.dis(code)
    elif arch == 'wasm':  # wasm
        code = out.decode('base64')
        result = wasmlib.dis(code)
    else:
        cs = Cs(cs[0], cs[1])
        result = []
        for i in cs.disasm(out.decode('base64'), 0x1000):
            result += [(i.mnemonic + " " + i.op_str).strip()]
        result = '\n'.join(result)
    print 'asm', result
    resultb64 = result.encode('base64').replace('\n', '')
    print 'asmb64', resultb64
    s.send(resultb64 + '\n')
    print 'D', s.recv(99999)
    print 'E', s.recv(99999)
    challenge = s.recv(99999)
    print repr(challenge)
    data = challenge[8:-10]
    print data.encode('hex')

    if arch == 'risc':
        result = riscv_dis.dis(data)
        print(result)
    elif arch == 'wasm':
        result = wasmlib.dis(data)
        print(result)
    else:
        result = []
        for i in cs.disasm(challenge, 0x1000):
            result += [(i.mnemonic + " " + i.op_str).strip()]
        result = '\n'.join(result)
        print result

    # callback for tracing instructions
    def hook_code(uc, address, size, user_data):
        print(">>> Tracing instruction at 0x%x, instruction size = 0x%x" % (address, size))
        for kot in cs.disasm(data[address - ADDRESS:address - ADDRESS + size], 4):
            OP = kot.mnemonic + " " + kot.op_str
            print 'OK', OP
            break
        if 'jr $ra' in OP:
            uc.emu_stop()
        elif 'ret' in OP:
            uc.emu_stop()
        elif 'bx lr' in OP:
            uc.emu_stop()
        return 'kot'

    if arch == 'ppc32':
        out = ppc_execute(result)
    elif arch == 'risc':
        out = risc_execute(result)
    elif arch == 'wasm':
        out = wasmlib.eval(result)
    else:
        uc = Uc(uc[0], uc[1])
        ADDRESS = 0x10000000
        STACK = 0x20000000
        uc.mem_map(ADDRESS, 4 * 1024 * 1024)
        uc.mem_map(STACK, 4 * 1024 * 1024)
        uc.mem_write(ADDRESS, data)
        uc.reg_write(uc_stack, STACK + 0x2000)
        # tracing one instruction at ADDRESS with customized callback
        uc.hook_add(UC_HOOK_CODE, hook_code, begin=ADDRESS, end=ADDRESS + len(data))
        uc.emu_start(ADDRESS, ADDRESS + len(data))
        out = uc.reg_read(uc_result)
    print "RESULT", hex(out)
    if arch!='wasm':
        s.sendall(hex(out).replace('L', '') + '\n')
    else:
        s.sendall(str(out)+"\n")
        interactive(s)
    print(receive_until_match(s, '------------------------------'))
    data = receive_until_match(s, '------------------------------')
    print(data)
    if "Wrong" in data:
        interactive(s)


def main():
    global s
    s = socket.socket()
    s.connect(('13.231.83.89', 30262))
    print 'A', s.recv(999999)
    print 'B', s.recv(999999)
    s.send('\n')
    print 'C', s.recv(999999)
    print 'D', s.recv(999999)
    s.send('\n')
    print 'E', s.recv(999999)
    print 'F', s.recv(999999)
    s.send('\n')
    print 'G', s.recv(999999)
    print 'H', s.recv(999999)
    s.send('A\n')
    print 'I', s.recv(999999)
    print 'J', s.recv(999999)
    s.send('\n')
    print 'K', s.recv(999999)
    print 'L', s.recv(999999)
    s.send('B\n')
    print 'M', s.recv(999999)
    print 'N', s.recv(999999)
    s.send('\n')
    print 'O', s.recv(999999)
    s.send('duck\n')

    for i in range(7):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('w\n')
    level()

    for i in range(16):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('d\n')
    print(receive_until_match(s, "w/a/s/d:"))
    s.sendall('w\n')
    level()

    for i in range(9):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('s\n')
    level()

    for i in range(16):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('a\n')
    print(receive_until_match(s, "w/a/s/d:"))
    s.sendall('s\n')
    level()

    for i in range(15):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('a\n')
    print(receive_until_match(s, "w/a/s/d:"))
    s.sendall('s\n')
    level()

    for i in range(6):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('d\n')
    for i in range(4):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('w\n')
    for i in range(2):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('a\n')
    level()

    for i in range(4):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('w\n')
    for i in range(5):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('a\n')
    print(receive_until_match(s, "w/a/s/d:"))
    s.sendall('w\n')
    level()

    while True:
        data = receive_until_match(s, '(Press the Enter key to continue...)')
        print(data)
        if 'EXIT2' in data:
            break
        s.sendall('\n')
    rakflag()


def rakflag():
    for i in range(7):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('w\n')
    for i in range(16):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('d\n')
    print(receive_until_match(s, "w/a/s/d:"))
    s.sendall('w\n')
    for i in range(10):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('s\n')
    for i in range(17):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('a\n')
    print(receive_until_match(s, "w/a/s/d:"))
    s.sendall('s\n')
    for i in range(16):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('a\n')
    print(receive_until_match(s, "w/a/s/d:"))
    s.sendall('s\n')
    for i in range(6):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('d\n')
    for i in range(4):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('w\n')
    for i in range(2):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('a\n')
    for i in range(4):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('w\n')
    for i in range(5):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('a\n')
    for i in range(2):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('w\n')
    for i in range(25):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('d\n')
    for i in range(4):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('s\n')
    for i in range(10):
        print(receive_until_match(s, "w/a/s/d:"))
        s.sendall('d\n')
    print(receive_until_match(s, "(Press the Enter key to continue...)"))
    s.sendall("\n")
    print(receive_until_match(s, "(Press the Enter key to continue...)"))
    s.sendall("\n")
    print(receive_until_match(s, "(Press the Enter key to continue...)"))
    s.sendall("\n")
    level()
    s.sendall("\n")
    s.sendall("\n")
    s.sendall("\n")
    interactive(s)


main()
