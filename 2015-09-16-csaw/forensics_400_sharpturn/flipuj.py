expected = 'efda2f556de36b9e9e1d62417c5f282d8961e2f8' # level 1
expected = '354ebf392533dce06174f9c8c093036c138935f3' # level 2
expected = 'd961f81a588fcfd5e57bbea7e17ddae8a5e61333' # level 3
expected = 'f8d0839dd728cb9a723e32058dcc386070d5e3b5' # level 4

d = open('sharp_v4_f8d0_8096').read()

def githash(d):
    import hashlib
    return hashlib.sha1('blob {}\0{}'.format(len(d), d)).hexdigest()

def bitflips(dat):
    for i in range(len(dat)):
        c = ord(dat[i])
        for bit in range(256):
            cc = chr(bit)
            dd = dat[:i] + cc + dat[i+1:]
            yield dd


for f in bitflips(d):
    if githash(f) == expected:
        print f
