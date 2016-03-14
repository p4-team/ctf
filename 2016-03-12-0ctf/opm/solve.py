
decompilation=open("decomp").read().split("\n")

equations=[]
free=[]

for i in range(16):
    variables={}
    for j in range(16):
        var=decompilation[i*18+j+1].split(" ")[4]
        val=decompilation[i*18+j+1].split(" ")[8][:-2]
        val=int(val)
        val-=72
        val/=4
        variables[var]=val
    assert(len(variables)==16)
    print variables
    eq=decompilation[i*18+17].split(" ")[8:]
    coeffs=eq[::4]
    va=eq[2::4]
    for j, v in enumerate(va):
        va[j]=variables[v]
    eq=[int(x[1]) for x in sorted(zip(va, coeffs))]
    assert(len(eq)==16)
    equations.append(eq)
    
    f=decompilation[290+i*2].split(" ")[-1][:-1]
    free.append(int(f, 16))

print equations
import numpy as np
A=np.matrix(equations)
B=np.matrix(free)

print A
print B.T
print ""
sol=A.I*B.T
print sol

arr=[int(x+0.25) for x in list(np.array(sol.T)[0])]
print arr
print "".join([chr(c) for c in arr])[::-1]
