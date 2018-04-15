Gibson 9000 Calcumatron.

Caving under the pressure of environmentalists, the Gibson inc. CPU
manufacturing company is working on a new line of processors in order to
decrease power consumption and cooling requirements, while still increasing
the amount of Jigawatts.

The current Gibson 9000 CPU design uses only uses 6 instructions, thereby
obviously reducing operating costs.  The Gibson 9000 incorporates bleeding-edge
automatic thermal throttling, but also advances the state-of-the-art through
its faster and more efficient "Meditation" mode. 

Our CPU has read-only program memory, 128 bytes of read-write data memory, an
instruction pointer and a data pointer.

The Gibson 9000 instructions are 2 octets wide and include one opcode and one
parameter.  For instance, the instruction "+5" (0x2B, 0x35) executes opcode
0x2B with parameter 0x35. Aside for 0x2A and 0x2B, the parameter for all other
instructions is ignored.

The opcodes are as follows:

0x2A	'*'		Add parameter to the value pointed out by the data pointer.
0x2B	'+'		Add parameter to the data pointer
0x5F	'_'		Conditional jump when the value pointed at by the data pointer is 0x00, otherwise skip
0x58	'X'		Output the data region
0x4D	'M'		Meditate to cool down the CPU
0x44	'D'		Toggle debugging mode

The possible parameters are:

0x30	'0'		value 0
0x31	'1'		value 1
0x32	'2'		value 2
0x33	'3'		value 3
0x34	'4'		value 4
0x35	'5'		value 5
0x36	'6'		value 6
0x37	'7'		value 7
0x38	'8'		value negative 0
0x39	'9'		value negative 1
0x41	'A'		value negative 2
0x42	'B'		value negative 3
0x43	'C'		value negative 4
0x44	'D'		value negative 5
0x45	'E'		value negative 6
0x46	'F'		value negative 7


For faster adoption, Gibson inc. provides an emulator of the new CPU
architecture so that all your banking software can already be converted to more
efficient opcodez.

Disclaimer: our emulator was written by an intern who was more occupied with
riding his skateboard than producing quality work. Please don't send viruses.
