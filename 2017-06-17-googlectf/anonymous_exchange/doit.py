from pwn import *
import json

r=remote("anon.ctfcompetition.com", 1337)
r.send("NEWACC\n"*256)
r.send("NEWCARD\n"*256)

r.send("ASSOC ucard0xff uaccount0x1\n")
r.send("ASSOC ucard0xfe uaccount0x1\n")
r.send("ASSOC ucard0x1 uaccount0x1\n")

for i in range(1, 0x41):
    r.send("ASSOC ucard"+hex(i)+" uaccount"+hex(i+1)+"\n")
    r.send("ASSOC ucard"+hex(i+1)+" uaccount"+hex(i+1)+"\n")
    r.send("ASSOC ccard"+hex(i)+" uaccount"+hex(i+1)+"\n")

r.send("ASSOC ucard0x41 uaccount0x42\n")

r.send("BACKUP\n")

r.recvuntil("[")
s="["+r.recvline()
j=json.loads(s)

print json.dumps(j, indent=4)
vertices=[]
edges={}
isburnt={}
for v in j:
    a="a_"+v["account"]
    vertices.append(a)
    for c in v["cards"]:
        c1=c
        c = "c_"+c["card"]
        isburnt[c] = "flagged" in c1
        if c not in vertices:
            vertices.append(c)

        if a not in edges:
            edges[a] = [c]
        else:
            edges[a].append(c)
        if c not in edges:
            edges[c] = [a]
        else:
            edges[c].append(a)

print vertices
print edges

# That's a very inefficient means of finding longest chain in the graph, but
# it works for the graph of this size...
def dfs(vis, v):
    vis=vis[:]
    res=0
    if v in edges:
        for e in edges[v]:
            if e not in vis:
                res=max(res, dfs(vis+[e], e))
    return res+1

bestd=-1
cands=[]
for v in vertices:
    d=dfs([v], v)
    if d>bestd:
        cands=[]
        bestd=d
    if d==bestd:
        cands.append(v)

print bestd, cands
for c in cands:
    if c[0]=="a":
        a=c

prevc = edges[a][0]
if edges[prevc][0] == a:
    a = edges[prevc][1]
else:
    a = edges[prevc][0]

result=""
while True:
    target = None
    next = None
    print len(edges[a]),"edges"
    for e in edges[a]:
        if len(edges[e]) == 1:
            target = e
        elif e != prevc:
            next = e
    if next is None:
        break
    if isburnt[target]:
        result+="1"
    else:
        result+="0"
    c=next
    for e in edges[c]:
        if e != a:
            next = e
    a=next
    prevc=c

print result
print len(result)



r.sendline(result[::-1])

r.interactive()
