# Counting (re, 246p)

> This strange program was found, which apparently specialises in counting. In order to find the flag, you need to output find what the output of ./counter 9009131337 is.

> code

> counter


In this challenge we were given two files: an ELF binary, and a small unknown file.

Running the binary with some small arguments gives the following results:

```
$ for i in 20 25 30; do time ./counter $i; done
CTF{0000000000000065}

real	0m0,015s
user	0m0,012s
sys	0m0,000s
CTF{000000000000000d}

real	0m0,096s
user	0m0,092s
sys	0m0,000s
CTF{000000000000013a}

real	0m1,015s
user	0m1,012s
sys	0m0,000s
```

OK, so running the file with argument as small as 30 already takes 30 seconds. That's too
bad, since we need to find the result of running `./counter 9009131337`. We need to find 
another way.

Thankfully, the `counter` binary was pretty small and quite simple to analyze. It seemed
to be opening the `code` file and reading its contents to 16-byte sized structures.
The second part of the binary was a virtual machine - it executed the instructions encoded
in those structures. The virtual machine had 26 registers - apparently one per each letter
of the alphabet. The argument given in the command line was put in the first one (rA).
When the instruction pointer reaches the point after last instruction, the interpreter
exits, and the flag is printed containg the value in first register in hexadecimal format.

There were only three types of instructions:
- 0: increment rX, then jump to instruction Y.
- 1: if rX is 0, jump to instruction Y, otherwise decrement rX and jump to instruction Z.
- 2: "fork" to instruction X, then copy first Y registers from fork.

The last instruction could be also interpreted as function call, while saving all
the registers except for ones making up the return value.

We wrote a simple parser in Python and used it to disassemble the file:

