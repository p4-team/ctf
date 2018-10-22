#!/usr/bin/env python
from Crypto.Util.number import *
from gmpy import *
from random import *
import sys,os


sys.stdin  = os.fdopen(sys.stdin.fileno(), 'r', 0)
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
rnd = SystemRandom()

def encrypt(g,n,data):
  num = bytes_to_long(data)
  res = pow(g,num,n*n)
  r = rnd.randint(0,n-1)
  magic = pow(r,n,n*n)
  res = (res*magic)%(n*n)
  return long_to_bytes(res).encode('hex')

def decrypt(phi,n,u,data):
  num = bytes_to_long(data)
  res = pow(num,phi,n*n)
  res = (res - 1)/n
  res = (res*u)%n
  return long_to_bytes(res).encode('hex')

if __name__ == '__main__':
  p = getPrime(512)
  q = getPrime(512)
  n = p*q
  phi = (p-1)*(q-1)
  g = n+1
  u = invert(phi,n)
  flag = open('flag').read()
  print 'Here is the flag!'
  print encrypt(g,n,flag)
  for i in xrange(2048):
    m = raw_input('cmd: ')
    if m[0] == 'A':
      m = raw_input('input: ')
      try:
        m = m.decode('hex')
        print encrypt(g,n,m)
      except:
        print 'no'
        exit(0)
    if m[0] == 'B':
      m = raw_input('input: ')
      try:
        m = m.decode('hex')
        print decrypt(phi,n,u,m)[-2:]
      except:
        print 'no'
        exit(0)
