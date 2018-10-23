from collections import defaultdict

dic = defaultdict(str)
next = {}

lines = open("lop.c").readlines()
inside = False
doit = 0
start = False


for line in lines:
    if "void __noreturn opcode_" in line:
        opnum = int(line.split("_")[-1].split("(")[0])
        inside = True
    elif "__cxa_begin_catch" in line and inside:
        doit = 1
    elif "}" in line:
        inside = False
        doit = 0
    elif "exception_class" in line:
        if opnum == 118:
            start = True
        if start:
            next[opnum] = int(line.split()[-1].strip(";"))
        doit = 0

    if doit > 1:
        if "__cxa_allocate_exception" not in line:
            dic[opnum] += line

    if doit:
        doit += 1

op = 28
while True:
    print dic[op].strip()
    op = next[op]
