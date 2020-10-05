#!/usr/bin/python3

s = []
p = 0

def init():
  global s,p
  s = [i for i in range(0,64)]
  p = 0
  return

def randgen():
  global s,p
  a = 3
  b = 13
  c = 37
  s0 = s[p]
  p = (p + 1) & 63
  s1 = s[p]
  res = (s0 + s1) & ((1<<64)-1)
  s1 ^= (s1 << a) & ((1<<64)-1)
  s[p] = (s1 ^ s0 ^ (s1 >> b) ^ (s0 >> c))  & ((1<<64)-1)
  return res

def jump(to):

  # Deleted...

  return

def check_jump():
  init()
  jump(10000)
  assert randgen() == 7239098760540678124

  init()
  jump(100000)
  assert randgen() == 17366362210940280642

  init()
  jump(1000000)
  assert randgen() == 13353821705405689004

  init()
  jump(10000000)
  assert randgen() == 1441702120537313559

  init()
  for a in range(31337):randgen()
  for a in range(1234567):randgen()
  buf = randgen()
  for a in range(7890123):randgen()
  buf2 = randgen()
  init()
  jump(31337+1234567)
  print (buf == randgen())  
  jump(7890123)
  print (buf2 == randgen())

check_jump()

init()
for a in range(31337):randgen()

flag = open("flag.txt").read()
assert len(flag) == 256

enc = b""

for x in range(len(flag)):
  buf = randgen()
  sh = x//2
  if sh > 64:sh = 64
  mask = (1 << sh) - 1
  buf &= mask
  jump(buf)
  enc += bytes([ ord(flag[x]) ^ (randgen() & 0xff) ])
  print ("%r" % enc)

open("enc.dat","wb").write(bytearray(enc))