```
00: if (rA!=0){ rA--; jmp 01;} else jmp 02;
01: rB++; jmp 00;
02: rC++; jmp 03;
03: rC++; jmp 04;
04: rC++; jmp 05;
05: rC++; jmp 06;
06: rC++; jmp 07;
07: rC++; jmp 08;
08: rC++; jmp 09;
09: rC++; jmp 10;
10: rC++; jmp 11;
11: rC++; jmp 12;
12: rC++; jmp 13;
13: fork @ 108; copy up to rB; jmp 14;
14: if (rA!=0){ rA--; jmp 119;} else jmp 15;
15: fork @ 20; copy up to rB; jmp 16;
16: if (rC!=0){ rC--; jmp 16;} else jmp 17;
17: if (rA!=0){ rA--; jmp 18;} else jmp 19;
18: rC++; jmp 17;
19: fork @ 64; copy up to rB; jmp 119;
20: if (rC!=0){ rC--; jmp 20;} else jmp 21;
21: fork @ 29; copy up to rB; jmp 22;
22: if (rA!=0){ rA--; jmp 23;} else jmp 24;
23: rC++; jmp 22;
24: if (rB!=0){ rB--; jmp 25;} else jmp 26;
25: if (rZ!=0){ rZ--; jmp 00;} else jmp 21;
26: if (rA!=0){ rA--; jmp 26;} else jmp 27;
27: if (rC!=0){ rC--; jmp 28;} else jmp 119;
28: rA++; jmp 27;
29: if (rC!=0){ rC--; jmp 29;} else jmp 30;
30: fork @ 84; copy up to rB; jmp 31;
31: if (rD!=0){ rD--; jmp 31;} else jmp 32;
32: if (rA!=0){ rA--; jmp 33;} else jmp 34;
33: rD++; jmp 32;
34: if (rD!=0){ rD--; jmp 35;} else jmp 42;
35: if (rD!=0){ rD--; jmp 36;} else jmp 42;
36: fork @ 45; copy up to rB; jmp 37;
37: rC++; jmp 38;
38: if (rB!=0){ rB--; jmp 38;} else jmp 39;
39: if (rA!=0){ rA--; jmp 40;} else jmp 41;
40: rB++; jmp 39;
41: if (rZ!=0){ rZ--; jmp 00;} else jmp 30;
42: if (rA!=0){ rA--; jmp 42;} else jmp 43;
43: if (rC!=0){ rC--; jmp 44;} else jmp 119;
44: rA++; jmp 43;
45: if (rC!=0){ rC--; jmp 45;} else jmp 46;
46: fork @ 84; copy up to rB; jmp 47;
47: if (rA!=0){ rA--; jmp 48;} else jmp 49;
48: rC++; jmp 47;
49: fork @ 92; copy up to rC; jmp 50;
50: if (rB!=0){ rB--; jmp 51;} else jmp 119;
51: if (rA!=0){ rA--; jmp 51;} else jmp 52;
52: if (rB!=0){ rB--; jmp 52;} else jmp 53;
53: if (rC!=0){ rC--; jmp 54;} else jmp 55;
54: rB++; jmp 53;
55: fork @ 84; copy up to rB; jmp 56;
56: if (rA!=0){ rA--; jmp 57;} else jmp 58;
57: rC++; jmp 56;
58: fork @ 84; copy up to rB; jmp 59;
59: if (rB!=0){ rB--; jmp 60;} else jmp 61;
60: rA++; jmp 59;
61: if (rC!=0){ rC--; jmp 62;} else jmp 63;
62: rA++; jmp 61;
63: rA++; jmp 119;
64: fork @ 84; copy up to rB; jmp 65;
65: if (rD!=0){ rD--; jmp 65;} else jmp 66;
66: if (rA!=0){ rA--; jmp 67;} else jmp 68;
67: rD++; jmp 66;
68: if (rD!=0){ rD--; jmp 69;} else jmp 119;
69: rA++; jmp 70;
70: if (rD!=0){ rD--; jmp 71;} else jmp 119;
71: if (rB!=0){ rB--; jmp 72;} else jmp 119;
72: fork @ 64; copy up to rB; jmp 73;
73: if (rE!=0){ rE--; jmp 73;} else jmp 74;
74: if (rA!=0){ rA--; jmp 75;} else jmp 76;
75: rE++; jmp 74;
76: if (rB!=0){ rB--; jmp 77;} else jmp 119;
77: fork @ 64; copy up to rB; jmp 78;
78: if (rA!=0){ rA--; jmp 79;} else jmp 80;
79: rE++; jmp 78;
80: if (rB!=0){ rB--; jmp 80;} else jmp 81;
81: if (rE!=0){ rE--; jmp 82;} else jmp 83;
82: rB++; jmp 81;
83: fork @ 99; copy up to rB; jmp 119;
84: if (rA!=0){ rA--; jmp 84;} else jmp 85;
85: if (rB!=0){ rB--; jmp 86;} else jmp 119;
86: rA++; jmp 85;
87: if (rA!=0){ rA--; jmp 87;} else jmp 88;
88: if (rB!=0){ rB--; jmp 89;} else jmp 90;
89: rA++; jmp 88;
90: if (rC!=0){ rC--; jmp 91;} else jmp 119;
91: rA++; jmp 90;
92: if (rA!=0){ rA--; jmp 92;} else jmp 93;
93: if (rB!=0){ rB--; jmp 93;} else jmp 94;
94: if (rC!=0){ rC--; jmp 95;} else jmp 119;
95: if (rC!=0){ rC--; jmp 96;} else jmp 98;
96: rA++; jmp 97;
97: if (rZ!=0){ rZ--; jmp 00;} else jmp 94;
98: rB++; jmp 119;
99: fork @ 108; copy up to rB; jmp 100;
100: if (rA!=0){ rA--; jmp 101;} else jmp 103;
101: if (rB!=0){ rB--; jmp 102;} else jmp 119;
102: rA++; jmp 101;
103: fork @ 113; copy up to rB; jmp 104;
104: if (rB!=0){ rB--; jmp 104;} else jmp 105;
105: if (rA!=0){ rA--; jmp 106;} else jmp 107;
106: rB++; jmp 105;
107: if (rZ!=0){ rZ--; jmp 00;} else jmp 99;
108: if (rA!=0){ rA--; jmp 108;} else jmp 109;
109: if (rC!=0){ rC--; jmp 110;} else jmp 119;
110: if (rB!=0){ rB--; jmp 111;} else jmp 112;
111: if (rZ!=0){ rZ--; jmp 00;} else jmp 108;
112: rA++; jmp 119;
113: if (rC!=0){ rC--; jmp 114;} else jmp 116;
114: if (rB!=0){ rB--; jmp 115;} else jmp 119;
115: if (rZ!=0){ rZ--; jmp 00;} else jmp 113;
116: if (rA!=0){ rA--; jmp 116;} else jmp 117;
117: if (rB!=0){ rB--; jmp 118;} else jmp 119;
118: rA++; jmp 117;
```

Hmm. That's quite a bit of arcane instructions. 

