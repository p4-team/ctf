

def circuit(inp):
    out=inp[:]
    out[0]=1-out[0]
    out[1]=1
    out[2]=1-out[2]
    out[3]=0
    out[4]=1
    out[5]=out[5]
    out[6]=0
    out[7]=1
    return out

code=open("Prototype.ino").readlines()[106:]

it=0
res=""
for _ in range(11):
    inp=[0]*8
    for i in range(8):
        line=code[it+i]
        if line.find("HIGH")>-1:
            inp[i]=1

    out=circuit(inp)

    it+=8
    it+=1
    for i in range(8):
        line=code[it+i*3]
        if "-" in line:
            out[i]-=1
        elif "+" in line:
            out[i]+=1
        if out[i]!=0 and out[i]!=1:
            print "Uhhh..."
            out[i]=0
    it+=24

    print out
    char=int("".join([str(dig) for dig in out]), 2)
    print chr(char)
    res+=chr(char)

    it+=2
print res
