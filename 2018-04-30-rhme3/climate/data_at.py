import sys, string

def is_printable(s):
    for c in s:
        if c not in string.printable:
            return False
    return True

i = int(sys.argv[1], 0)
if len(sys.argv) > 2:
    l = int(sys.argv[2], 0)
else:
    l = 256
s = open("climate.bin", "rb").read()

i -= 0x2000
i += 0x12612

data = s[i:][:l]
print data.encode("hex")
print repr(data)
data = data.split("\x00")[0]

if is_printable(data):
    print "\n\n"
    print data
