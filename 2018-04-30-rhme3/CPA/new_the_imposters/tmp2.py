from library import *

if len(sys.argv) > 2:
    n = int(sys.argv[2])
else:
    n = None

i, o, t = load_npz(sys.argv[1], n)
t = t[:, 436000:465000]
align_fft(t, 1000)

inda = [j for j in range(len(i)) if i[j][0] == 0xaa]
indb = [j for j in range(len(i)) if i[j][0] != 0xaa]

t01 = t
ts = []

for ind in [inda, indb]:
    t1 = t01[ind]
    t1 = t1[:12]
    ts.append(t1)

print len(ts[0]), len(ts[1])
smooth(ts[0], 50)
smooth(ts[1], 50)
show_red_green(ts[0], ts[1])
