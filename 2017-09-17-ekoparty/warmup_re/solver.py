import gdb
import codecs
import string

flag = []
gdb.execute("break *0x4009dc")
gdb.execute("r <<< $(echo 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')")
for i in range(28):
    for i in range(2):
        gdb.execute("n")
    addr = int(str(gdb.parse_and_eval("$eax")),16)
    for i in range(2):
        gdb.execute("n")
    value = chr(int(str(gdb.parse_and_eval("$eax")),16))
    flag.append((addr, value))
    gdb.execute("set $dl = $al")
    for i in range(2):
        gdb.execute("n")
gdb.execute("c")
flag = sorted(flag, key=lambda x: x[0])
print("".join([c[1] for c in flag]))