

functions = ["none"] * 150
exceptions = open("exceptions").readlines()


for i, line in enumerate(open("exc2").readlines()):
    line = line.strip()
    if i % 3 == 1:
        fun = line.split("(")[0].split()[-1]
    elif i % 3 == 2:
        line = int(line.split("[")[1].split("]")[0])
        functions[line] = fun

for i, f in enumerate(functions):
    lines = []
    for line in exceptions:
        if f in line:
            lines.append(line)

    if lines:
        line = lines[0].strip().split()[4]
    else:
        line = "none"

    if line.startswith("sub_"):
        line = int(line.split("_")[1], 16)
        print "MakeName(", hex(line), ", ", "'opcode_"+str(i)+ "')"
    else:
        print "#", i, f, line
