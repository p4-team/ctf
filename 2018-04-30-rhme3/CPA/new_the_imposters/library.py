import subprocess
import serial, sys
import time, random
import matplotlib.pyplot as plt
import numpy as np
from scipy import fftpack

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
    return np.array([get(line) for line in data], dtype=np.float32)

def get_sample(inp):
    p = subprocess.Popen(["sigrok-cli", "--driver", "rigol-ds", "--frames", "1",
        "-o", "/tmp/test", "-C", "CH1", "-O", "analog", "-c", "data_source=Memory"])
    time.sleep(1)
    out = enc("".join(chr(c) for c in inp))
    out = np.array([ord(c) for c in out])

    wait(p, 30)
    data = parse_sigrok("/tmp/test")
    return out, data

def save_npz(fname, inputs, outputs, traces):
    np.savez_compressed(fname, inputs=inputs, outputs=outputs, traces=traces)

def collect(fname, inputs):
    assert type(inputs) == np.ndarray
    n = len(inputs)
    outputs = np.zeros((n, 16), dtype=np.uint8)
    traces = np.zeros((n, 1048576), dtype=np.float32)

    for i, inp in enumerate(inputs):
        print i, "/", len(inputs)
        out, dat = get_sample(inp)
        outputs[i] = out
        traces[i] = dat

    save_npz(fname, inputs, outputs, traces)

def load_npz(fname, n=None):
    arr = np.load(fname)
    inputs, outputs, traces = arr["inputs"], arr["outputs"], arr["traces"]
    if n is not None:
        inputs = inputs[:n]
        outputs = outputs[:n]
        traces = traces[:n]
    return inputs, outputs, traces

def show_traces(traces, legend = False):
    for i, t in enumerate(traces):
        plt.plot(t, label = str(i))
    
    if legend:
        plt.legend()
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

def align_fft(traces, maxshift, add=None, verbose=True):
    t0 = traces[0]
    T0 = fftpack.fft(t0)
    shifts = []
    for t in traces:
        T = -fftpack.fft(t).conjugate()
        ii = fftpack.ifft(T0*T)
        ii[maxshift:-maxshift] = 0

        shift = -np.argmin(ii)
        if shift < -len(t) / 2:
            shift += len(t)
        shifts.append(shift)

    for i, s in enumerate(shifts):
        print "%+06d" % s,
        if i % 10 == 9:
            print
    print

    if add is None:
        add = -min(shifts)

    shifts = [s + add for s in shifts]

    for i in range(len(traces)):
        shifted = traces[i][shifts[i]:]
        zeros = np.zeros(shifts[i])
        shifted = np.concatenate((shifted, zeros))
        traces[i] = shifted


def get_corr(a, b):
    return np.corrcoef((a, b))[0][1]


def filter_corr(inputs, outputs, traces, min_corr):
    med = np.median(traces, axis=0)
    ind = [i for i, t in enumerate(traces) if get_corr(t, med) > min_corr]
    return inputs[ind], outputs[ind], traces[ind]


def print_corr(traces):
    med = np.median(traces, axis=0)
    corr = [get_corr(t, med) for t in traces]
    for i, s in enumerate(corr):
        print "%+1.3f" % s,
        if i % 10 == 9:
            print
    print
