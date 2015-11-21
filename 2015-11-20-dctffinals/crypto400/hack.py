inp0 = "People don't understand computers. Computers are magical boxes that do things. People believe what computers tell them."
inp1 = "There are two types of encryption: one that will prevent your sister from reading your diary and one that will prevent your government."
inp2 = "There's an entire flight simulator hidden in every copy of Microsoft Excel 97."

inp0 = "People don't understand computers. Computers are magical boxes that do things. People believe what computers tell them."
out0 = "a2ccb5e4a4f694bd8a87cec3679d69a87db401a4199006dbb0ccbfe6a7ecc3e4f7b2e426c53fed35f95fe3498d038bebdbadeabce9cdfecf87968776876be12088228041c951730a7a30702e197802372236c03dc443934bef55ee71e03f423f7e213715360c1e060aec10fa7ea57ad36f94069f066c50".decode("hex")

inp1 = "There are two types of encryption: one that will prevent your sister from reading your diary and one that will prevent your government."
out1 = "2e4d3e6d2433102f12514b45ae01ef33f32d9869da5b891177076b3b7f34172d237224ca28da588151f349b023a5335a6a0155014b69557c343e2fd3358a538f3c8330a36ffe8eec999ac69abf94a7acbbe01fe108dd4f96378529b96df397e6e6a2fadeb2919b979b38c131f93aa015b709990d9fecdebafdbbf79ead9d819163867db97bb854".decode("hex")

inp2 = "There's an entire flight simulator hidden in every copy of Microsoft Excel 97."
out2 = "fa99eab9f0e0d1bc8588c6da30cb38ef3aa101bc0989139ab2d2a5e1a0f3d8f9f6efb950b54680489e7dda6da923afcfadcfc99bc8ffd4a9aebbe521dc20f82291358510dc6e147a074846463554".decode("hex")

out3 = "b4d0b1b0e5bd8ae7cdcbc4d139cf75b173ad4bfb0787008ff2cdf3bffda783f6fff2a44ba81fd61edf3c853daa65ea9ce99690d586e1dee2e1f7a949a916d50dbd19bc2eab3e50380e0d7a2c1d205a59455fbe0ffa2ea63b9074ce43d11e715d495401235f693e31289b2c8d198158f81ba471b32917644e".decode('hex')
inp = [inp0, inp1, inp2]
out = [out0, out1, out2, out3] 

print ''.join(chr((ord(out1[i]) ^ ord(out1[i+1])) ^ (ord(out3[i]) ^ ord(out3[i+1])) ^ ord(inp1[i+1])) for i in range(len(out0)))

#for c in range(256):
#    if (ord(out1[0]) ^ ord(out1[1])) ^ (ord(out3[0]) ^ ord(out3[1])) == ord(inp1[1]) ^ c:
#        print chr(c)

#for o in out:
#    print len(o)
#
#for o in out:
#    for i in range(20):
#        print ord(o[i]) ^ ord(o[i+1]), 
#    print
#
#print out0[29], out1[29]
#
#print ord(out0[29]) ^ ord(out1[29])


#for oi in range(3):
#    o = out[oi]
#    for i in range(1):
#        print ord(o[i]) ^ ord(o[i+1]) - ord(inp[oi][i]),
#    print

#for i in range(len(out)):
#    o = out[i]
#    print ''.join('1' if ord(oc)&0x40 != 0 else '0' for oc in o)
#
#from collections import defaultdict
#hack = defaultdict(list)
#
#for i in range(len(inp1) - 1):
#    x = ord(inp1[i]) ^ ord(inp1[i+1])
#
#print
#for i in range(20):
#    print ord(out1[i]) ^ ord(out2[i]), 
