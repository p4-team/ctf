from library import *
import sys
import numpy as np

SZ = 10

inputs, outputs, traces1 = parse(sys.argv[1], SZ, left = 600000, right=700000)
inputs, outputs, traces2 = parse(sys.argv[2], SZ, left = 600000, right=700000)

traces = np.concatenate((traces1, traces2))

normalize(traces)

for i in range(len(traces)):
    traces[i] = np.convolve(traces[i], np.ones(25))[:len(traces[i])]

align(traces, range(-5000, 15000))

if 1:
    traces = traces[:,72500:78000]
    align(traces, range(-250, 250))

    if 0:
        traces = traces[:,300:1200]
        align(traces, range(-10, 10))

tr1 = np.mean(traces[:SZ], 0)
tr1s = np.std(traces[:SZ], 0)
tr2 = np.mean(traces[SZ:], 0)
tr2s = np.std(traces[SZ:], 0)

# show_red_green([tr1-tr1s, tr1+tr1s], [tr2-tr2s, tr2+tr2s])
show_red_green(traces[:SZ], traces[SZ:])
