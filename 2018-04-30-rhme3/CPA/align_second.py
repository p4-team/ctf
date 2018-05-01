from library import *
from lib_attack import *
import sys
import numpy as np

inputs, outputs, traces = parse(sys.argv[1], left=750000, right=800000)

normalize(traces)
smooth(traces, 25)
align(traces, range(-5000, 15000))

save_traces(sys.argv[2], inputs, outputs, traces)
