s="""0; 35.645592;  50.951123; 
20; 35.144068;  50.467725; 
40; 34.729775;  48.204541; 
60; 34.204433;  46.117139; 
80; 33.602623;  44.908643; 
100;    33.162285;  42.337842; 
120;    33.712359;  40.140576; 
140;    33.931410;  38.580518; 
150;    33.894940;  37.745557; 
170;    33.474422;  36.273389; 
190;    35.32583531;    35.663648; 
210;    33.130089;  35.19047214; 
220;    32.409544;  35.141797; 
230;    32.085525;  34.786115; 
"""

x=[]
y1=[]
y2=[]
for line in s.split("\n")[:-1]:
    line=line.split(";")
    x.append(float(line[0]))
    y1.append(float(line[1]))
    y2.append(float(line[2]))


import numpy as np
import matplotlib.pyplot as plt

x=np.asarray(x)
y1=np.asarray(y1)
y2=np.asarray(y2)
def coef(x, y):
    x.astype(float)
    y.astype(float)
    n = len(x)
    a = []
    for i in range(n):
        a.append(y[i])

    for j in range(1, n):

        for i in range(n-1, j-1, -1):
            a[i] = float(a[i]-a[i-1])/float(x[i]-x[i-j])

    return np.array(a) # return an array of coefficient

def Eval(a, x, r):
    x.astype(float)
    n = len( a ) - 1
    temp = a[n]
    for i in range( n - 1, -1, -1 ):
        temp = temp * ( r - x[i] ) + a[i]
    return temp # return the y_value interpolation

print Eval(coef(x,y1), x, 180)
print Eval(coef(x,y2), x, 180)
