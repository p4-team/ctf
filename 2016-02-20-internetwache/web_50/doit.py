import hashlib

def md5(s):
    m=hashlib.md5()
    m.update(s)
    return m.hexdigest()

def hash(s):
    return md5(md5(s)+"SALT")

def isnum(s):
    for c in s:
        if c not in "0123456789":
            return False
    return True

i=0
while True:
    i+=1
    h=hash(str(i))
    if h[:2]=="0e" and isnum(h[2:]):
        print h
        print i
        break
    if i%1000000==0:
        print i
