from library import *

i, o, t = load_npz(sys.argv[1])

normalize(t)
smooth(t, 25)
align_fft(t, 35000)
print_corr(t)
i, o, t = filter_corr(i, o, t, 0.4)
print len(t)

save_npz(sys.argv[2], i, o, t)
