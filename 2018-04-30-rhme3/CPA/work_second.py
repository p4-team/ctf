from library import *
from lib_attack import *
import sys
import numpy as np
from pyaes.aes import *

inputs, outputs, traces_orig = parse(sys.argv[1])

# show_traces(traces_orig)

key_0 = [228, 123, 155, 110, 8, 116, 222, 158, 59, 117, 91, 119, 170, 23, 182, 148]
key_0 = [
    [key_0[0], key_0[1], key_0[2], key_0[3]],
    [key_0[4], key_0[5], key_0[6], key_0[7]],
    [key_0[8], key_0[9], key_0[10], key_0[11]],
    [key_0[12], key_0[13], key_0[14], key_0[15]],
]

for i, inp in enumerate(inputs):
    inp = [
        [inp[0], inp[1], inp[2], inp[3]],
        [inp[4], inp[5], inp[6], inp[7]],
        [inp[8], inp[9], inp[10], inp[11]],
        [inp[12], inp[13], inp[14], inp[15]],
    ]
    inp = AddRoundKey(inp, key_0)
    inp = SubBytes(inp)
    inp = ShiftRows(inp)
    inp = MixColumns(inp)
    all = []
    for x in inp:
        all += x
    inputs[i] = all

j = 0

flag = [0] * 16
for place in range(9734, 33996+800, 1626):
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
