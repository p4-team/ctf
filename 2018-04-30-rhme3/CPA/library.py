import subprocess
import serial, sys
import time, random
import matplotlib.pyplot as plt
import numpy as np

def enc(e):
    s = serial.Serial("/dev/ttyUSB0", 115200, timeout = 2)
    stuff = "\xae" + e + "\n"
    s.write(stuff)
    rd = s.read(18)
    print repr(stuff), repr(rd)
    assert rd == stuff
    return s.read(16)

def wait(p, t):
    t0 = time.time()
    while time.time() - t0 < t:
        if p.poll() is not None:
            return
        time.sleep(0.1)
    raise Exception("Timeout")

def parse_sigrok(fname):
    def get(line):
        f = float(line.split()[1])
        if "mV" in line:
            return f/1e3
        return f
    data = open(fname).readlines()[1:-1]
    return [get(line) for line in data]

def save_sample(f, inp):
    p = subprocess.Popen(["sigrok-cli", "--driver", "rigol-ds", "--frames", "1",
        "-o", "/tmp/test", "-C", "CH1", "-O", "analog", "-c", "data_source=Memory"])
    time.sleep(1)
    out = enc(inp)
    s = inp.encode("hex") + "\n" + out.encode("hex") + "\n"
    print s
    wait(p, 30)
    data = parse_sigrok("/tmp/test")
    s += ",".join(str(x) for x in data) + "\n"
    f.write(s)
    f.flush()

def save_traces(fname, inputs, outputs, traces):
    with open(fname, "w") as f:
        for i, o, t in zip(inputs, outputs, traces):
            i = "".join(chr(c) for c in i)
            o = "".join(chr(c) for c in o)
            s = i.encode("hex") + "\n" + o.encode("hex") + "\n"
            s += ",".join(str(x) for x in t) + "\n"
            f.write(s)
            f.flush()


def parse(fname, n=999999, left=None, right=None):
    with open(fname) as f:
        inputs, outputs, traces = [], [], []
        for i, line in enumerate(f.xreadlines()):
            if i % 3 == 0:
                inputs.append([ord(c) for c in line.strip().decode("hex")])
            elif i % 3 == 1:
                outputs.append([ord(c) for c in line.strip().decode("hex")])
            else:
                traces.append([float(c) for c in line.split(",")])
                if left is not None:
                    traces[-1] = traces[-1][left:right]
            if len(traces) == n:
                break
        traces = np.array(traces)
        return inputs, outputs, traces

def show_traces(traces):
    for t in traces:
        plt.plot(t)
    plt.show()

def show_red_green(red, green):
    for t in red:
        plt.plot(t, "r")
    for t in green:
        plt.plot(t, "g")
    plt.show()

def normalize(traces):
    for t in traces:
        t -= np.mean(t)
        t /= np.std(t)

def smooth(traces, r):
    for i, t in enumerate(traces):
        traces[i] = np.convolve(t, np.ones(r))[:len(t)]

def align(traces, shifts, verbose=True, max_shift=None):
    t0 = traces[0]
    res = [0]
    for i in range(1, len(traces)):
        if verbose:
            print i, "/", len(traces), "-", 
        trace = traces[i]
        best, bests = 1e18, -1
        for shift in shifts:
            if shift < 0:
                diff = t0[-shift:] - trace[:shift]
            elif shift == 0:
                diff = t0 - trace
            else:
                diff = t0[:-shift] - trace[shift:]

            s = np.mean(diff**2)
            if s < best:
                best, bests = s, shift

        if verbose:
            print bests
        res.append(bests)

    resx = res[:]
    mn = min(res)
    res = [s - mn for s in res]

    for i in range(len(traces)):
        shifted = traces[i][res[i]:]
        zeros = np.zeros(res[i])
        shifted = np.concatenate((shifted, zeros))
        traces[i] = shifted

    if max_shift is not None:
        traces = traces[[i for i in range(len(traces)) if abs(resx[i]) < max_shift]]
    return traces
