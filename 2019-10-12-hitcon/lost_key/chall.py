#!/usr/bin/env python
from Crypto.Util.number import *
import os,sys

sys.stdin  = os.fdopen(sys.stdin.fileno(), 'r', 0)
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

def read_key():
    key_file = open("key")
    n,e,d = map(int,key_file.readlines()[:3])
    return n,e,d

def calc(n,p,input):
  data = "X: "+input
  num = bytes_to_long(data)
  res = pow(num,p,n)
  return long_to_bytes(res).encode('hex')

def read_flag():
  flag = open('flag').read()
  assert len(flag) >= 50
  assert len(flag) <= 60
  prefix = os.urandom(68)
  return prefix+flag

if __name__ == '__main__':
  n,e,d = read_key()
  flag =  calc(n,e,read_flag())
  print 'Here is the flag!', flag
  for i in xrange(100):
    m = raw_input('give me your X value: ')
    try:
      m = m.decode('hex')[:15]
      print calc(n,e,m)
    except:
      print 'no'
      exit(0)
