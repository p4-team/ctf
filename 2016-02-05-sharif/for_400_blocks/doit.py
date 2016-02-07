import zlib, itertools, binascii

s=[]
q=open("blobs","rb").read().split("\n")[:-1]
for w in q:
    w=w.split("'")[1]
    s.append(binascii.unhexlify(w))
print len(s)

i=0
for perm in itertools.permutations(s):
    w="".join(perm)
    try:
        q=zlib.decompress(w)
        print perm
    except:
        pass
    i+=1
    if i%10000==0:
        print i
        for j in perm:
            print repr(j)[:3],
        print ""
