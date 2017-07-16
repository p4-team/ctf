from rc4 import RC4

L = 0x24+8

key = [ord(c) for c in "error: _ptr is not null"]
r = RC4(key)
s = open("crackme3000", "rb").read()
f = s.find("5f6897286932".decode("hex"))
d = [ord(c) for c in s[f:f+L]]
x = []
for c in d:
    x.append(c ^ r.next())

e = "No such file or directory"

flag = "c"
for i in range(1, L):
    flag += chr(ord(e[i % len(e)]) ^ x[i] ^ ord(flag[-1]))

print flag

