

s = open("generated.h").read()
s = s.split("{")[1].split("}")[0]
s = s.split(",")
s = [int(c, 16) for c in s]

# DECRYPT
key = [0x4b, 0xa9, 0xdc, 0x18][::-1]
for i in range(0x38, 0xa0):
    s[i] ^= key[i%4]

key = [0x17, 0xdb, 0x41, 0xdc][::-1]
for i in range(0xf4, 0x13c):
    s[i] ^= key[i%4]

key = [0x73, 0xd4, 0x01, 0xac][::-1]
for i in range(0x190, 0x21c):
    s[i] ^= key[i%4]

opcode_table = {}
for line in open("parsed").readlines():
    name, op, args = line.strip().split("|")
    args = args.split()
    opcode_table[int(op, 16)] = name, args


pc = 0
hadret = True
while pc < len(s):
    if hadret and pc % 4 == 0:
        hadret = False
        print "----"

    try:
        name, args = opcode_table[s[pc]]
    except:
        name = hex(s[pc])
        args = []

    if name == "RET":
        hadret = True
    #print name, args
    pc0 = pc
    pc += 1
    act_args = s[pc:pc+len(args)]
    length = len(args)

    if (name == "EECALL" or name == "EELOADA" or name == "EESAVEA" or
        name == "EELOAD" or name == "EESAVE"):
        act_args[-1] *= 4

    if 0 and name == "EEWRITE":
        slot, num = act_args[:2]
        act_args = [slot*4] + s[pc+2:pc+2+num]
        length = 2 + num

    if name == "WRBLK":
        num = act_args[0] * 4
        act_args = s[pc+1:pc+1+num]
        length = 1 + num

    if name == "STRSET" or name == "STRCMP" or name == "STRFCHR":
        act_args = []
        i = pc
        while s[i]:
            act_args.append(s[i])
            i += 1
        length = i - pc + 1

    act_args = ", ".join(["{:02x}".format(a) for a in act_args])
    pc += length

    print "{:03x}: {} {}".format(pc0, name, act_args)
