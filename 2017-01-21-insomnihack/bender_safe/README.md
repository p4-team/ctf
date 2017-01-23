# Bender Safe (re, 50 points)

Binary provided in challenge is 32bit MIPS, which is a bit unusual, and makes reversing harder.

We can connect to challenge server, but it wants us to provide some OTP key:

    $ nc bender_safe.teaser.insomnihack.ch 31337
    Welcome to Bender's passwords storage service
    Here's your OTP challenge : 
    IMYTSAAAUI87YIQU

After a while of reverse-engineering, we have found that there is only one function that matter (named aptly `validate`).

Checks are performed one-by-one, but characters are checked out-of-order (so naively bruteforcing password by tracing program and counting instructions will not work).

Checks was rather trivial, so instead of trying to be smart, we've just reverse engineered everything the traditional way (using IDA Pro + qemu remote debugger), and came out with this OTP generator (challenge in argv[1]):

```python
import sys

mychars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

ss = sys.argv[1]

out = ''

out += ss[0]

out += ss[15]

if ord(ss[7]) >= 65:
    out += chr(ord(ss[7]) ^ 0x20)
else:
    out += chr(ord(ss[7]) ^ 0x40)

if ord(ss[3]) >= 65:
    ndx = mychars.find(ss[3])
    ndx = (ndx + 10) % len(mychars)
    out += mychars[ndx]
else:
    ndx = mychars.find(ss[3])
    ndx = (ndx - 10) % len(mychars)
    out += mychars[ndx]

if ord(ss[4]) >= 65:
    ndx = mychars.find(ss[4])
    ndx = (ndx + 10) % len(mychars)
    out += mychars[ndx]
else:
    ndx = mychars.find(ss[4])
    ndx = (ndx - 10) % len(mychars)
    out += mychars[ndx]

v25 = ord(ss[1]) - ord(ss[2])
if v25 >= 0:
    v26 = v25
else:
    v26 = -v25
out += mychars[v26 % (len(mychars) - 1)]

v25 = ord(ss[5]) - ord(ss[6])
if v25 >= 0:
    v26 = v25
else:
    v26 = -v25
out += mychars[v26 % (len(mychars) - 1)]

if ord(ss[8]) >= 65:
    out += chr(ord(ss[8]) ^ 0x20)
else:
    out += chr(ord(ss[8]) ^ 0x40)

print out
```
