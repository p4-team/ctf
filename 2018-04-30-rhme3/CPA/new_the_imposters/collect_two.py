from library import *
import sys

# python collect_same.py traces.npz 10 0x41 0x42

n = int(sys.argv[2])
inputs1 = np.full((n, 16), int(sys.argv[3], 0), dtype=np.uint8)
inputs2 = np.full((n, 16), int(sys.argv[4], 0), dtype=np.uint8)
inputs = np.concatenate((inputs1, inputs2))
np.random.shuffle(inputs)
collect(sys.argv[1], inputs)
