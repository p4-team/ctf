# Russian threesome, re, 5 solves, 500p

> Interested in the hot secret hidden in my basement? That's right, it's stored on this old computer. Unfortunately it stopped working a long time ago. However I've got an emulator that simulates this machine and I even was able to dump it's magnetic drum into a file. I'm sure that way extracting the juicy data should be easy, right? 


As the description stated, we got two files: a compiled emulator and image of a magnetic drum. Reversing the emulator was the first part of the
challenge.

As it turns out, the emulated architecture is pretty interesting. It uses balanced ternary encoding for everything, organized into 9-trit mini-words ("trytes"),
two of which make a word. There are 27 words in a sector. The whole drum is composed of 36 sectors.

The machine contains a few registers and memory objects:
- sectors X, Y, Z - three of drum sectors can be loaded into memory at the same time,
- accumulator (A), used generally as tryte-sized object,
- secondary accumulator (B), used for multiplication etc.
- program counter (PC), five-trit sized (selects X/Y/Z, one of 27 words, one of trytes; must not have -1 as LSB)
- flag (F), one trit of last operation sign
- indirection register (V), five-trit sized

Program counter always increments after the instruction, even if it was a jump (so jump target is actually one after what is encoded). All instructions
are tryte-sized and have the same composition: 3-trit opcode, 5-trit immediate, 1-trit indirection flag. If indirection flag is non-zero, the
indirection register is added to immediate field. This behavior allows for indirect indexing, for example `A = [V+20]` (other than by using V, all instructions
use constant addresses).

The machine has a few allowances for IO: audio (interprets X/Y/Z as speaker tones), puts and gets (reads or writes string into X/Y/Z). The machine
has specific charset, where bytes lower than 128 are ASCII and 128-255 are custom Russian characters.

There is quite a few opcodes, but they are mostly variations of the same:

```
X/Y/Z = drumsector n
audio X/Y/Z
puts X/Y/Z
gets X/Y/Z
drumsector n = X/Y/Z
shift A, Tn
mov Tn, A
add V, Tn
mov V, Tn
mov V, pc+Tn
mov Tn, V
jmp Tn
mov Tn, pc
jneg Tn
jzer Tn
jpos Tn
halt
and A, Tn
mov B, Tn
sub A, Tn
mov A, Tn
add A, Tn
mov A, Tn + A * B
mul A, Tn
add A, Tn * B
```

There are no instructions for loading a register with a constant, so instead the constants are store in memory and loaded as Tn.

Now that the emulator is reversed, we wrote a disassembler and reversed the drum code.

Since the machine lacks convenient stack, or even call/ret instructions, these are implemented in software in sector 1. This sector is loaded most
of the time into sector X and allows simpler sector switching. Sector Y is devoted to currently executed code, and sector Z to data being operated on.

Running the emulator we see a menu and admin panel protected by a password. Reversing the code shows it calculates a simple hash based on
256-byte substitution table - though due to architecture quirks this takes hundreds of instructions and many thousands of cycles. The hash was
reversible, so we wrote a script to calculate the inverse, which when put into the emulator got us the flag:

```
ak@ak-VirtualBox:~$ ./emulator magnetic_drum.img 
Добро пожаловать!

Меню:
1. Коробейники
2. Сведения
3. Админка
4. Остановить
3
Введите пароль: Кто хочет много знать, тому мало спать.
flag{put_your_trits_inside_my_drum}
```



