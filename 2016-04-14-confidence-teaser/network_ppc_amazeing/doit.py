from pwn import *
import hashlib
import matplotlib.pyplot as plt

sys.setrecursionlimit(100000)
context.log_level="DEBUG"
host="amazeing.hackable.software"
r=remote(host,1337)
key=""

def move(m):
    x=m[0]
    y=m[1]
    if y==-1:
        port=31337
    if y==1:
        port=31339
    if x==-1:
        port=31336
    if x==1:
        port=31338
    rr=remote(host,port)
    rr.sendline(key)
    rr.close()

def brute(start, needed):
    i=0
    while True:
        s=start+str(i)
        h=hashlib.sha1(s).hexdigest()[:len(needed)]
        if h==needed:
            return s
        i+=1

s=r.recvuntil("... ...")
print s
for word in s.split(" "):
    if word[:2]=="0x":
        pof=word[2:].lower()
s=brute("DrgnS",pof)
print s
r.send(s+"\n")

r.recvuntil("secret is : ")
key=r.recvuntil(" ")[:-1]
print repr(key)
r.recvline()

visited=set((5,-5))
walls=set()

plt.get_current_fig_manager().resize(1200,800)
plt.show(block=False)
xx=[]
yy=[]
xw=[]
yw=[]

def move_ok():
    line=r.recvline()
    print "OKOKOK: ", line
    if line.find("Ok")>-1:
        return True
    return False

def redraw():
    plt.plot(xx, yy, "ro", xw, yw, "bo")
    plt.xlim(min(xx+xw)-1, max(xx+xw)+1)
    plt.ylim(min(yy+yw)-1, max(yy+yw)+1)
    plt.draw()

def dfs(curpos):
    xx.append(curpos[0])
    yy.append(curpos[1])
    if (len(xx)+len(xw))%20==0:
        print "Visited"
        print visited
        print "Walls"
        print walls
        redraw()
    print "DFS"+str(curpos)
    print ""
    for movement in [(0,1),(0,-1),(-1,0),(1,0)]:
        newpos=(curpos[0]+movement[0], curpos[1]+movement[1])
        if newpos in visited:
            continue
        if newpos in walls:
            continue
        move(movement)
        if move_ok():
            visited.add(newpos)
            dfs(newpos)
            revmovement=(-movement[0], -movement[1])
            move(revmovement)
            move_ok()
        else:
            xw.append(newpos[0])
            yw.append(newpos[1])
            walls.add(newpos)

dfs((5,5))
print visited
print walls
redraw()

r.interactive()
