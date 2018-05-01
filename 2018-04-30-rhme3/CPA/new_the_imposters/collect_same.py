from library import *
import sys

# python collect_same.py traces.npz 10 0x41

n = int(sys.argv[2])
inputs = np.full((n, 16), int(sys.argv[3], 0), dtype=np.uint8)
collect(sys.argv[1], inputs)
