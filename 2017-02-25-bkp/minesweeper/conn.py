from pwn import *
import math

#r=remote("localhost", 8001)
r=remote("54.202.194.91", 65535)

def setGates(gates, final=False):
    s=""
    s+=struct.pack(">H", len(gates))
    for gate in gates:
        # X, Y, Z, Hadamard, rotate by 90, Measure
        if gate[0]!="R":
            type, wire, arg = gate
        else:
            type, wire, arg, ang = gate
        ch=0x80*wire
        if type=='M':
            ch|=arg # Bomb number
        else:
            ch|=0x70
            ch+=0x8*arg # Controlled?
            ch|={"X": 1, "Y": 2, "Z": 3, "H": 4, "9": 5, "R": 6}[type]
        s+=chr(ch)
        if type=="R":
            s+=struct.pack("<d", ang)
    r.send(s)
    if not final:
        return ord(r.recv(1))

if 0:
    xxx=[
        ("H", 0, 0),
        ("H", 1, 0),
        ("R", 0, 1, 0.01),
        ("X", 0, 1),
        ("R", 0, 1, -0.01),
        ("H", 0, 1),
        ("9", 0, 0)
    ]

    gates=[
        ("H", 0, 0),
        ("X", 1, 0),
    ]

    for i in range(0, 100):
        gates+=[
            ("R", 0, 0, 0.01),
            ("X", 0, 0),
            ("R", 0, 0, -0.01),
            ("H", 0, 0),
            ("R", 0, 0, math.atan2(i**0.5, (1+i/100.)**0.5)),
            ("9", 0, 0),
            ("H", 0, 0),
        ]

def test(idx):
    num=500
    gates=[
            ("H", 0, 0),
            ("R", 0, 0, math.pi/num),
            ("H", 0, 0),
            ("M", 0, idx),
    ]*num
    return setGates(gates)

bombs=[]
for i in range(14*8):
    print "Testing",i,"/",14*8
    bombs.append(test(i))
    # 0 - bomb, 1 - clear
setGates([], True)
print bombs
s=""
for i in range(14):
    b=0
    for j in range(8):
        if bombs[i*8+j]==0:
            b|=1<<(7-j)
    s+=chr(b)
r.send(s)
print r.recv()
