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
        print(v2, v3, v4)
    return v2

def powmod(mat, n):
    if n == 1:
        return mat
    half = powmod(mat, n//2)
    full = np.matmul(half, half)
    if n&1:
        full = np.matmul(full, mat)
    return full % 31337

import numpy as np
mat = np.array([[2, 1, 7], [1, 0, 0], [0, 1, 0]])
vals = np.array([1, 1, 1])

for t in range(1, 10):
    print("Naive:", solve(t))
    print("Clever:", np.matmul(powmod(mat, t), vals))

flag = ""
for m, t in zip(magic, target):
    #c = solve(t) ^ m
    c = (np.matmul(powmod(mat, t), vals)[0]%31337) ^ m
    flag += chr(c&0xff)
    print(flag)
    
