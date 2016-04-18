import subprocess, sys

def gdb(txt):
    p=subprocess.Popen(["gdb", "qqq"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.stdin.write("set disassembly-flavor intel\n")
    p.stdin.write("b *0x804820a\n")
    p.stdin.write("r --pctfkey PCTF{1234567890qwertyuiop1234567890qwertyuiop1234567}\nc\n")
    p.stdin.write(txt+"\nq\n")
    return p.stdout.read()

ROP_LEN=(2**18)/4
ROP_POS=0x0818c080
out=gdb("x/"+str(ROP_LEN)+"d "+str(ROP_POS))
out=out.split("(gdb) ")[5]

rop=[]

for line in out.splitlines():
    print line
    for num in line.split("\t")[1:]:
        rop.append( (int(num)+2**32)%(2**32) )

while rop[-1]==0:
    rop.pop()

print "ROP_CHAIN"
print "Length:",len(rop),"dwords"
for r in rop:
    print hex(r)

print "VALUES"
f=open("values","w")
for i in range(14):
    f.write(hex(rop[0x208c4/4+i*7])+"\n")
f.close()

f=open("ropchain","w")

cache={}
for index, r in enumerate(rop):
    if r in cache:
        out=cache[r]
    else:
        out=gdb("x/10i "+str(r))
        out=out.split("(gdb) ")[5]
        cache[r]=out
    print hex(r), index,"out of",len(rop)
    f.write(hex(r)+" - ROP offset: "+hex(index*4)+"\n")
    out=out.splitlines()
    res=None
    for i, line in enumerate(out):
        if line.find("ret")>-1:
            res="\n".join(out[:i+1])
            break
        if r==ord("w"):
            f.write("Note: this is probably FAILING place.\n")
    if res is None:
        f.write("\n".join(out)+"\n")
    else:
        f.write(res+"\n")

NUM_STEPS=5000
s="display/i $eip\n"
for reg in ["eax", "ebx", "ecx", "edx", "esp", "ebp", "esi", "edi"][::-1]:
    s+="display/x $"+reg+"\n"
s+="si\n"*NUM_STEPS
out=gdb(s)
for line in out.splitlines():
    if line.find("(gdb)")>-1:
        print ""
    elif line.find("/x")>-1:
        print line
    elif line.find("=>")>-1:
        print line
