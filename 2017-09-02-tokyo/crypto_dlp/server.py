# Python 3
from signal import alarm
from Crypto.Util.number import *

p = 160634950613302858781995506902938412625377360249559915379491492274326359260806831823821711441204122060415286351711411013883400510041411782176467940678464161205204391247137689678794367049197824119717278923753940984084059450704378828123780678883777306239500480793044460796256306557893061457956479624163771194201
g = 2

bits = size(p)

with open("flag", "r") as f:
    flag = f.readline().strip().encode("latin1")
    m = bytes_to_long(flag)

def run(fin, fout):
    alarm(1200)
    try:
        while True:
            line = fin.readline()[:4+bits//4]
            s = int(line, 16) # Note: input is HEX
            c = pow(g, m ^ s, p)
            fout.write(hex(c) + "\n")
            fout.flush()
    except:
        pass

if __name__ == "__main__":
    run(sys.stdin, sys.stdout)
