from library import *
from collections import defaultdict

if len(sys.argv) > 2:
    n = int(sys.argv[2])
else:
    n = None

i, o, t = load_npz(sys.argv[1])


if 0:
    t = t[:, 100:1600]
    normalize(t)
    align_fft(t, 200)

    if 0:
        t = t[:, 4500:6500]
        normalize(t)
        align_fft(t, 100)

d = defaultdict(list)
for j, inp in enumerate(i):
    inp = "".join(chr(c) for c in inp)
    d[inp].append(j)

tlist = []
for indices in d.values():
    tlist.append(indices)

t1 = t[tlist[0]]
t2 = t[tlist[1]]

show_red_green(t1, t2)
