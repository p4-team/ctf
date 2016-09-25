import string, hashlib

s=open("re400.bin").read().strip().decode("hex")[::-1]

lasthi=2

res=""
for c in s:
    hi=ord(c)>>4
    res+=chr(ord(c)^((hi^lasthi)<<4))
    lasthi=hi
print res
print hashlib.md5(res[1:]).hexdigest()
