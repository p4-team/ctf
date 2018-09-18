# Parsletongue (re, 400p)

In the task we get a binary, which after some reversing comes down to the flag verification algorithm:

```python
def validate(inval):
    if len(inval) == 0 or False:
        return False
    if not inval.startswith('TMCTF{'):
        return False
    if not inval.endswith('}'):
        return False
    else:
        length = len(inval)
        inval = inval.split('TMCTF{', 1)[-1].rsplit('}', 1)[0]
        try:
            assert len(inval) + 7 == length
        except:
            return False
    inval = map(ord, inval)
    length = len(inval)
    if length != 24:
        return False
    s = sum(inval)
    if s % length != 9:
        return False
    sdl = s / length
    if chr(sdl) != 'h':
        return False
    inval = [x ^ ord('h') for x in inval]
    ROFL = list(reversed(inval))
    KYRYK = [0] * 5
    QQRTQ = [0] * 5
    KYRYJ = [0] * 5
    QQRTW = [0] * 5
    KYRYH = [0] * 5
    QQRTE = [0] * 5
    KYRYG = [0] * 5
    QQRTR = [0] * 5
    KYRYF = [0] * 5
    QQRTY = [0] * 5
    for i in xrange(len(KYRYK)):
        for j in xrange(len(QQRTQ) - 1):
            KYRYK[i] ^= inval[i + j]
            if QQRTQ[i] + inval[i + j] > 255:
                return False
            QQRTQ[i] += inval[i + j]
            KYRYJ[i] ^= inval[i * j]
            if QQRTW[i] + inval[i * j] > 255:
                return False
            QQRTW[i] += inval[i * j]
            KYRYH[i] ^= inval[8 + i * j]
            if QQRTE[i] + inval[8 + i * j] > 255:
                return False
            QQRTE[i] += inval[8 + i * j]
            KYRYG[i] ^= ROFL[8 + i * j]
            if QQRTR[i] + ROFL[8 + i * j] > 255:
                return False
            QQRTR[i] += ROFL[8 + i * j]
            KYRYF[i] ^= ROFL[i + j]
            if QQRTY[i] + ROFL[i + j] > 255:
                return False
            QQRTY[i] += ROFL[i + j]
        KYRYK[i] += 32
        KYRYJ[i] += 32
        KYRYH[i] += 32
        KYRYG[i] += 32
        KYRYF[i] += 32
        QQRTE[i] += 8
        QQRTY[i] += 1
    for ary in [KYRYK, KYRYJ, KYRYH, KYRYG, KYRYF, QQRTW, QQRTE, QQRTR, QQRTY]:
        for x in ary:
            if x > 255:
                return False
    if ('').join(map(chr, KYRYK)) != 'R) +6':
        return False
    try:
        if ('').join(map(chr, QQRTQ)) != 'l1:C(':
            return False
    except ValueError:
        return False
    if ('').join(map(chr, KYRYJ)) != ' RP%A':
        return False
    if tuple(QQRTW) != (236, 108, 102, 169, 93):
        return False
    if ('').join(map(chr, KYRYH)) != ' L30Z':
        print 'X2'
        return False
    if ('').join(map(chr, QQRTE)) != ' j36~':
        print 's2'
        return False
    if ('').join(map(chr, KYRYG)) != ' M2S+':
        print 'X3'
        return False
    if ('').join(map(chr, QQRTR)) != '4e\x9c{E':
        print 'S3'
        return False
    if ('').join(map(chr, KYRYF)) != '6!2$D':
        print 'X4'
        return False
    if ('').join(map(chr, QQRTY)) != ']PaSs':
        print 'S4'
        return False
    return True
```

Since there is nothing apart form simple XOR, add, sub operations, we can just use Z3 to figure out the answer.
We transpose the verification function into:

```python
import z3


def decryptor():
    E_KYRYK = 'R) +6'
    E_QQRTQ = 'l1:C('
    E_KYRYJ = ' RP%A'
    E_QQRTW = "".join(map(chr, [236, 108, 102, 169, 93]))
    E_KYRYH = ' L30Z'
    E_QQRTE = ' j36~'
    E_KYRYG = ' M2S+'
    E_QQRTR = '4e\x9c{E'
    E_KYRYF = '6!2$D'
    E_QQRTY = ']PaSs'
    s = z3.Solver()
    flag = [z3.BitVec("flag_" + str(i), 8) for i in range(24)]
    added = sum(flag)
    s.add(added == 2505)
    inval = [x ^ ord('h') for x in flag]
    KYRYK, KYRYJ, KYRYH, KYRYG, KYRYF, QQRTW, QQRTE, QQRTR, QQRTY, QQRTQ = convert(inval)
    for i in range(5):
        pass
        s.add(KYRYK[i] == ord(E_KYRYK[i]))
        s.add(KYRYJ[i] == ord(E_KYRYJ[i]))
        s.add(KYRYH[i] == ord(E_KYRYH[i]))
        s.add(KYRYG[i] == ord(E_KYRYG[i]))
        s.add(KYRYF[i] == ord(E_KYRYF[i]))
        s.add(QQRTE[i] == ord(E_QQRTE[i]))
        s.add(QQRTW[i] == ord(E_QQRTW[i]))
        s.add(QQRTR[i] == ord(E_QQRTR[i]))
        s.add(QQRTY[i] == ord(E_QQRTY[i]))
        s.add(QQRTQ[i] == ord(E_QQRTQ[i]))
    print(s.check())
    print(s.model())
    print("".join([chr(int(str(s.model()[var]))) for var in flag]))


def convert(inval):
    ROFL = list(reversed(inval))
    KYRYK = [0] * 5
    QQRTQ = [0] * 5
    KYRYJ = [0] * 5
    QQRTW = [0] * 5
    KYRYH = [0] * 5
    QQRTE = [0] * 5
    KYRYG = [0] * 5
    QQRTR = [0] * 5
    KYRYF = [0] * 5
    QQRTY = [0] * 5
    for i in xrange(len(KYRYK)):
        for j in xrange(len(QQRTQ) - 1):
            KYRYK[i] ^= inval[i + j]
            QQRTQ[i] += inval[i + j]
            KYRYJ[i] ^= inval[i * j]
            QQRTW[i] += inval[i * j]
            KYRYH[i] ^= inval[8 + i * j]
            QQRTE[i] += inval[8 + i * j]
            KYRYG[i] ^= ROFL[8 + i * j]
            QQRTR[i] += ROFL[8 + i * j]
            KYRYF[i] ^= ROFL[i + j]
            QQRTY[i] += ROFL[i + j]
        KYRYK[i] += 32
        KYRYJ[i] += 32
        KYRYH[i] += 32
        KYRYG[i] += 32
        KYRYF[i] += 32
        QQRTE[i] += 8
        QQRTY[i] += 1
    return KYRYK, KYRYJ, KYRYH, KYRYG, KYRYF, QQRTW, QQRTE, QQRTR, QQRTY, QQRTQ
```

And after a moment Z3 says the flag is: `TMCTF{SlytherinPastTheReverser}`
