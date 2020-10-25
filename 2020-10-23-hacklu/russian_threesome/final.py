sol = [202, 242, 238, 32, 245, 238, 247, 229, 242, 32, 236, 237, 238, 227, 238, 32, 231, 237, 224, 242, 252, 44, 32, 242, 238, 236, 243, 32, 236, 224, 235, 238, 32, 241, 239, 224, 242, 252, 46, 0]

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

def get(c):
    print(c)
    if c < 128:
        return chr(c)
    else:
        return charset[c-128]

print("".join(get(c) for c in sol))