We implemented a simple interpreter (in Python too) running the code to make sure
we understood the opcodes correctly. And yep, it returned the same result as the original
binary (though a couple of times slower).

We definitely need to optimize the code a bit, but it's a bit hard to read. We can improve
readability by skipping the `jmp xxx` bit if the target of the jump is the next instruction.
Also, there are some instructions like:
```
108: if (rA!=0){ rA--; jmp 108;} else jmp 109;
```
We can easily translate it to:
```
108: rA=0;
```
This also improves performance! I also added empty line before each fork target, to 
visually separate "subroutines".

New, slightly more readable code:
```
00: if (rA!=0){ rA--; } else jmp 02
01: rB++; jmp 00;
02: rC++; 
03: rC++; 
04: rC++; 
05: rC++; 
06: rC++; 
07: rC++; 
08: rC++; 
09: rC++; 
10: rC++; 
11: rC++; 
12: rC++; 
13: fork @ 108; copy up to rB; jmp 14;
14: if (rA!=0){ rA--; jmp 119;} else 
15: fork @ 20; copy up to rB; jmp 16;
16: rC=0; 
17: if (rA!=0){ rA--; } else jmp 19
18: rC++; jmp 17;
19: fork @ 64; copy up to rB; jmp 119;

20: rC=0; 
21: fork @ 29; copy up to rB; jmp 22;
22: if (rA!=0){ rA--; } else jmp 24
23: rC++; jmp 22;
24: if (rB!=0){ rB--; } else jmp 26
25: if (rZ!=0){ rZ--; jmp 00;} else jmp 21
26: rA=0; 
27: if (rC!=0){ rC--; } else jmp 119
28: rA++; jmp 27;

29: rC=0; 
30: fork @ 84; copy up to rB; jmp 31;
31: rD=0; 
32: if (rA!=0){ rA--; } else jmp 34
33: rD++; jmp 32;
34: if (rD!=0){ rD--; } else jmp 42
35: if (rD!=0){ rD--; } else jmp 42
36: fork @ 45; copy up to rB; jmp 37;
37: rC++; 
38: rB=0; 
39: if (rA!=0){ rA--; } else jmp 41
40: rB++; jmp 39;
41: if (rZ!=0){ rZ--; jmp 00;} else jmp 30
42: rA=0; 
43: if (rC!=0){ rC--; } else jmp 119
44: rA++; jmp 43;

45: rC=0; 
46: fork @ 84; copy up to rB; jmp 47;
47: if (rA!=0){ rA--; } else jmp 49
48: rC++; jmp 47;
49: fork @ 92; copy up to rC; jmp 50;
50: if (rB!=0){ rB--; } else jmp 119
51: rA=0; 
52: rB=0; 
53: if (rC!=0){ rC--; } else jmp 55
54: rB++; jmp 53;
55: fork @ 84; copy up to rB; jmp 56;
56: if (rA!=0){ rA--; } else jmp 58
57: rC++; jmp 56;
58: fork @ 84; copy up to rB; jmp 59;
59: if (rB!=0){ rB--; } else jmp 61
60: rA++; jmp 59;
61: if (rC!=0){ rC--; } else jmp 63
62: rA++; jmp 61;
63: rA++; jmp 119;

64: fork @ 84; copy up to rB; jmp 65;
65: rD=0; 
66: if (rA!=0){ rA--; } else jmp 68
67: rD++; jmp 66;
68: if (rD!=0){ rD--; } else jmp 119
69: rA++; 
70: if (rD!=0){ rD--; } else jmp 119
71: if (rB!=0){ rB--; } else jmp 119
72: fork @ 64; copy up to rB; jmp 73;
73: rE=0; 
74: if (rA!=0){ rA--; } else jmp 76
75: rE++; jmp 74;
76: if (rB!=0){ rB--; } else jmp 119
77: fork @ 64; copy up to rB; jmp 78;
78: if (rA!=0){ rA--; } else jmp 80
79: rE++; jmp 78;
80: rB=0; 
81: if (rE!=0){ rE--; } else jmp 83
82: rB++; jmp 81;
83: fork @ 99; copy up to rB; jmp 119;

84: rA=0; 
85: if (rB!=0){ rB--; } else jmp 119
86: rA++; jmp 85;
87: rA=0; 
88: if (rB!=0){ rB--; } else jmp 90
89: rA++; jmp 88;
90: if (rC!=0){ rC--; } else jmp 119
91: rA++; jmp 90;

92: rA=0; 
93: rB=0; 
94: if (rC!=0){ rC--; } else jmp 119
95: if (rC!=0){ rC--; } else jmp 98
96: rA++; 
97: if (rZ!=0){ rZ--; jmp 00;} else jmp 94
98: rB++; jmp 119;

99: fork @ 108; copy up to rB; jmp 100;
100: if (rA!=0){ rA--; } else jmp 103
101: if (rB!=0){ rB--; } else jmp 119
102: rA++; jmp 101;
103: fork @ 113; copy up to rB; jmp 104;
104: rB=0; 
105: if (rA!=0){ rA--; } else jmp 107
106: rB++; jmp 105;
107: if (rZ!=0){ rZ--; jmp 00;} else jmp 99

108: rA=0; 
109: if (rC!=0){ rC--; } else jmp 119
110: if (rB!=0){ rB--; } else jmp 112
111: if (rZ!=0){ rZ--; jmp 00;} else jmp 108
112: rA++; jmp 119;

113: if (rC!=0){ rC--; } else jmp 116
114: if (rB!=0){ rB--; } else jmp 119
115: if (rZ!=0){ rZ--; jmp 00;} else jmp 113
116: rA=0; 
117: if (rB!=0){ rB--; } else jmp 119
118: rA++; jmp 117;
```

