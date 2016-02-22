import subprocess, string, itertools, random, binascii, base64, sys

def get_n(f):
    s=subprocess.check_output(["openssl","rsa","-noout","-text","-inform","PEM","-pubin","-in",f])
    start=string.find(s,"Modulus:")
    end=string.find(s,"Exponent:")
    modulus=s[start:end].replace("Modulus:","").replace("\n","").replace(":","").replace(" ","")
    return int(modulus, 16)

print get_n("bob.pub")
print get_n("bob2.pub")
print get_n("bob3.pub")

#From yafu:

p=[20016431322579245244930631426505729, 16549930833331357120312254608496323, 19193025210159847056853811703017693]
q=[17963604736595708916714953362445519, 16514150337068782027309734859141427, 17357677172158834256725194757225793]

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def get_d(p, q):
    phi=(p-1)*(q-1)
    return modinv(65537, phi)

def decrypt(ct, p, q):
    ct=int(binascii.hexlify(ct), 16)
    s=hex(pow(ct, get_d(p,q), p*q))[2:]
    if s[-1]=="L":
        s=s[:-1]
    if len(s)%2!=0:
        s="0"+s
    return binascii.unhexlify(s)

txt=open("secret.enc","rb").read().split("\n")
cts=[]
for i in txt:
	if i=="":
		continue
	cts.append(base64.b64decode(i))

for ct in cts:
	for i in range(3):
		pt=decrypt(ct, p[i], q[i])
		for c in pt:
			if c in string.printable:
				sys.stdout.write(c)
			else:
				sys.stdout.write(" ")
		print ""
