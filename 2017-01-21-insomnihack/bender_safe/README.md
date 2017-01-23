# Bender Safe (re, 50 points)

Binary provided in challenge is 32bit MIPS, which is a bit unusual, and makes reversing harder.

We can connect to challenge server, but it wants us to provide some OTP key:

    $ nc bender_safe.teaser.insomnihack.ch 31337
    Welcome to Bender's passwords storage service
    Here's your OTP challenge : 
    IMYTSAAAUI87YIQU

After a while of reverse-engineering, we have found that there is only one function that matter (named aptly `validate`).

Checks are performed one-by-one, but characters are checked out-of-order (so naively bruteforcing password by tracing program and counting instructions will not work).

For example, second check looks like this:

```asm
.text:00401E0C loc_401E0C:                              # CODE XREF: validate+184
.text:00401E0C                 lw      $v1, 0x60+dead($fp)
.text:00401E10                 lw      $v0, 0x60+babe($fp)
.text:00401E14                 mult    $v1, $v0
.text:00401E18                 mflo    $v0
.text:00401E1C                 sw      $v0, 0x60+deadXbabe($fp)
.text:00401E20                 lw      $v1, 0x60+defe($fp)
.text:00401E24                 lw      $v0, 0x60+cate($fp)
.text:00401E28                 mult    $v1, $v0
.text:00401E2C                 mflo    $v0
.text:00401E30                 sw      $v0, 0x60+defeXcate($fp)
.text:00401E34                 lw      $v1, 0x60+dead2($fp)
.text:00401E38                 lw      $v0, 0x60+beef($fp)
.text:00401E3C                 mult    $v1, $v0
.text:00401E40                 mflo    $v0
.text:00401E44                 sw      $v0, 0x60+deadXbeef($fp)
.text:00401E48                 lw      $v1, 0x60+deadXbabe($fp)
.text:00401E4C                 lw      $v0, 0x60+babe($fp)
.text:00401E50                 divu    $v1, $v0
.text:00401E54                 teq     $v0, $zero  #7
.text:00401E58                 mfhi    $v1
.text:00401E5C                 mflo    $v0
.text:00401E60                 sw      $v0, 0x60+var_24($fp)
.text:00401E64                 lw      $v1, 0x60+defeXcate($fp)
.text:00401E68                 lw      $v0, 0x60+cate($fp)
.text:00401E6C                 divu    $v1, $v0
.text:00401E70                 teq     $v0, $zero  #7
.text:00401E74                 mfhi    $v1
.text:00401E78                 mflo    $v0
.text:00401E7C                 sw      $v0, 0x60+var_20($fp)
.text:00401E80                 lw      $v1, 0x60+deadXbeef($fp)
.text:00401E84                 lw      $v0, 0x60+beef($fp)
.text:00401E88                 divu    $v1, $v0
.text:00401E8C                 teq     $v0, $zero  #7
.text:00401E90                 mfhi    $v1
.text:00401E94                 mflo    $v0
.text:00401E98                 sw      $v0, 0x60+var_1C($fp)
.text:00401E9C                 lw      $v1, 0x60+var_24($fp)
.text:00401EA0                 lw      $v0, 0x60+dead($fp)
.text:00401EA4                 divu    $v1, $v0
.text:00401EA8                 teq     $v0, $zero  #7
.text:00401EAC                 mfhi    $v1
.text:00401EB0                 mflo    $v0
.text:00401EB4                 move    $v1, $v0
.text:00401EB8                 lw      $v0, 0x60+var_20($fp)
.text:00401EBC                 mult    $v1, $v0
.text:00401EC0                 mflo    $v1
.text:00401EC4                 lw      $v0, 0x60+defe($fp)
.text:00401EC8                 move    $at, $at
.text:00401ECC                 divu    $v1, $v0
.text:00401ED0                 teq     $v0, $zero  #7
.text:00401ED4                 mfhi    $v1
.text:00401ED8                 mflo    $v0
.text:00401EDC                 move    $v1, $v0
.text:00401EE0                 lw      $v0, 0x60+var_1C($fp)
.text:00401EE4                 mult    $v1, $v0
.text:00401EE8                 mflo    $v1
.text:00401EEC                 lw      $v0, 0x60+dead2($fp)
.text:00401EF0                 move    $at, $at
.text:00401EF4                 divu    $v1, $v0
.text:00401EF8                 teq     $v0, $zero  #7
.text:00401EFC                 mfhi    $v1
.text:00401F00                 mflo    $v0
.text:00401F04                 sw      $v0, 0x60+deadXbabe($fp)
.text:00401F08                 lw      $v1, 0x60+arg_4($fp)
.text:00401F0C                 lw      $v0, 0x60+deadXbabe($fp)
.text:00401F10                 addu    $v0, $v1, $v0
.text:00401F14                 lb      $v1, 0($v0)
.text:00401F18                 lw      $v0, 0x60+arg_0($fp)
.text:00401F1C                 addiu   $v0, 0xF
.text:00401F20                 lb      $v0, 0($v0)
.text:00401F24                 beq     $v1, $v0, loc_401F5C
.text:00401F28                 move    $at, $at
.text:00401F2C                 lui     $v0, 0x48  # 'H'
.text:00401F30                 addiu   $a0, $v0, (aNope_0 - 0x480000)  # "Nope!"
.text:00401F34                 la      $v0, puts
.text:00401F38                 move    $t9, $v0
.text:00401F3C                 jalr    $t9 ; puts
.text:00401F40                 move    $at, $at
.text:00401F44                 lw      $gp, 0x60+var_50($fp)
.text:00401F48                 li      $a0, 1
.text:00401F4C                 la      $v0, exit
.text:00401F50                 move    $t9, $v0
.text:00401F54                 jalr    $t9 ; exit
.text:00401F58                 move    $at, $at
```

This looks overwhelming, but most of the opcodes are useless.

Checks was rather trivial, so instead of trying to be smart, we've just reverse engineered everything the traditional way (using IDA Pro + qemu remote debugger), and came out with this OTP generator (challenge in argv[1]):

```python
import sys

mychars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

ss = sys.argv[1]

out = ''

out += ss[0]

out += ss[15]

if ord(ss[7]) >= 65:
    out += chr(ord(ss[7]) ^ 0x20)
else:
    out += chr(ord(ss[7]) ^ 0x40)

if ord(ss[3]) >= 65:
    ndx = mychars.find(ss[3])
    ndx = (ndx + 10) % len(mychars)
    out += mychars[ndx]
else:
    ndx = mychars.find(ss[3])
    ndx = (ndx - 10) % len(mychars)
    out += mychars[ndx]

if ord(ss[4]) >= 65:
    ndx = mychars.find(ss[4])
    ndx = (ndx + 10) % len(mychars)
    out += mychars[ndx]
else:
    ndx = mychars.find(ss[4])
    ndx = (ndx - 10) % len(mychars)
    out += mychars[ndx]

v25 = ord(ss[1]) - ord(ss[2])
if v25 >= 0:
    v26 = v25
else:
    v26 = -v25
out += mychars[v26 % (len(mychars) - 1)]

v25 = ord(ss[5]) - ord(ss[6])
if v25 >= 0:
    v26 = v25
else:
    v26 = -v25
out += mychars[v26 % (len(mychars) - 1)]

if ord(ss[8]) >= 65:
    out += chr(ord(ss[8]) ^ 0x20)
else:
    out += chr(ord(ss[8]) ^ 0x40)

print out
```
