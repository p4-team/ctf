from library import *
import sys

with open(sys.argv[1], "w") as f:
    for i in range(int(sys.argv[2])):

        save_sample(f, chr(int(sys.argv[3], 0))*16)

