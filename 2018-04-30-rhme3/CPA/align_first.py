from library import *
from lib_attack import *
import sys
import numpy as np

inputs, outputs, traces = parse(sys.argv[1], left=650000, right=700000)

normalize(traces)
smooth(traces, 25)
align(traces, range(-5000, 15000))

if 1:
    traces = traces[:,0:40000]
    normalize(traces)
    align(traces, range(-50, 50))

    if 0:
        traces = traces[:, 8000:9500]
        normalize(traces)
        align(traces, range(-20, 20))

save_traces(sys.argv[2], inputs, outputs, traces)
