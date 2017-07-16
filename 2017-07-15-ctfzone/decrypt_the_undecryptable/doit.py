s=open("flag.encrypted","rb").read()

o=0x2c500
key=s[o:o+128]
r=s[:128*50]
for i in range(128*50, len(s)):
    r+=chr(ord(s[i]) ^ ord(key[i%128]))
open("dec","wb").write(r)
