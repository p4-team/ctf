import r2pipe, sys

r2=r2pipe.open("iof.elf")
s=r2.cmd("p8 4 @ "+sys.argv[1])
s=s[6:8]+s[4:6]+s[2:4]+s[0:2]
print s
print r2.cmd("xr 4 @ "+sys.argv[1]+"")
r=open("esp32.rom").readlines()
for l in r:
    if s in l:
        print l
