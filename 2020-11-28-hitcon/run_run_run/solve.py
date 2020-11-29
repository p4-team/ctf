magic = [98,32,84,253,217,18,92,22,112,138,147,46,168,229,31,149,72,94,191,124,21,176,10,104,154,213,235,25,237,61,18,15]
target = [3**i for i in range(32)]

def solve(t):
    v2 = 1
    v3 = 1
    v4 = 1
    for i in range(t):
        v5 = (2*v2 + v3 + 7*v4) % 31337
        v4 = v3
        v3 = v2
        v2 = v5
    return v2&0xff


flag = ""
for m, t in zip(magic, target):
    c = solve(t) ^ m
    flag += chr(c)
    print(flag)
    
