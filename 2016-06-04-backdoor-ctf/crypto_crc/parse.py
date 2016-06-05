

a=[]
for i in range(30):
    a.append([])

data=open("out").readlines()
mx=0
for line in data:
    if line.strip()=="":
        break
    num=int(line.split("(")[1].split(")")[0])
    line=line.split(") for ")[1]
    a[num].append(line.strip())
    if len(a[num])>mx:
        mx=len(a[num])

for i in range(mx):
    for arr in a:
        if len(arr)<=i:
            print " "*7,
        else:
            print arr[i],
    print 
