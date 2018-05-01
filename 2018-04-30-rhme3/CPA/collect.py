from library import *
import sys

with open(sys.argv[1], "w") as f:
    for i in range(int(sys.argv[2])):
        while True:
            inp = "".join(chr(random.randint(0, 255)) for _ in range(16))
            if "\n" not in inp:
                break

        save_sample(f, inp)

