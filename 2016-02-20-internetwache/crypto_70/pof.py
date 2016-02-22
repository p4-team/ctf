import hashlib, sys

for i in range(1000000, 9999999):
    s=sys.argv[1]+str(i)
    h=hashlib.sha1()
    h.update(s)
    h=h.hexdigest()
    if h[-4:]=="0000":
        print s
        break
