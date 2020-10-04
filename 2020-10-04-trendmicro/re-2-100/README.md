# Reversing-II 100 (NES reverse engineering)

We are provided with a NES ROM (`impossible_game.nes`). The goal is simple - find a cheat code for walking through walls. The hints explain that we should flip only one bit in a data section of the ROM.

We would ideally avoid reversing the entire game, as that would take forever - especially for a 100 point challenge. I decided to instrument an emulator to find the instructions responsible for handling the collision.

After failing to figure out how to open a ROM in higan, I cloned the source for FCEUX. As the emulator is available in `nixpkgs`, building it was a piece of cake:

```shell
[~/ctf/2020/trendmicro/nes-re/fceux]$ nix-shell '<nixpkgs>' -A fceux
[nix-shell:~/ctf/2020/trendmicro/nes-re/fceux]$ $buildPhase
```

(unfortunately this includes a non-idempotent patch to `SConstruct`, repeated builds had to be done with `git checkout SConstruct;$buildPhase`)

Some strategic source spelunking quickly lead me to the code responsible for dispatching an instruction:

```cpp
   // x6502.cpp, in X6502_Run, around line 490
   IncrementInstructionsCounters();

   _PI=_P;
   b1=RdMem(_PC);

   ADDCYC(CycTable[b1]);
```

I added some quick-n-dirty logging to print a line each time an instruction at a specific address is reached for the first time:

```diff
   // x6502.cpp, in X6502_Run, around line 490
   IncrementInstructionsCounters();

   _PI=_P;

+  static bool seenPC[0x10000] = {0};
+  if (!seenPC[_PC]) {
+      printf("New PC: 0x%04x\n", _PC);
+      seenPC[_PC]=1;
+  }

   b1=RdMem(_PC);

   ADDCYC(CycTable[b1]);
```

I recompiled the emulator and fired up the game, fully prepared to get spammed by a large amount of output. I made sure to move my character both ways, but avoid colliding with the wall. Then, I applied the age-old technique of marking a point in the output of a CLI program by pressing Enter a few times and finally walked into the wall. This yielded the following, quite short output:

```
New PC: 0x94af
New PC: 0x94b1
New PC: 0x92d7
New PC: 0x92d9
New PC: 0x9309
New PC: 0x930b
New PC: 0x930e
New PC: 0x9311
New PC: 0x9314
New PC: 0x9315
New PC: 0x9317
```

I've set out to obtain the disassembly of these addresses. Unfortunately, the Linux version of FCEUX includes only the most basic UI, but the Windows build runs just fine in `wine`, and contains an intuitive debugger. Trying not to get distracted by the code textbox using a non-monospace font (probably a Wine quirk :P), I used "seek PC" to find this code:

```
 00:94A9:A5 31     LDA $0031 = #$C0
 00:94AB:29 40     AND #$40
 00:94AD:F0 04     BEQ $94B3 ------- jumps-.
 00:94AF:E6 33     INC $0033 = #$00         \    <- only runs on collision
 00:94B1:E6 34     INC $0034 = #$00         |    <-
 00:94B3:AD E9 04  LDA $04E9 = #$C4 <- here '
```

As we can see, the collision flags at this moment are stored in address `$31` of the zeropage, and bit `$40` corresponds to the collision we want to avoid. I've added a write watchpoint at `$0031` to find that it's only written in these two places:

```
 00:9739:A4 36     LDY $0036 = #$C4
 00:973B:B9 F8 03  LDA $03F8,Y @ $04BC = #$00
 00:973E:85 31     STA $0031 = #$C0            <-- useless write
 00:9740:A4 31     LDY $0031 = #$C0                read it again immediately (ever heard about TAY?)
 00:9742:B9 14 99  LDA $9914,Y @ $99D8 = #$00      index into a table
 00:9745:85 31     STA $0031 = #$C0            <-- remember the flags
```

Looks like we need to overwrite the byte at `$9914+Y`. But what's Y when the collision occurs? When it finally happens, the register will surely have already been overwritten a hundred times over, and if we place a breakpoint around `00:9745`, there's no way to know whether it's actually the interesting collision being evaluated (maybe it's just the floor?).

As FCEUX doesn't have any reverse-debugging features I know of, I decided to add another ad-hoc patch. First, whenever `$0031` is written, I remember the value of Y:

```diff
+uint8_t p4writeCollY = 0;

 static INLINE void WrRAM(unsigned int A, uint8 V)
 {
+        if (A == 0x0031) {
+            p4writeCollY = _Y;
+        }
         RAM[A]=V;
 }
```

Then, I print it when a new instruction is executed:

```cpp
printf("New PC: 0x%04x, [0x0031] = %02x, Y = %02x\n", _PC, RAM[0x31], p4writeCollY);
```

Repeating the same experiment, we obtain

```
New PC: 0x94af, [0x0031] = c0, Y = 02
New PC: 0x94b1, [0x0031] = c0, Y = 02
New PC: 0x92d7, [0x0031] = 00, Y = 00
New PC: 0x92d9, [0x0031] = 00, Y = 00
New PC: 0x9309, [0x0031] = 00, Y = 00
New PC: 0x930b, [0x0031] = 00, Y = 00
New PC: 0x930e, [0x0031] = 00, Y = 00
New PC: 0x9311, [0x0031] = 00, Y = 00
New PC: 0x9314, [0x0031] = 00, Y = 00
New PC: 0x9315, [0x0031] = 00, Y = 00
New PC: 0x9317, [0x0031] = 00, Y = 00
```

Looks like we need to patch `$9916`, then. Careful to take into account the iNES header and ROM load address, we try our modification out:

```python
>>> d = open('impossible_game.nes', 'rb').read()
>>> d = bytearray(d)
>>> d[0x1926] = 0x80
>>> open('possible_game.nes', 'wb').write(d)
```

This lets us walk right through the wall. As a finishing stretch, we use the `Game Genie Decoder/Encoder` tool included in `fceux.exe` to turn our findings into a cheat code, which is also the flag:

```
TMCTF{EAOPVPEG}
```
