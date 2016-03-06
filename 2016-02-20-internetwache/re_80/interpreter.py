import string

code = open("priner.tb").read().strip().split(" ")
pointer = 0
memory = [0, 0, 0]
alphabet = " " + string.uppercase

res = ""
for instruction in code:
    print memory, "Pointer:", pointer
    print "Executing:", instruction
    if instruction == "%%":
        pointer = 0
    elif instruction == "#%":
        memory = [1, 1, 1]
    elif instruction == "##":
        memory = [0, 0, 0]
    elif instruction == "%#":
        pointer += 1
    elif instruction == "%++":
        memory[pointer] += 1
    elif instruction[0] == "@":
        mem = memory[len(instruction) - 2]
        c = alphabet[mem]
        res += c
        print "WHOLE OUTPUT:", res
    elif "-" in instruction:
        ins = instruction.split("-")
        lt = len(ins[0]) - 1
        rt = len(ins[1]) - 1
        memory[pointer] = memory[lt] - memory[rt]
    elif "+" in instruction:
        ins = instruction.split("+")
        lt = len(ins[0]) - 1
        rt = len(ins[1]) - 1
        memory[pointer] = memory[lt] + memory[rt]
    elif "&" in instruction:
        ins = instruction.split("&")
        lt = len(ins[0]) - 1
        rt = len(ins[1]) - 1
        memory[pointer] = memory[lt] * memory[rt]
    else:
        print "Unknown instruction encountered: ", instruction
    print ""