Now, we needed to slowly analyze what each function does. We can either do this black
box style (using a lot of inputs and analyzing output to guess a function), or white box
(just analyze each instruction properly). We ended up doing it the latter way, as functions
are short enough not to be painful to analyze.

We started at leaf functions, i.e. ones without forks in themselves. For example function
at 113:
```
113: if (rC!=0){ rC--; } else jmp 116
114: if (rB!=0){ rB--; } else jmp 119
115: if (rZ!=0){ rZ--; jmp 00;} else jmp 113
116: rA=0; 
117: if (rB!=0){ rB--; } else jmp 119
118: rA++; jmp 117;
```
It can be literally transcribed to:
```
while true:
  if rC != 0:   # 113
    rC--
    if rB != 0: # 114
      rB--
    else:
      return
    continue
  else:
    break

rA = 0       # 116
while true:
  if rB != 0:
    rB--
    rA++
  else:
    break
```
It's pretty weird code, but putting loop-ending conditions in the `while` condition 
and ignoring useless assignments makes it better:
```
while rC != 0:
  rC--
  rB--
rA = 0
while rB != 0:
  rA++
  rB--
```
With code written as such, we can recognize the function as subtraction - `rA = rB-rC`.
The `rA` register is then copied to the main, non-forked function as a return value.

Now that we know what this function does, we can patch our interpreter to make it run 
faster by adding a special case to its main loop:
```python
if pc == 113:
    regs[0] = regs[1]-regs[2]
    break
```
This has somewhat sped up calculations. Without reversing all the functions though,
the calculation is still way too slow.

I won't write up how to reverse all the functions - I'll just summarize what each of them does
(roughly in the order I reversed them):

```
113: return rB-rC;
108: return rC>rB;
99: return rB mod rC;  (this was calculated by repeated subtraction of rC from rB)
84: return rB;         (this might seem unnecessary, but it's used as a means 
                        of copying a register)
92: return rC/2, rC%2; (this function is unique in that it returns two values in rA and rB)
45: if rB%2 == 0:
      return rB/2;
    else:
      return rB*3+1;   (a.k.a. Collatz sequence)
29: return total_stopping_time(rB); (a.k.a. number of iterations we need to apply
                                     Collatz function, until we get a 1)
20: return sum(total_stopping_time(i) for i in 1..n)
64: return fibonacci(rB) % rC (originally calculated in exponential time - recursively)
0: return fibmod(arg, sumcollatz(arg))
```

We implemented all of these shortcuts in our interpreter, but it was still very slow.
We were able to calculate an answer up to maybe a couple millions, but after that it was 
too much waiting. Instead, we rewrote the final function to C++ code. We also memoized
all the Collatz stopping times for all integers up to a billion - it took 2GB of RAM, but
sped up calculations significantly. In the end, the C++ code printed the flag after just
a couple of minutes.

The disassembler and sped up interpreter is in `parse.py` file, while the final C++
solver is in `fast.cpp` file. Python code gets its argument as command line argument,
while C++ one reads it from stdin.
