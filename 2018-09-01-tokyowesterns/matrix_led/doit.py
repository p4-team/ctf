from aes import enc, dec

col = [
#   (b, g, r, 0)
    (0, 0, 6, 0), # RED
    (0, 3, 6, 0), # ORA
    (0, 6, 6, 0), # YEL
    (0, 6, 0, 0), # GRE
    (6, 6, 0, 0), # LBL
    (6, 0, 0, 0), # DBL
    (6, 0, 6, 0), # PIN
    (6, 6, 6, 0), # WHI
]

key = (
"GRRR LYYW" +
"DRYY LPPD" +
"DROG YWLD" +
"GWDR DGPD" +
"OPPR GOPY" +
"YGWR DRYL" +
"GGGD WPLO" +
"YWOD DYWW" )


def conv1(s):
    s = s.replace(" ", "")
    s = ["ROYGLDPW".index(c) for c in s]
    return s

def rot(block):
    ret = []
    for i in range(0, 8, 2):
        for j in range(8):
            ret.append(block[i + j*8])
        for j in range(8)[::-1]:
            ret.append(block[i + j*8 + 1])

    return ret

def to_bytes(block):
    ret = ""
    for b in block:
        ret += "{:03b}".format(b)
    s = []
    for i in range(24):
        s.append(int(ret[i*8:i*8+8], 2))
    return s

import subprocess
def check(block, chk):
    p = subprocess.Popen(["other/simavr/run_avr",
        "/home/adam/VirtualBoxVMs/SharedFolder/MatrixLED.ino.elf",
        "-m", "atmega32u4"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    s = "%s\n" % " ".join(str(c) for c in block)
    p.stdin.write(s)
    p.stdin.close()
    for line in p.stdout.readlines():
        if line.startswith("Res:"):
            p.kill()
            return line.split()[1][:16] == "".join(
                    ("{:02x}".format(c) for c in chk))
    assert False


key = to_bytes(rot(conv1(key)))
key, chk = key[:16], key[16:]
assert check(key, chk)

def decode_block(block):
    data = to_bytes(rot(block))
    data, chk = data[:16], data[16:]
    if check(data, chk):
        return [], data

    for i in range(64):
        if block[i] not in [1, 2]: continue
        block2 = block[:]
        block2[i] = 3 - block[i]
        data = to_bytes(rot(block2))
        data, chk = data[:16], data[16:]
        if check(data, chk):
            return [("at %d from %d to %d" % (i, block[i], block2[i]))], data

    for i in range(64):
        if block[i] not in [1, 2]: continue
        block2 = block[:]
        block2[i] = 3 - block[i]
        for i2 in range(i):
            if block[i2] not in [1, 2]: continue
            block3 = block2[:]
            block3[i2] = 3 - block[i2]
            data = to_bytes(rot(block3))
            data, chk = data[:16], data[16:]
            if check(data, chk):
                return [
                        ("at %d from %d to %d" % (i, block[i], block3[i])),
                        ("at %d from %d to %d" % (i2, block[i2], block3[i2]))
                        ], data
    return [], None
    for i in range(64):
        if block[i] not in [1, 2]: continue
        block2 = block[:]
        block2[i] = 3 - block[i]
        for i2 in range(i):
            if block[i2] not in [1, 2]: continue
            block3 = block2[:]
            block3[i2] = 3 - block[i2]
            for i3 in range(i2):
                if block[i3] not in [1, 2]: continue
                block4 = block3[:]
                block4[i3] = 3 - block[i3]
                data = to_bytes(rot(block4))
                data, chk = data[:16], data[16:]
                if check(data, chk):
                    return [
                            ("at %d from %d to %d" % (i, block[i], block4[i])),
                            ("at %d from %d to %d" % (i2, block[i2], block4[i2])),
                            ("at %d from %d to %d" % (i2, block[i2], block4[i3])),
                            ], data

    for i in range(64):
        for j in range(8):
            block2 = block[:]
            block2[i] = j
            data = to_bytes(rot(block2))
            data, chk = data[:16], data[16:]
            if check(data, chk):
                return [("at %d from %d to %d" % (i, block[i], j))], data

    return [], None

import ast
import sys
infile = sys.argv[1]
outfile = sys.argv[2]
nfrom = int(sys.argv[3])
nto = int(sys.argv[4])

of = open(outfile, "w")
for aa in open(infile).readlines():
    line = int(aa.split()[0])
    if line not in range(nfrom, nto):
        continue

    aa = ast.literal_eval("[" + aa.split("[")[1])

    i, aa = decode_block(aa)
    if aa is not None:
        of.write(str(line) + " " + str(dec(aa, key)) + "\n")
        
    if aa is None:
        print line, "!!!!!!!!!!!!"
    else:
        print line, "OK", len(i)
