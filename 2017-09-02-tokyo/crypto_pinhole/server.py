# Python 3
from signal import alarm
from Crypto.Util.number import *
import Crypto.Random as Random

with open("secretkey", "r") as f:
    sk1 = int(f.readline(), 16)
    sk2 = int(f.readline(), 16)

with open("publickey", "r") as f:
    n = int(f.readline(), 16)
    n2 = int(f.readline(), 16)
    g = int(f.readline(), 16)

cbits = size(n2)
mbits = size(n)
b = mbits//2

def L(x, n):
    return (x - 1) // n
    
def decrypt(c, sk1, sk2, n, n2):
    return L(pow(c, sk1, n2), n) * sk2 % n

def run(fin, fout):
    alarm(1200)
    try:
        while True:
            line = fin.readline()[:4+cbits//4]
            ciphertext = int(line, 16) # Note: input is HEX
            m = decrypt(ciphertext, sk1, sk2, n, n2)
            fout.write(str((m >> b) & 1) + "\n")
            fout.flush()
    except:
        pass

if __name__ == "__main__":
    run(sys.stdin, sys.stdout)
