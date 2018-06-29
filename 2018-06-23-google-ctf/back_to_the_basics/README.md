# Back to the basics, re, 293p

>You won't find any assembly in this challenge, only C64 BASIC. Once you get the password, the flag is CTF{password}. P.S. The challenge has been tested on the VICE emulator.

Running the attached file on the emulator greets us with password prompt, so we probably have to guess it.

The binary was "compiled" BASIC code, and running it through a few disassemblers showed only a couple of
lines of source; much less than what we would expect from 32kB binary. There are a few strange `POKE`s there,
and when we checked what addresses they write to, it turned out to be program memory - so we have a self-modifying code
there!

Not willing to run it with debugger, I wrote a simple dumb disassembler, not stopping on any errors - `replace.py`.
We then found some extra lines:
```
2001 POKE  03397, 00069 : POKE  03398, 00013
2002 POKE  1024 +  CHKOFF +  1, 81:POKE  55296 +  CHKOFF +  1, 7
2004 ES =  03741 : EE =  04981 : EK =  148
2005 FOR  I =  ES TO  EE : K =  ( PEEK (I) +  EK ) AND  255 : POKE  I, K : NEXT  I
2009 POKE  1024 +  CHKOFF +  1, 87
```
These lines seem to be decoding some data, which happened to be garbage bytes placed right afterwards. We wrote a
script running the same algorithm (in a few places, since there were multiple blocks of code like that) - `decode.py`.
Disassembling the new code too, we found most of it readable. The encrypted chunks were of following form:
```
2010 V =  0.6666666666612316235641 -  0.00000000023283064365386962890625 : G =  0
2020 BA =  ASC ( MID$ (P$, 1, 1) )
2021 BB =  ASC ( MID$ (P$, 2, 1) )
2025 P0 =  0:P1 =  0:P2 =  0:P3 =  0:P4 =  0:P5 =  0:P6 =  0:P7 =  0:P8 =  0:P9 =  0:PA =  0:PB =  0:PC =  0
2030 IF  BA AND  1 THEN  P0 =  0.062500000001818989403545856475830078125
2031 IF  BA AND  2 THEN  P1 =  0.0156250000004547473508864641189575195312
2032 IF  BA AND  4 THEN  P2 =  0.0039062500001136868377216160297393798828
2033 IF  BA AND  8 THEN  P3 =  0.0009765625000284217094304040074348449707
2034 IF  BA AND  16 THEN  P4 =  0.0002441406250071054273576010018587112427
2035 IF  BA AND  32 THEN  P5 =  0.0000610351562517763568394002504646778107
2036 IF  BA AND  64 THEN  P6 =  0.0000152587890629440892098500626161694527
2037 IF  BA AND  128 THEN  P7 =  0.0000038146972657360223024625156540423632
2040 IF  BB AND  1 THEN  P8 =  0.0000009536743164340055756156289135105908
2031 IF  BB AND  2 THEN  P9 =  0.0000002384185791085013939039072283776477
2032 IF  BB AND  4 THEN  PA =  0.0000000596046447771253484759768070944119
2033 IF  BB AND  8 THEN  PB =  0.000000014901161194281337118994201773603
2034 IF  BB AND  16 THEN  PC =  0.0000000037252902985703342797485504434007
2050 K =  V +  P0 +  P1 +  P2 +  P3 +  P4 +  P5 +  P6 +  P7 +  P8 +  P9 +  PA +  PB +  PC
2060 G =  0.671565706376017
2100 T0 =  K =  G : A =  86 : B =  10
2200 IF  T0 =  - 1 THEN  A =  83 : B =  5
2210 POKE  1024 +  CHKOFF +  1, 90
2500 REM 
```

`P` was our password, and the code seems to be checking if sum of some bits of the password
multiplied by a few float constants is equal to another constant - i.e. subset sum problem.
We simply brute forced all the possibilities and saved the one that gave result closest to
the expected - `final.py`. Combining answers to a single text, yields the flag: `LINKED-LISTS-AND-40-BIT-FLOATS`.
