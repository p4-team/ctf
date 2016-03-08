## unholy (reversing, 4 points, 68 solves)
	python or ruby? why not both! 

In this task we got a Ruby program, refering to shared library unholy.so. The program
mixed Ruby and Python code (and native code from the library).

Quick analysis of `main.rb` file showed that the program had a basic structure of typical
keygenme: get flag, tell if flag is good. We had to reverse the `is_key_correct` function.

Starting at the end, we noticed that it calls Python interpreter with the following code:
```
exec """
import struct
e=range
I=len
import sys
F=sys.exit
X=[[%d,%d,%d], [%d,%d,%d], [%d,%d,%d]]
Y = [[383212,38297,8201833], [382494 ,348234985,3492834886], [3842947 ,984328,38423942839]]
n=[5034563854941868,252734795015555591,55088063485350767967, -2770438152229037,142904135684288795,-33469734302639376803, -3633507310795117,195138776204250759,-34639402662163370450]
y=[[0,0,0],[0,0,0],[0,0,0]]
A=[0,0,0,0,0,0,0,0,0]
for i in e(I(X)):
 for j in e(I(Y[0])):
  for k in e(I(Y)):
   y[i][j]+=X[i][k]*Y[k][j]
c=0
for r in y:
 for x in r:
  if x!=n[c]:
   print "dang..."
   F(47)
  c=c+1
print ":)"
"""
```
It seems that we need to solve for X - it had `%d`'s in it, and assembly code called 
`sprintf` before, so it's probably our input, possibly after some processing.

The above Python code was simply multiplying `X` with `Y` and then comparing 
with `n` - all three being 3x3 matrices. Using numpy we quickly solved the `X*Y=n` equation
through tranforming it to equivalent equation `X=n*inv(Y)`.

OK, so now we got X. It did not look as ASCII or anything, so we had to look into unholy.so
to see what it really was. The most of the code was just parsing and changing internal number
representations - nothing really interesting. At some point, there was a lot of xors and shifts
with some constants - something that looked like a cipher of some kind. Googling one of the
constants (0xc6ef3720) revealed that it was XTEA algorithm. We found the decryption function
implementation and wrote a C++ code (`decrypt.cpp`) to decrypt what we had (the key was hidden 
as constant too). Running it yields the correct flag.
in the assembly too).
