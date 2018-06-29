import struct
import sys
import hashlib
from better_zip import *

"""
[03:17-adam ~/CTF/gctf/zip]" python notes.py stuff.zip after_ins.png aabbccddaabbccddaabbccddaabbccddaabbccdd
"\xf5Q\xcd\xb9\xab\x9a\x89h\xe4\xed\xe4\xd6\xc8\x98\x8e\xac\xf0'\xd3\xa0"
LSFR: 20 467988 872949
LSFR: 20 644596 703388
LSFR: 20 317451 559514
LSFR: 20 200965 974406
LSFR: 20 260557 579300
LSFR: 20 71238 584076
LSFR: 20 945718 520364
LSFR: 20 409044 658738
'zt\xbb\xe4\r\x07$\x11r\xbd\x97\xbd\xb7\x99f\xdd\xde\xc6<Q'
LSFR: 20 943177 750714
LSFR: 20 102160 56907
LSFR: 20 636971 74759
LSFR: 20 584802 775969
LSFR: 20 904372 507287
LSFR: 20 99297 420251
LSFR: 20 844474 450269
LSFR: 20 571703 332748
"""

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

def find_polys(iv, expected):
    polys = []
    for poly in range(2**20):
        l = LFSR(poly, iv, 20)
        prev = 0
        bad = False
        for i, what in expected:
            while prev != i:
                prev += 1
                l.get_bit()
            prev += 1
            bit = l.get_bit()
            if bit != what:
                bad = True
                break
        
        if poly % 2**14 == 0:
            print poly

        if not bad:
            polys.append(poly)
    return polys

known = {
    20: "\x00", # Hi height
    21: "\x00", # Hi height
    24: "\x08", # Bit depth
    25: "\x02", # Color type [?]
    26: "\x00", # Compression
    27: "\x00", # Filter type
    28: "\x00", # No interlace
    33: "\x00", # chunk high byte
#    37: "I",
#    38: "D",
#    39: "A",
#    40: "T",
    # 00 00 00 00 49  45 4e 44 ae 42 60 82
    tgtlen - 12: "\x00",
    tgtlen - 11: "\x00",
    tgtlen - 10: "\x00",
    tgtlen - 9: "\x00",
    tgtlen - 8: "I",
    tgtlen - 7: "E",
    tgtlen - 6: "N",
    tgtlen - 5: "D",
    tgtlen - 4: "\xae",
    tgtlen - 3: "\x42",
    tgtlen - 2: "\x60",
    tgtlen - 1: "\x82",
}
cipher_iv_stream = BitStream(cipher_iv)
for bit in range(8):
    expected = []
    for c in sorted(known):
        expected.append((c, ((ord(known[c]) ^ ord(enc[c])) >> bit) & 1))
    iv = cipher_iv_stream.get_bits(20)
    print find_polys(iv, expected), "for", bit
