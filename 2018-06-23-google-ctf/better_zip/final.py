import os
import zipfile
import zlib
import hashlib
from struct import pack, unpack
import sys

POLY_SZ = 20


class BitStream:
  def __init__(self, data, sz=None):
    if sz is None:
      sz = len(data) * 8

    self.sz = sz
    self.data = bytearray(data)
    self.idx = 0

  def get_bit(self):
    if self.idx >= self.sz:
      raise Exception('All bits used. Go away.')

    i_byte = self.idx / 8
    i_bit = self.idx % 8

    bit = (self.data[i_byte] >> i_bit) & 1
    self.idx += 1

    return bit

  def get_bits(self, sz):
    v = 0
    for i in xrange(sz):
      v |= self.get_bit() << i

    return v


class LFSR:
  def __init__(self, poly, iv, sz):
    self.sz = sz
    self.poly = poly
    self.r = iv
    self.mask = (1 << sz) - 1

  def get_bit(self):
    bit = (self.r >> (self.sz - 1)) & 1

    new_bit = 1
    masked = self.r & self.poly
    for i in xrange(self.sz):
      new_bit ^= (masked >> i) & 1

    self.r = ((self.r << 1) | new_bit) & self.mask
    return bit


class LFSRCipher:
  def __init__(self, poly_sz=20, keys=None, cipher_iv=None):
    cipher_iv_stream = BitStream(cipher_iv)

    self.lfsr = []
    for i in xrange(8):
      l = LFSR(keys[i],
               cipher_iv_stream.get_bits(poly_sz), poly_sz)
      self.lfsr.append(l)

  def get_keystream_byte(self):
    b = 0
    for i, l in enumerate(self.lfsr):
      b |= l.get_bit() << i
    return b

  def crypt(self, s):
    s = bytearray(s)
    for i in xrange(len(s)):
      s[i] ^= self.get_keystream_byte()
    return str(s)

a = [
    [891178],
    [96592, 196791, 382325, 560159, 741274, 950625],
    [360648, 384019, 569495],
    [51229, 161872],
    [219426],
    [416203],
    [161972, 860275, 1010447],
    [111181, 342767],
]

import itertools
import sys, struct

s = open(sys.argv[1], "rb").read()
datalen = struct.unpack("<I", s[18:22])[0]
tgtlen = datalen - 40 - 32 # 0x16dea
print hex(tgtlen)
fname = "flag.png"
#fname = "after_ins.png"
data = s[s.find(fname)+len(fname):][:datalen]
key_iv = data[:20]
cipher_iv = data[20:40]
print repr(cipher_iv)
enc = data[40:][:tgtlen]

poss = []
for prod in itertools.product(*a):
    c = LFSRCipher(20, prod, cipher_iv)
    cc = c.crypt(enc[:100])
    if cc[37:41] != "sRGB": continue
    print prod
    print repr(cc[33:])
    c = LFSRCipher(20, prod, cipher_iv)
    cc = c.crypt(enc)
    poss.append(cc)

for i, p in enumerate(poss):
    open(str(i) + ".png", "wb").write(p)
