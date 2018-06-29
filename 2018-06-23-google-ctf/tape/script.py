import subprocess
import string

for a in string.letters:
    for b in string.letters:
        with open("/tmp/ff", "wb") as f:
            f.write(": You probably just want the flag.  So here it is: CTF{dZXi%c%c--------PIUTYMI}. :" % (a, b))
        o = subprocess.check_output([
            "./crchack", "-w64", "-p", "0x42F0E1EBA9EA3693", "-Rr", "/tmp/ff", "0x30d498cbfb871112", "-o", "61"])
        l = len(repr(o))
        if l < 85:
            print a, b, l, repr(o)
