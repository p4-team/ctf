import r2pipe, sys

r2=r2pipe.open("iof.elf")
fn=[
    0x40103b40,
    0x40103b90,
    0x40103bbc,
    0x40103bdc,
    0x40103c00,
    0x40103c24,
    0x40103c44,
    0x40103c98,
    0x40103ce0,
    0x40103d60,
    0x40103d88,
    0x40103dac,
    0x40103dd8,
    0x40103e04,
    0x40103e64,
    0x40103ec0,
    0x40103ee0,
    0x40103f00,
    0x40103f3c,
    0x40103f5c,
    0x40103f84,
    0x40103fb4
]
for f in fn:
    print hex(f)
    r2.cmd("s "+hex(f))
    r2.cmd("af")
    r2.cmd("afn f"+hex(f))
    j=r2.cmdj("pdfj")["ops"]
    for c in j:
        op=c["opcode"]
        op=op.replace("0x400d0a94", "$pass")
        op=op.replace("0x400d0aa0", "$MAC")
        op=op.replace("0x400d0a98", "$state")
        print "    "+op
        if "bne" in op:
            print "{-}"
    print "-----------------"
