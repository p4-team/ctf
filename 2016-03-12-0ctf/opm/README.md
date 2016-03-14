## OPM (Misc, 3p)
	
###ENG
[PL](#pl-version)

In this task, we got only an image - so the first step was probably solving a stegano task.
Using Stegsolve, we quickly see that least significant bits of all three channels (R,G,B) contain
semi-random data on top of the image, and are totally black on the bottom. Extracting data from those
channels (also using Stegsolve), we see that first two bytes are "PK" - a zip file signature.

After unzipping the file, we get a single file called "STMFD SP!, {R11,LR}". We recognize it as an
ARM assembly instruction. The file contained hexdump of another file in form:
```
aa109c60 e92d4800
aa109c64 e28db004
aa109c68 e24dd018
aa109c6c e50b0010
aa109c70 e50b1014
aa109c74 e50b2018
...
```
The first column was increasing, so it was probably just an address - the bytes on the right were more
interesting. After creating a new file containing the second column concatenated and unhexed (in little
endian), we got an ARM binary (without any headers, just the assembled code). After analyzing the code,
we see that it accepts a password and checks if it is correct. A very high fraction of the file is
used for the key-checking function. It is very repetitive too: most of the code looks like:
```
     c7c:    e51b3050     ldr    r3, [fp, #-80]    ; 0xffffffb0
     c80:    e3e0101a     mvn    r1, #26
     c84:    e0030391     mul    r3, r1, r3
     c88:    e0822003     add    r2, r2, r3
```
That means:
```
c7c - load byte from password at position 80
c80 - r1=26
c84 - r3=r1*r3
c88 - r2+=r3
```
Or, shortly: `r2+=password[80]*26`.

This procedure was repeated for every password byte. R2 was then checked against a constant value.
The whole checking code was repeated a few times with different constants, to ensure that the password
is unique.

We quickly saw that the password is a string that satisfies:
```
pass[0]*a00 + pass[1]*a01 + pass[2]*a02 ... = b0
pass[0]*a10 + pass[1]*a11 + pass[2]*a12 ... = b1
...
```
It was not easy to parse the disassembly to get the a's and b's though - some multiplications
were realized as logical shifts, for example. Instead, we decompiled the code using Retargetable 
Decompiler - http://pastebin.com/yrziPfYy. The code looked much better for parsing. We selected
the interesting part of the code to `decomp` file, and wrote Python code which would parse it -
`solve.py`. The code, when ran, gives us the flag: `Tr4c1Ng_F0R_FuN!`.

###PL version
