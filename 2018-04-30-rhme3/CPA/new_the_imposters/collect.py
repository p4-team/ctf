from library import *
import sys

n = int(sys.argv[2])
inputs = np.zeros((n, 16), dtype=np.uint8)

for i in range(n):
    while True:
        inp = np.array([random.randint(0, 255) for _ in range(16)])
        if ord("\n") not in inp:
            break
    inputs[i] = inp

collect(sys.argv[1], inputs)
