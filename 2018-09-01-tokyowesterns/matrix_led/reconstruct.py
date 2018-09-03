import sys
import ast


nums = {}

try:
    for f in sys.argv[1:]:
        for i, line in enumerate(open(f).readlines()):
            no = int(line.split()[0])
            data = ast.literal_eval("[" + line.split("[")[1])
            nums[no] = data
except Exception as e:
    print f, i, repr(line), e



start = min(nums)
end = max(nums)
prev = start
prevdata = [0] * 16
alldata = []
for i in range(start, end):
    if i in nums:
        prev = i
        data = nums[i]
        same = True
        for a, b in zip(data, prevdata):
            if a != b: same = False
        if not same:
            alldata += data
            prevdata = data
    else:
        if i >= prev + 3:
            print i, "missing..."
            prev = i

alldata = "".join(chr(c) for c in alldata)
alldata = alldata[32:]
alldata = "d091577d5889e64724e3a93bc1f8112f".decode("hex") + alldata
alldata = alldata[:-10]
print hex(len(alldata))
open("final", "wb").write(alldata)

from hashlib import md5
print 'TWCTF{{{}}}'.format(md5(open('final', 'rb').read()).hexdigest())
