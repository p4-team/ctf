from library import *

if len(sys.argv) > 2:
    n = int(sys.argv[2])
else:
    n = None

i, o, t = load_npz(sys.argv[1], n)

t1 = t[0][261968:][:2000]
t2 = t[0][286991+57:][:2000]

show_traces([t1, t2])
