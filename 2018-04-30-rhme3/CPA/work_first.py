from library import *
from lib_attack import *
import sys
import numpy as np

inputs, outputs, traces_orig = parse(sys.argv[1])

j = 0

flag = [0] * 16
for place in range(7620, 32500, 1626):
    traces = np.copy(traces_orig[:, place-400:place+400])
    normalize(traces)
    align(traces, range(-50, 50))
    traces = traces[:, :-40]

    print "Flag so far", flag

    #show_traces(traces)
    i = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15][j]
    j += 1
    fb = find_byte(inputs, outputs, traces, i)
    for a in fb[:5]:
        print a
    print 
    if fb[0][0] / fb[1][0] > 1.3:
        print "\t\tFOUND BYTE %d: %02x" % (i, fb[0][1])
        flag[i] = fb[0][1]

print flag
