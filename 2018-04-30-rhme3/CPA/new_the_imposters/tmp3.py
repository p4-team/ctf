from library import *

if len(sys.argv) > 2:
    n = int(sys.argv[2])
else:
    n = None

i, o, t = load_npz(sys.argv[1], n)
t = t[:, 395000:398000]
align_fft(t, 500)
show_traces(t)
