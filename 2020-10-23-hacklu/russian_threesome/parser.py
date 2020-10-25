import sys

drum = open(sys.argv[1], "rb").read()
s = open("emulator", "rb").read()
s = s[s.find(b"\xd0\x82\x00"):]
s = s.split(b"\x00\x00\x00")[0].split(b"\x00")
charset = []
for ss in s:
    try:
        sss = ss.decode()
    except:
        sss = "???"
    charset.append(sss)


def as_trit(b):
    return "-0+"[b]

def to_int(tr):
    n = 0
    p3 = 1
    for c in tr[::-1]:
        n += ("-0+".index(c)-1) * p3
        p3 *= 3
    return n

def to_int_pack(tr):
    n = 0
    p3 = 1
    for c in tr[::-1]:
        n += ("-0+".index(c)) * p3
        p3 *= 4
    return n


sector = 0
while drum:
    print("SECTOR %d:" % sector)
    sector += 1
    sec = drum[:135]
    drum = drum[135:]

    words = []
    chars = []
    while sec:
        w = sec[:5]
        sec = sec[5:]
        v = 0
        for c in w:
            v = (v<<8) | c
        s = ""
        for i in range(0,36,2):
            s += as_trit((v>>i)&3)
        s = s[::-1]
        words.append(s)
        for j,tryte in enumerate([s[:9], s[9:]]):
            tryte = to_int(tryte)
            if tryte < 0:
                chars.append("\x00")
                continue
            if tryte < 128:
                chars.append(chr(tryte))
            elif tryte < 256:
                chars.append(charset[tryte-128])
            else:
                chars.append("\x00")
    
    while words and words[-1] == "0" * 18:
        words.pop()

    stringsectors = [3, 10, 11, 12, 13, 14, 27, 28, 29, 30, 31, 32, 33, 34]
    if (sector-1) in stringsectors:
        chars = "".join(chars).split("\x00")[0]
        print("--- as string:")
        print(chars)
        print("---")

    call = -1
    for i,word in enumerate(words):
        if (sector-1) in stringsectors and i < len(chars)//2:
            continue
        for j,tryte in enumerate([word[:9], word[9:]]):
            opcode = tryte[5:8]
            opci = to_int_pack(opcode)

            imm = tryte[:5]
            sm = tryte[8]
            lo5 = tryte[-5:]

            b6 = imm[0]
            b6s = {"-": "X", "0": "Y", "+": "Z"}[b6]
            lo5s = {"-": "X", "0": "Y", "+": "Z"}[lo5[0]]
            lo5s += str(13+to_int(lo5[1:4]))
            if to_int(lo5[-1]) == -1:
                pass
            else:
                lo5s += "." + ["hi", "lo"][to_int(lo5[-1])]
            if lo5s[0] == "Y":
                lo5s = lo5s[1:]
            
            lo = imm[1:]
            ft = to_int(lo)-1
            b5 = imm[1:4]
            wd = b6s + str(to_int(b5) + 13)
            b7 = imm[4]
            if to_int(b7) == -1:
                tr = wd
            else:
                tr = wd + "." + ["hi", "lo"][to_int(b7)]
            
            indir = ""
            if sm == "+":
                indir = "(V+) "
            elif sm == "-":
                indir = "(V-)"

            dis = "unk #%d (0x%x)" % (to_int(tryte), to_int(tryte))
            if opci == 4:
                dis = "%s = drumsector %d" % (b6s, ft)
            elif opci == 5:
                try:
                    dis = "IO.%s %s" % (
                            {"-+++": "audio", "----": "puts", "---0": "gets"}[lo], b6s)
                except KeyError:
                    dis = "IO.broken"
            elif opci == 6:
                dis = "drumsector %d = %s" % (ft, b6s)
            elif opci == 9:
                dis = "shift ACC, %s" % tr
            elif opci == 10:
                dis = "mov %s, ACC" % tr
            elif opci == 16:
                dis = "add V, %s" % tr
            elif opci == 17:
                dis = "mov V, %s" % tr
            elif opci == 18:
                dis = "mov V, pc+%s" % tr
            elif opci == 20:
                dis = "mov %s, V" % tr
            elif opci == 21:
                dis = "jmp 1+%s" % tr
            elif opci == 22:
                dis = "mov %s, pc" % tr
            elif opci == 24:
                dis = "jneg 1+%s" % tr
            elif opci == 25:
                dis = "jzer 1+%s" % tr
            elif opci == 26:
                dis = "jpos 1+%s" % tr
            elif opci == 32:
                dis = "halt"
            elif opci == 33:
                dis = "weirdxor ACC, %s" % tr
            elif opci == 34:
                dis = "mov BETA, %s" % tr
            elif opci == 36:
                dis = "sub ACC, %s" % tr
            elif opci == 37:
                dis = "mov ACC, %s" % tr
            elif opci == 38:
                dis = "add ACC, %s" % tr
            elif opci == 40:
                dis = "mov ACC, %s + ACC*BETA" % tr
            elif opci == 41:
                dis = "mul ACC, %s" % tr
            elif opci == 42:
                dis = "add ACC, %s * BETA" % tr

            if call == 0:
                call += 1
                dis = "  sector: %d" % (to_int(tryte)-1)
                indir = ""
            elif call == 1:
                call += 1
                dis = "  off: %s+1" % (lo5s)
                indir = ""
            else:
                if "jmp 1+Z26.lo" in dis:
                    dis = dis.replace("jmp 1+Z26.lo", "call")
                    call = 0
                dis = dis.replace("jmp 1+X6.hi", "return")
            
            print("%02d.%s: %s.%s.%s [% 5x]   %s%s" % (i, ["hi","lo"][j], imm,opcode,sm,to_int(tryte),indir,dis))
