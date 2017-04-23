from Crypto.Cipher import DES
import struct
import string

def seven_to_eight(x):
  [val] = struct.unpack("Q", x+"\x00")
  out = 0
  mask = 0b1111111
  for shift in xrange(8):
    out |= (val & (mask<<(7*shift)))<<shift
  return struct.pack("Q", out)

def unpad(x):
  #split up into 7 byte chunks
  length = struct.pack("Q", len(x))
  sevens = [x[i:i+7].ljust(7, "\x00") for i in xrange(0,len(x),7)]
  sevens.append(length[:7])
  return map(seven_to_eight, sevens)

def hash(x):
  h0 = "SHA4_IS_"
  h1 = "DA_BEST!"
  keys = unpad(x)
  for key in keys:
    h0 = DES.new(key).encrypt(h0)
    h1 = DES.new(key).encrypt(h1)
  return h0+h1