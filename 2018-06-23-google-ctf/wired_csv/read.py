import sys
import matplotlib.pyplot as plt

# http://atariage.com/forums/topic/188172-pokey-keyboard-codes/
keys = {
    63: "A",
    62: "S",
    61: "G",
    60: "Cap",
    58: "D",
    57: "H",
    56: "F",
    55: "Great",
    54: "Less",
    53: "8",
    52: "BSp",
    51: "7",
    50: "0",
    48: "9",
    47: "Q",
    46: "W",
    45: "T",
    44: "Tab",
    43: "Y",
    42: "E",
    40: "R",
    39: "Inv",
    38: "Slash",
    37: "M",
    35: "N",
    34: "Dot",
    33: "Spa",
    32: "Comma",
    31: "1",
    30: "2",
    29: "5",
    28: "Esc",
    27: "6",
    26: "3",
    24: "4",
    23: "Z",
    22: "X",
    21: "B",
    20: "F4",
    19: "F3",
    18: "C",
    17: "Hlp",
    16: "V",
    15: "Equal",
    14: "Minus",
    13: "I",
    12: "Ret",
    11: "U",
    10: "P",
    8: "O",
    7: "Aster",
    6: "plus",
    5: "K",
    4: "F2",
    3: "F1",
    2: "Semi",
    1: "J",
    0: "L",
}

t, y, z = [], [], []
datas = []
when = []
for line in open(sys.argv[1]).readlines()[1:]:
    line = line.split(",")
    it = float(line[0])
    w6 = float(line[1])
    w7 = float(line[2])
    t.append(it)
    y.append(w6)
    z.append(w7)
    if w6 < 2.5 and (not when or it - when[-1] > 0.050):
        when.append(it)

print when
bits = [0] * len(when)
for bit in range(6):
    i = 0
    for line in open(sys.argv[1]).readlines()[1:]:
        line = line.split(",")
        it = float(line[3+2*bit])
        if it > when[i]:
            val = int(line[4+2*bit])
            bits[i] |= val << bit
            i += 1
            if i >= len(when): break
    print bit

for bit in bits:
    print keys[bit]
print bits


plt.plot(t, y)
plt.plot(t, z)
plt.show()
