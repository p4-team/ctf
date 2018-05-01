from library import *

if len(sys.argv) > 2:
    n = int(sys.argv[2])
else:
    n = None

i, o, t = load_npz(sys.argv[1])

normalize(t)
smooth(t, 25)
align_fft(t, 35000)
print_corr(t)
i, o, t = filter_corr(i, o, t, 0.4)
print len(t)

show_traces(t)
