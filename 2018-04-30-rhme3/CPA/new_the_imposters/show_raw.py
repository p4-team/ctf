from library import *

if len(sys.argv) > 2:
    n = int(sys.argv[2])
else:
    n = None

i, o, t = load_npz(sys.argv[1], n)
show_traces(t)
