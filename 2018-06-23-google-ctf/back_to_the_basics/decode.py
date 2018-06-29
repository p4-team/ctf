

s = """
2004 ES =  03741 : EE =  04981 : EK =  148
2004 ES =  05363 : EE =  06632 : EK =  152
2004 ES =  07014 : EE =  08219 : EK =  165
2004 ES =  08601 : EE =  09868 : EK =  184
2004 ES =  10250 : EE =  11483 : EK =  199
2004 ES =  11865 : EE =  13107 : EK =  240
2004 ES =  13489 : EE =  14760 : EK =  249
2004 ES =  15142 : EE =  16351 : EK =  132
2004 ES =  16733 : EE =  17975 : EK =  186
2004 ES =  18360 : EE =  19633 : EK =  214
2004 ES =  20020 : EE =  21265 : EK =  245
2004 ES =  21652 : EE =  22923 : EK =  203
2004 ES =  23310 : EE =  24584 : EK =  223
2004 ES =  24971 : EE =  26178 : EK =  237
2004 ES =  26565 : EE =  27837 : EK =  192
2004 ES =  28224 : EE =  29471 : EK =  157
2004 ES =  29858 : EE =  31101 : EK =  158
2004 ES =  31488 : EE =  32761 : EK =  235
2004 ES =  33148 : EE =  34367 : EK =  143
"""
# 2005 FOR  I =  ES TO  EE : K =  ( PEEK (I) +  EK ) AND  255 : POKE  I, K : NEXT  I

f = open("crackme.prg", "rb").read()
for line in s.splitlines()[1:]:
    s = line.split()
    es = int(s[3])
    ee = int(s[7])
    ek = int(s[11])

    es -= 0x800 - 1
    ee -= 0x800 - 2

    def dec(s, n):
        return "".join(chr((ord(c) + n)&0xff) for c in s)

    f = f[:es] + dec(f[es:ee], ek) + f[ee:]
open("new.prg", "wb").write(f)
