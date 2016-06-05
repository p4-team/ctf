

names=[17220, 24, 27220, 38,   48065, 48073, 58073, 68073, 80099, 8034, 97316 ]
ends= [30063, 28, 48063, 13066,48068, 64831, 72088, 80088 ,109822,24013,119733]

bytes=[-1]*119738

for name, end in zip(names,ends):
    data=open(str(name),"rb").read()
    f=data.find("\r\n\r\n")
    data=data[f+4:]
    for i, c in enumerate(data):
        if bytes[i+name]==-1:
            bytes[i+name]=ord(c)
        if bytes[i+name]!=ord(c):
            print "Mismatch"

for i, c in enumerate(bytes):
    if c==-1:
        print "Missing at",hex(i)
        bytes[i]=0xcc

open("png.png","wb").write("".join([chr(c) for c in bytes]))
