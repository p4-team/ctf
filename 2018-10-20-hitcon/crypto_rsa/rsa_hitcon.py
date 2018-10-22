#!/usr/bin/env python
from Crypto.Util.number import *
from gmpy import *
import os,sys

sys.stdin  = os.fdopen(sys.stdin.fileno(), 'r', 0)
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

def genKey():
  p = getPrime(512)
  q = getPrime(512)
  n = p*q
  phi = (p-1)*(q-1)
  while True:
    e = getRandomInteger(40)
    if gcd(e,phi) == 1:
      d = int(invert(e,phi))
      return n,e,d

def calc(n,p,data):
  num = bytes_to_long(data)
  res = pow(num,p,n)
  return long_to_bytes(res).encode('hex')

def readFlag():
  flag = open('flag').read()
  assert len(flag) >= 50
  assert len(flag) <= 60
  prefix = os.urandom(68)
  return prefix+flag

if __name__ == '__main__':
  n,e,d = genKey()
  flag =  calc(n,e,readFlag())
  print 'Here is the flag!'
  print flag
  for i in xrange(150):
    msg = raw_input('cmd: ')
    if msg[0] == 'A':
      m = raw_input('input: ')
      try:
        m = m.decode('hex')
        print calc(n,e,m)
      except:
        print 'no'
        exit(0)
    elif msg[0] == 'B':
      m = raw_input('input: ')
      try:
        m = m.decode('hex')
        print calc(n,d,m)[-2:]
      except:
        print 'no'
        exit(0)

