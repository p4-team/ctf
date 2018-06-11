import ebcdic
import sys

data = open("data.txt", "r").read().split()

for i in range(0,len(data),2):
    a = ((int(data[i],2) >> 1) << 4) + (int(data[i+1],2) >> 1)
    sys.stdout.write(chr(a).decode("cp500"))
