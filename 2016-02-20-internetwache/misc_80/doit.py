import binascii

s=open("flag.pcapng","rb").read().split(".2015.")
res=""
for i in s:
    j=i.split("Host: ")[-1]
    try:
        r=binascii.unhexlify(j)
        print r
        res=res+r
    except:
        pass
print res
