import string

s=open("re400.bin").read().strip().decode("hex")[::-1]

sofar=""
cur=len(sofar)

while True:
    print "==============="
    print sofar
    next=s[cur:cur+16]
    poss=[]
    for c in next:
        p=[]
        for i in range(0,128,16):
            cand=chr(ord(c)^i)
            if cand in string.printable:
                p.append(cand)
        poss.append(p)

    for p in poss:
        print repr("".join(p))

    print "Choices:"
    print "-1 Backspace"
    for i,p in enumerate(poss[0]):
        print i,repr(p)

    inp=int(raw_input())
    if inp==-1:
        sofar=sofar[:-1]
        cur-=1
        continue
    cur+=1
    sofar+=poss[0][inp]
