import subprocess, string, sys, os

alphabet=string.printable

def get_ic(s):
    subprocess.check_output(["/bin/bash", "ins", s]) # ins is my alias for intel pin's instructioon counting tool.
    return int(open("inscount.out").read()[5:])

key="BKPCTF{"
while True:
    longest=0
    longest_for=""
    for c in alphabet:
        print repr(c),
        sys.stdout.flush()
        n=get_ic(key+c)
        if n>longest:
            longest=n
            longest_for=c
            print "!!!",
    key=key+longest_for
    print key
