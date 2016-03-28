import struct, string

data=open("dump","rb").read()
events=[]
for i in range(len(data)/24):
    ev=data[i*24:i*24+24]
    time=ev[:16]
    ev=ev[16:]
    tp=ev[:2]
    ev=ev[2:]
    code=ev[:2]
    ev=ev[2:]
    val=ev
    events.append( ( struct.unpack("<H",tp)[0], struct.unpack("<H",code)[0], struct.unpack("<I",val)[0] ) )

EV_KEY=1
key_events=[]
for event in events:
    if event[0]==EV_KEY:
        key_events.append(event)

keys=open("keys.h").readlines()
keydata={}
for line in keys:
    ln=line.split("\t")
    name=ln[0].split(" ")[-1]
    code=int(ln[-1])
    keydata[code]=name

shift=0
full=""
for event in key_events:
    if event[2]==0:
        print "Released",
    elif event[2]==1:
        print "---> Pressed",
    else:
        print "???",
    code=event[1]
    print keydata[code]
    if keydata[code]=="KEY_RIGHTSHIFT" or keydata[code]=="KEY_LEFTSHIFT":
        if event[2]==0:
            shift-=1
        else:
            shift+=1
    elif event[2]==1:
        if len(keydata[code])==5:
            c=keydata[code][-1]
            if shift==0:
                c=string.lower(c)
            full+=c
        elif keydata[code]=="KEY_SPACE":
            full+=" "
        else:
            keydata[code]+="["+keydata[code]+"]"

print full
