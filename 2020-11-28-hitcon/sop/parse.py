import struct

s = open("sop_bytecode", "rb").read()
assert len(s) % 8 == 0
pc = 0

def getbits(x, n):
    r = x & ((1<<n)-1)
    x >>= n
    return r, x

def nice(sys):
    if sys == 218:
        return "set_tid_address"
    if sys == 157:
        return "          prctl"#
    if sys == 9:
        return "           mmap"
    if sys == 0:
        return "           read"
    if sys == 1:
        return "          write"
    if sys == 13:
        return "   rt_sigaction" # Do some shit on SIGSYS
    if sys == 104:
        return "         getgid" # Probably for SIGSYS?
    if sys == 39:
        return "         getpid" # Same.
    if sys == 110:
        return "        getppid" # Same.
    if sys == 102:
        return "         getuid" # Same.
    if sys == 107:
        return "        geteuid" # Same.
    if sys == 108:
        return "        getegid" # Same.
    if sys == 111:
        return "        getpgrp" # Same.
    if sys == 186:
        return "         gettid" # Same.
    if sys == 57:
        return "           fork" # Same.
    assert False

def nice(sys):
    if sys == 218:
        return "set_tid_address"
    if sys == 157:
        return "          prctl"#
    if sys == 9:
        return "           mmap"
    if sys == 0:
        return "           read"
    if sys == 1:
        return "          write"
    if sys == 13:
        return "   rt_sigaction" # Do some shit on SIGSYS
    if sys == 104:
        return "         AND" # Probably for SIGSYS?
    if sys == 39:
        return "         ADD" # Same.
    if sys == 110:
        return "         SHL" # Same.
    if sys == 102:
        return "         SHR" # Same.
    if sys == 107:
        return "         XOR" # Same.
    if sys == 108:
        return "         SUB" # Same.
    if sys == 111:
        return "         MUL" # Same.
    if sys == 186:
        return "         OR " # Same.
    if sys == 57:
        return "         DIV" # Same.
    assert False

dis = []
while pc < len(s):
    op = struct.unpack("<Q", s[pc:pc+8])[0]
    sys, op = getbits(op, 8)
    args = []
    for i in range(6):
        t, op = getbits(op, 2)
        if t == 0:
            r, op = getbits(op, 4)
            args.append("r%d" % r)
        elif t == 1:
            r, op = getbits(op, 4)
            args.append("&r%d" % r)
        elif t == 2:
            n, op = getbits(op, 5)
            n, op = getbits(op, n+1)
            if n < 100:
                args.append("%d" % n)
            else:
                args.append("0x%x" % n)
        elif t == 3:
            break

    dis.append((pc, nice(sys), args))
    pc += 8

dis2 = []
i = 0
while i < len(dis):
    pc, sys, args = dis[i]
    try:
        pc1, sys1, args1 = dis[i+1]
    except:
        pass

    if sys.strip() == "set_tid_address" and sys1.strip() == "prctl" and args1[0] == "40":
        dis2.append((pc, "MOV", [("*"+args1[1]).replace("*&",""), args[0]]))
        i += 2
        continue
    if sys.strip() == "prctl" and args[0] == "15" and sys1.strip() == "prctl" and args1[0] == "16":
        dis2.append((pc, "STRCPY", [args1[1], args[1]]))
        i += 2
        continue

    dis2.append((pc, sys, args))
    i += 1

i = 0
while i < len(dis2):
    pc, sys, args = dis2[i]
    try:
        pc1, sys1, args1 = dis2[i+1]
        pc2, sys2, args2 = dis2[i+2]
        pc3, sys3, args3 = dis2[i+3]
        pc4, sys4, args4 = dis2[i+4]
        pc5, sys5, args5 = dis2[i+5]
    except:
        pass

# 06648: MOV *0x217022, &r7
# 06664: MOV r0, r7
# 06680: MOV r1, r11
# 06696:          ADD r0, r1, 0
# 06704:          ADD r0, r1, 16
    
    if (
            sys == "MOV" and args[0] == "*0x217022" and
            sys1 == "MOV" and args1[0] == "r0" and
            sys2 == "MOV" and args2[0] == "r1" and
            args3[0] == "r0" and args3[1] == "r1" and args3[2] == "0" and sys3 == sys4 and
            args4[0] == "r0" and args4[1] == "r1" and args4[2] == "16"):
        dst = ("*"+args[1]).replace("*&","")
        print("%05d: %s = %s %s %s" % (pc, dst, args1[1], sys3.strip(), args2[1]))
        i += 5
        continue


    print("%05d: %s %s" % (pc, sys, ", ".join(args)))
    i += 1
