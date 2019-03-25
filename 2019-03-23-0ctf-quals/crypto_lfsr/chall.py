from secret import init1,init2,init3,FLAG
import hashlib
assert(FLAG=="flag{"+hashlib.sha256(init1+init2+init3).hexdigest()+"}")

class lfsr():
    def __init__(self, init, mask, length):
        self.init = init
        self.mask = mask
        self.lengthmask = 2**(length+1)-1

    def next(self):
        nextdata = (self.init << 1) & self.lengthmask 
        i = self.init & self.mask & self.lengthmask 
        output = 0
        while i != 0:
            output ^= (i & 1)
            i = i >> 1
        nextdata ^= output
        self.init = nextdata
        return output

def combine(x1,x2,x3):
    return (x1*x2)^(x2*x3)^(x1*x3)

if __name__=="__main__":
    l1 = lfsr(int.from_bytes(init1,"big"),0b100000000000000000000000010000000000000000000000,48)
    l2 = lfsr(int.from_bytes(init2,"big"),0b100000000000000000000000000000000010000000000000,48)
    l3 = lfsr(int.from_bytes(init3,"big"),0b100000100000000000000000000000000000000000000000,48)

    with open("keystream","wb") as f:
        for i in range(8192):
            b = 0
            for j in range(8):
                b = (b<<1)+combine(l1.next(),l2.next(),l3.next())
            f.write(chr(b).encode())
