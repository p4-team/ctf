

lines = open("602.txt").readlines()

def try_parse(data):
    try:
        data = data.split()
        assert len(data[0]) == 2
        op = int(data[0], 16)
        rest = data[1:]
        return True, op, rest
    except:
        return False, "", ""

def save(opname, op, args):
    print opname + "|" + hex(op) + "|" + " ".join(args)

for i, line in enumerate(lines):
    if line == "Opcode:\n":
        opx = lines[i-1].strip().split()[0]

        for j in range(i, i+10):
            data = lines[j].strip()
            ok, op, args = try_parse(data)
            if ok:
                save(opx, op, args)
                break

