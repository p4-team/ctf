# ummmfpu

> Reverse Engineering, 400
>
> Difficulty: medium (9 solvers)
>
> So I found this Micromega FPU in my drawer, connected it to an Arduino Uno and programmed it to validate the flag.

In this task we are given an Arduino code. It is connected to a Micromega FPU and sends
firmware to it; then it sends flag and makes the firmware validate it.

The whole task reduces to reverse engineering the FPU assembly. There is no disassembler
easily available, but there's a documentation of the coprocessor instruction
set at: http://micromegacorp.com/downloads/documentation/uMFPU-V3_1%20Instruction%20Set.pdf.

After parsing the documentation and writing a rudimentary disassembler, we reverse
engineered the firmware. It was self-modifying (xoring a few functions with a constant),
so the disassembler inverted the transformation.

The FPU had a few odd instructions, like matrix operations (transposing) or
string operations (splitting on given character). In the end, the algorithm
was quite simple and involved xoring with an LCG and comparing to a constant buffer.
