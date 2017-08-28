#!/usr/bin/env python

import sys
from deadpool_dca import *

def processinput(iblock, blocksize):
    p='%0*x' % (2*blocksize, iblock)
    f=open("/tmp/xd", "wb")
    f.write(p.decode("hex"))
    f.close()
    return ["--stdin </tmp/xd"]

def processoutput(output, blocksize):
    o=output.replace(" ","")
    return int(o, 16)
    return int(''.join([x for x in output.split('\n') if x.find('OUTPUT')==0][0][10:].split(' ')), 16)

T=TracerPIN('./whitebox', processinput, processoutput, ARCH.amd64, 16, shell=True)
T.run(2000)
bin2daredevil(configs={'attack_sbox':   {'algorithm':'AES', 'position':'LUT/AES_AFTER_SBOX'},
                       'attack_multinv':{'algorithm':'AES', 'position':'LUT/AES_AFTER_MULTINV'}})
