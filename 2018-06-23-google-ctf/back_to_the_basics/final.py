

s = """
2010 V =  0.6666666666612316235641 -  0.00000000023283064365386962890625 : G =  0
2020 BA =  ASC ( MID$ (P$, 1, 1) )
2021 BB =  ASC ( MID$ (P$, 2, 1) )
2025 P0 =  0:P1 =  0:P2 =  0:P3 =  0:P4 =  0:P5 =  0:P6 =  0:P7 =  0:P8 =  0:P9 =  0:PA =  0:PB =  0:PC =  0
2030 IF  BA AND  1 THEN  P0 =  0.062500000001818989403545856475830078125
2031 IF  BA AND  2 THEN  P1 =  0.0156250000004547473508864641189575195312
2032 IF  BA AND  4 THEN  P2 =  0.0039062500001136868377216160297393798828
2033 IF  BA AND  8 THEN  P3 =  0.0009765625000284217094304040074348449707
2034 IF  BA AND  16 THEN  P4 =  0.0002441406250071054273576010018587112427
2035 IF  BA AND  32 THEN  P5 =  0.0000610351562517763568394002504646778107
2036 IF  BA AND  64 THEN  P6 =  0.0000152587890629440892098500626161694527
2037 IF  BA AND  128 THEN  P7 =  0.0000038146972657360223024625156540423632
2040 IF  BB AND  1 THEN  P8 =  0.0000009536743164340055756156289135105908
2031 IF  BB AND  2 THEN  P9 =  0.0000002384185791085013939039072283776477
2032 IF  BB AND  4 THEN  PA =  0.0000000596046447771253484759768070944119
2033 IF  BB AND  8 THEN  PB =  0.000000014901161194281337118994201773603
2034 IF  BB AND  16 THEN  PC =  0.0000000037252902985703342797485504434007
2050 K =  V +  P0 +  P1 +  P2 +  P3 +  P4 +  P5 +  P6 +  P7 +  P8 +  P9 +  PA +  PB +  PC
2060 G =  0.671565706376017
"""

alllines = open("raw_code").readlines()
allchars = {}

for i in range(len(alllines)):
    ln  = alllines[i]
    if "V =  " in ln:
        start = i
        continue
    elif "0 G =  " in ln:
        end = i
    else:
        continue
    s = alllines[start:end+1]

#s = s.splitlines()[1:]
    for i, line in enumerate(s):
        if "P0" in line:
            n = i
            break

    line = s[0].split()
    v = float(line[3])
    try:
        v -= float(line[5])
    except Exception:
        pass

    name2char = {"BX": 31}
    for line in s[1:n]:
        line = line.split()
        name = line[1]
        nx = int(line[7].strip(","))
        name2char[name] = nx

    exp = float(s[-1].split()[-1])
    eqs = []
    for line in s[n+1:-2]:
        line = line.split()
        name = line[2]
        bit = int(line[4])
        val = float(line[-1])
        eqs.append((name, bit, val))

    mn, mni, mn2 = 1e9, None, 1e9
    for i in range(1<<len(eqs)):
        s = v
        for j in range(len(eqs)):
            if i & (1<<j):
                s += eqs[j][2]
        s -= exp
        s = abs(s)
        if s < mn:
            mn, mni, mn2 = s, i, mn
        elif s < mn2:
            mn2 = s

    print mn, mni, mn2, mn/mn2

    for i, eq in enumerate(eqs):
        allchars[(name2char[eq[0]], eq[1])] = (mni>>i) & 1

mystr = [0] * 40

for k in sorted(allchars):
    print k, allchars[k]
    i, b = k
    mystr[i] |= allchars[k] * b

mystr = "".join([chr(c) for c in mystr])
print mystr





