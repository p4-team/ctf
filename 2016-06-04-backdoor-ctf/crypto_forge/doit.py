import subprocess

infile="mandog.png"

print "Running first collision."
subprocess.check_output(["./fastcol","-p",infile,"-o","a","b"])
col1a=open("a","rb").read()[-0x80:]
col1b=open("b","rb").read()[-0x80:]

print "Running second collision."
subprocess.check_output(["./fastcol","-p","a","-o","c","d"])
col2a=open("c","rb").read()[-0x80:]
col2b=open("d","rb").read()[-0x80:]

print "Running third collision."
subprocess.check_output(["./fastcol","-p","c","-o","e","f"])
col3a=open("e","rb").read()[-0x80:]
col3b=open("f","rb").read()[-0x80:]

base=open("a","rb").read()[:-0x80]

i=0
for col1 in [col1a, col1b]:
    for col2 in [col2a, col2b]:
        for col3 in [col3a, col3b]:
            open("collision_"+str(i)+".png","wb").write(base+col1+col2+col3)
            i+=1
