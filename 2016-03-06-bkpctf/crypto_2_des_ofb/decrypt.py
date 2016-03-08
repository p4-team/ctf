from Crypto.Cipher import DES

ct=open("ciphertext","rb").read()
pt=[]
for i in range(16):
    counts=[0]*256
    for c in ct[i::16]:
        counts[ord(c)]+=1
    mx=0
    best=0
    for k, val in enumerate(counts):
        if val>mx:
            mx=val
            best=k
    if i==6:
        best=0x53
    if i==13:
        best=0x16
    if i==15:
        best=0x18
    print "Key:", best
    ptt=[]
    for c in ct[i::16]:
        ptt.append(chr(ord(c)^best^ord(" ")))
    pt.append("".join(ptt))

res=[]
for i in range(len(pt[0])):
    for j in range(16):
        try:
            res.append(pt[j][i])
        except:
            pass
print "".join(res)

