import subprocess

for byte in range(256):
    data=open("png.png","rb").read()

    hdr="89504e470d0a1a0a0000000d494844520000029b000010000802000000b210bd54"
    hdr=hdr.decode("hex")

    data=hdr+data[len(hdr):]

    idats=[]
    ind=0
    while True:
        ind=data.find("IDAT", ind+1)
        if ind==-1:
            break
        idats.append(ind)
    print idats

    data=[ord(c) for c in data]

    def putint(pos, n):
        data[pos+3]=n%256
        n/=256
        data[pos+2]=n%256
        n/=256
        data[pos+1]=n%256
        n/=256
        data[pos]=n%256

    putint(0x21, 16000) # Size of IDAT
    data[0x25]=ord('I') # Fix IDAT name

    data[0xbbc0]=byte
    putint(0xbbc5, 16000) # Size of IDAT

    putint(0x138d9, 0x46d70176) # CRC
    putint(0x138dd, 16000) # Size of IDAT
    data[0x138e1]=ord('I')
    data[0x138e2]=ord('D')

    putint(0x1d3b6, 0xae426082) # CRC

    open("png3","wb").write("".join([chr(c) for c in data]))

    try:
        subprocess.check_output(["pngcheck","png3"])
        print byte,"is good"
        break
    except:
        print byte,"is bad"
        continue
