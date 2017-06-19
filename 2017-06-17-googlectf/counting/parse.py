import struct, string, sys

s = open("code", "rb").read()
s=s[4:]

al = string.uppercase

instructions = []
for i in range(len(s)/16):
    tp, reg, n1, n2 = struct.unpack("<IIII", s[i*16:i*16+16])
    instructions.append((tp, reg, n1, n2))

for i, ins in enumerate(instructions):
    tp, reg, n1, n2 = ins
    print "%02d:" % i,
    if tp == 0:
        print "r"+al[reg]+"++; jmp %02d;"%n1
    elif tp == 1:
        print "if (r"+al[reg]+"!=0){ r"+al[reg]+"--; jmp %02d"%n1+";} else jmp %02d;"%n2
    else:
        print "fork @ %02d"%n1+"; copy up to r"+al[reg]+"; jmp %02d;"%n2

regs = [0]*26
regs[0] = int(sys.argv[1])

count = [0]*120

def fibmod(n, m):
    if n<=1:
        return n%m
    a = 0
    b = 1
    for i in range(n):
        c = (a+b)%m
        a=b
        b=c
    return a

def collatz(n):
    if n % 2 == 0:
        return n/2
    else:
        return 3*n+1

remc=[-1 for i in range(10000)]
remc[0]=0
remc[1]=0
def collatzcnt(n):
    if n>=len(remc):
        return 1+collatzcnt(collatz(n))
    while remc[n]==-1:
        remc[n] = 1+collatzcnt(collatz(n))
    return remc[n]

for i in range(10000):
    collatzcnt(i)

print "preproc"

rem=[0]

def sumcollatzcnt(n):
    if n<=len(rem):
        return rem[n]
    s = rem[-1]
    for i in range(len(rem)+1, n+1):
        s += collatzcnt(i)
        rem.append(s)
    return s

def run(regs, pc):
    while pc!=len(instructions):
        count[pc]+=1
        # peephole
        if pc == 116:
            regs[0] = regs[1]
            break
        elif pc==113:
            regs[0] = max(0, regs[1]-regs[2])
            break
        elif pc==108:
            if regs[2]>regs[1]:
                regs[0] = 1
            else:
                regs[0] = 0
            break
        elif pc==99:
            regs[0] = regs[1] % regs[2]
            break
        elif pc ==84:
            regs[0] = regs[1]
            break
        elif pc == 92: 
            regs[0]=regs[2]/2
            regs[1]=regs[2]%2;
            break
        elif pc == 45:
            regs[0] = collatz(regs[1])
            break
        elif pc == 64:
            regs[0] = fibmod(regs[1], regs[2])
            break
        elif pc == 29:
            regs[0] = collatzcnt(regs[1])
            break
        elif pc == 20:
            regs[0] = sumcollatzcnt(regs[1])
            break
        elif pc == 0: 
            a = regs[0]
            if a<11:
                regs[0] = 0
            else:
                s = sumcollatzcnt(a)
                print hex(s)
                regs[0] = fibmod(a, s)
            break

        ins = instructions[pc]
        tp, reg, n1, n2 = ins
        if tp==0:
            regs[reg]+=1
            pc = n1
        elif tp==1:
            if regs[reg]:
                regs[reg] -= 1
                if pc == n1:
                    regs[reg] = 0
                pc = n1
            else:
                pc = n2
        else:
            childregs = regs[:]
            run(childregs, n1)
            for i in range(reg):
                regs[i] = childregs[i]
            pc = n2

run(regs, 0)
for i, c in enumerate(count):
    print i, c
print hex(regs[0])
