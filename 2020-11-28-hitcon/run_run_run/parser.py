opcodes = """
    public static final int NOP = 0;
    public static final int INCSP = 1;
    public static final int POPV = 2;
    public static final int ADD = 3;
    public static final int SUB = 4;
    public static final int MUL = 5;
    public static final int DIV = 6;
    public static final int AND = 7;
    public static final int OR = 8;
    public static final int MOD = 9;
    public static final int SHL = 10;
    public static final int SHR = 11;
    public static final int XOR = 12;
    public static final int GETV = 13;
    public static final int PUTV = 14;
    public static final int INVOKE = 15;
    public static final int AGETV = 16;
    public static final int APUTV = 17;
    public static final int LGETV = 18;
    public static final int LPUTV = 19;
    public static final int NEWA = 20;
    public static final int NEWC = 21;
    public static final int RETURN = 22;
    public static final int RET = 23;
    public static final int NEWS = 24;
    public static final int GOTO = 25;
    public static final int EQ = 26;
    public static final int LT = 27;
    public static final int LTE = 28;
    public static final int GT = 29;
    public static final int GTE = 30;
    public static final int NE = 31;
    public static final int ISNULL = 32;
    public static final int ISA = 33;
    public static final int CANHAZPLZ = 34;
    public static final int JSR = 35;
    public static final int TS = 36;
    public static final int IPUSH = 37;
    public static final int FPUSH = 38;
    public static final int SPUSH = 39;
    public static final int BT = 40;
    public static final int BF = 41;
    public static final int FRPUSH = 42;
    public static final int BPUSH = 43;
    public static final int NPUSH = 44;
    public static final int INV = 45;
    public static final int DUP = 46;
    public static final int NEWD = 47;
    public static final int GETM = 48;
    public static final int LPUSH = 49;
    public static final int DPUSH = 50;
    public static final int THROW = 51;
    public static final int CPUSH = 52;
    public static final int ARGC = 53;
    public static final int NEWBA = 54;
"""

srcmap = """
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconMenuDelegate.mc:6 initialize (pc 268435456)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconMenuDelegate.mc:7 initialize (pc 268435460)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconMenuDelegate.mc:10 onMenuItem (pc 268435479)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconMenuDelegate.mc:11 onMenuItem (pc 268435483)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconMenuDelegate.mc:12 onMenuItem (pc 268435494)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconMenuDelegate.mc:13 onMenuItem (pc 268435518)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconMenuDelegate.mc:14 onMenuItem (pc 268435529)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:16 initialize (pc 268435554)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:17 initialize (pc 268435558)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:18 initialize (pc 268435576)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:22 onLayout (pc 268435611)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:23 onLayout (pc 268435615)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:27 onUpdate (pc 268435636)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:28 onUpdate (pc 268435640)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:29 onUpdate (pc 268435660)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:30 onUpdate (pc 268435678)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:31 onUpdate (pc 268435718)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:32 onUpdate (pc 268435737)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:33 onUpdate (pc 268435759)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:35 onUpdate (pc 268435796)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:36 onUpdate (pc 268435818)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:37 onUpdate (pc 268435844)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:41 timerCallback (pc 268435913)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:42 timerCallback (pc 268435917)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:43 timerCallback (pc 268435936)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:46 solve (pc 268435953)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:47 solve (pc 268435957)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:48 solve (pc 268435964)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:50 solve (pc 268435985)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:51 solve (pc 268436008)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:52 solve (pc 268436018)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:53 solve (pc 268436046)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:54 solve (pc 268436050)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:55 solve (pc 268436054)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:57 solve (pc 268436061)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:60 drawFlag (pc 268436065)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:61 drawFlag (pc 268436069)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:62 drawFlag (pc 268436105)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:63 drawFlag (pc 268436117)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:64 drawFlag (pc 268436153)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:65 drawFlag (pc 268436172)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:66 drawFlag (pc 268436191)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconDelegate.mc:5 initialize (pc 268436247)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconDelegate.mc:6 initialize (pc 268436251)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconDelegate.mc:9 onMenu (pc 268436270)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconDelegate.mc:10 onMenu (pc 268436274)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconDelegate.mc:11 onMenu (pc 268436358)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconApp.mc:6 initialize (pc 268436362)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconApp.mc:7 initialize (pc 268436366)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconApp.mc:11 onStart (pc 268436385)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconApp.mc:15 onStop (pc 268436390)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconApp.mc:19 getInitialView (pc 268436395)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconApp.mc:20 getInitialView (pc 268436399)
    Rez:15 MainLayout (pc 268436437)
    Rez:26 initialize (pc 268436450)
    Rez:27 initialize (pc 268436454)
    Rez:28 initialize (pc 268436472)
    Rez:29 initialize (pc 268436528)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:11 <init> (pc 268437102)
    C:/Users/lyc/eclipse-workspace/hitcon/source/hitconView.mc:12 <init> (pc 268437660)
"""

def getsz(n): 
    if n in [49, 50]: return 9
    if n in [24, 37, 38, 39, 52]: return 5
    if n in [25, 35, 40, 41]: return 3
    if n in [1, 10, 11, 15, 18, 19, 43, 46, 53]: return 2
    return 1

opmap = []
for line in opcodes.splitlines():
    line = line.strip()
    if not line: continue
    line = line.split()
    name = line[-3]
    opmap.append(name)

srcmapx = {}
prevfun = None
for line in srcmap.splitlines():
    line = line.strip()
    if not line: continue
    s = line.split()
    fun = s[-3]
    if fun == prevfun: continue
    prevfun = fun
    pc = int(s[-1][:-1]) - 268435456
    srcmapx[pc] = line

syms = {}
for line in open("syms").readlines():
    line = line.strip()
    if not line: continue
    line = line.split(":")
    arg = int(line[0])
    syms[arg] = line[1].strip()

import sys, struct

s = open(sys.argv[1], "rb").read()
n = s.find(b"\xc0\xde\xba\xbe")
assert n != -1
sz = struct.unpack(">I", s[n+4:n+8])[0]
s = s[n+8:][:sz]
pc = 0
while pc < len(s):
    op = s[pc]
    sz = getsz(op)
    arg = s[pc+1:][:sz-1]
    args = 0
    for a in arg:
        args *= 256
        args += a
    if len(arg) == 2:
        args += pc + 3
        args &= 65535
    if opmap[op] == "SPUSH":
        args = syms[args]
    if (opmap[op] == "ARGC"): print()
    if pc in srcmapx:
        print(srcmapx[pc])
        print()
    print("%04d: %s %s" % (pc, opmap[op], args))
    pc += sz

