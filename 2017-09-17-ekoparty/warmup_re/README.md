# Warmup (RE, 397p, 63 solved)

It's a classic reversing challenge.
We get a [binary](warmup), ELF x64, statically compiled.
In the strings we can see something resembling a permutated flag:

```asm
00000000004a171b         db  0x4f ; 'O'                                         ; DATA XREF=sub_4009d8+12
00000000004a171c         db  0x00 ; '.'
00000000004a171d         db  0x5f ; '_'                                         ; DATA XREF=sub_4009d8+36, sub_4009d8+276, sub_4009d8+300, sub_4009d8+396, sub_4009d8+564
00000000004a171e         db  0x00 ; '.'
00000000004a171f         db  0x75 ; 'u'                                         ; DATA XREF=sub_4009d8+60, sub_4009d8+588
00000000004a1720         db  0x00 ; '.'
00000000004a1721         db  0x74 ; 't'                                         ; DATA XREF=sub_4009d8+84, sub_4009d8+372
00000000004a1722         db  0x00 ; '.'
00000000004a1723         db  0x31 ; '1'                                         ; DATA XREF=sub_4009d8+108, sub_4009d8+228
00000000004a1724         db  0x00 ; '.'
00000000004a1725         db  0x7b ; '{'                                         ; DATA XREF=sub_4009d8+132
00000000004a1726         db  0x00 ; '.'
00000000004a1727         db  0x6a ; 'j'                                         ; DATA XREF=sub_4009d8+156
00000000004a1728         db  0x00 ; '.'
00000000004a1729         db  0x73 ; 's'                                         ; DATA XREF=sub_4009d8+180, sub_4009d8+252
00000000004a172a         db  0x00 ; '.'
00000000004a172b         db  0x68 ; 'h'                                         ; DATA XREF=sub_4009d8+204
00000000004a172c         db  0x00 ; '.'
00000000004a172d         db  0x3f ; '?'                                         ; DATA XREF=sub_4009d8+324
00000000004a172e         db  0x00 ; '.'
00000000004a172f         db  0x35 ; '5'                                         ; DATA XREF=sub_4009d8+348
00000000004a1730         db  0x00 ; '.'
00000000004a1731         db  0x34 ; '4'                                         ; DATA XREF=sub_4009d8+420, sub_4009d8+492
00000000004a1732         db  0x00 ; '.'
00000000004a1733         db  0x4b ; 'K'                                         ; DATA XREF=sub_4009d8+444
00000000004a1734         db  0x00 ; '.'
00000000004a1735         db  0x77 ; 'w'                                         ; DATA XREF=sub_4009d8+468
00000000004a1736         db  0x00 ; '.'
00000000004a1737         db  0x72 ; 'r'                                         ; DATA XREF=sub_4009d8+516
00000000004a1738         db  0x00 ; '.'
00000000004a1739         db  0x6d ; 'm'                                         ; DATA XREF=sub_4009d8+540
00000000004a173a         db  0x00 ; '.'
00000000004a173b         db  0x70 ; 'p'                                         ; DATA XREF=sub_4009d8+608
00000000004a173c         db  0x00 ; '.'
00000000004a173d         db  0x45 ; 'E'                                         ; DATA XREF=sub_4009d8+628
00000000004a173e         db  0x00 ; '.'
00000000004a173f         db  0x7d ; '}'                                         ; DATA XREF=sub_4009d8+648
```

If we look at how those values are used we can see a clear pattern:

```asm
00000000004009dc         mov        eax, 0x6ccd62
00000000004009e1         movzx      edx, byte [rax]
00000000004009e4         mov        eax, 0x4a171b
00000000004009e9         movzx      eax, byte [rax]
00000000004009ec         cmp        dl, al
00000000004009ee         jne        loc_400d58

00000000004009f4         mov        eax, 0x6ccd72
00000000004009f9         movzx      edx, byte [rax]
00000000004009fc         mov        eax, 0x4a171d
0000000000400a01         movzx      eax, byte [rax]
0000000000400a04         cmp        dl, al
0000000000400a06         jne        loc_400d51

0000000000400a0c         mov        eax, 0x6ccd6d
0000000000400a11         movzx      edx, byte [rax]
0000000000400a14         mov        eax, 0x4a171f
0000000000400a19         movzx      eax, byte [rax]
0000000000400a1c         cmp        dl, al
0000000000400a1e         jne        loc_400d4a

0000000000400a24         mov        eax, 0x6ccd67
0000000000400a29         movzx      edx, byte [rax]
0000000000400a2c         mov        eax, 0x4a1721
0000000000400a31         movzx      eax, byte [rax]
0000000000400a34         cmp        dl, al
0000000000400a36         jne        loc_400d43

0000000000400a3c         mov        eax, 0x6ccd69
0000000000400a41         movzx      edx, byte [rax]
0000000000400a44         mov        eax, 0x4a1723
0000000000400a49         movzx      eax, byte [rax]
0000000000400a4c         cmp        dl, al
0000000000400a4e         jne        loc_400d3c
```

and more checks like this following.
Target for the `jne` jump is finishing without printing "valid!".

It looks like a perfect binary for angr, but for some reason we had issues with running angr on it, and we decided it will be faster to do it just with gdb script, instead of trying to fix the angr issue.

What we want to do:

1. Break at the point in binary where the pattern of comparison-and-jump starts -> `0x4009dc`
2. Move to the point where address of our input byte is loaded and save this address, so that we know which byte was checked.
3. Move to comparison and save the expected byte value
4. Set our value to the expected one, so the comparison passes and we go to the next character
5. We now know which address of our input bytes was supposed to be a certain flag byte, and since those addresses are from a single memory block, we can just sort it to get the flag.

```python
import gdb
import codecs
import string

flag = []
gdb.execute("break *0x4009dc")
gdb.execute("r <<< $(echo 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')")
for i in range(28):
    for i in range(2):
        gdb.execute("n")
    addr = int(str(gdb.parse_and_eval("$eax")),16)
    for i in range(2):
        gdb.execute("n")
    value = chr(int(str(gdb.parse_and_eval("$eax")),16))
    flag.append((addr, value))
    gdb.execute("set $dl = $al")
    for i in range(2):
        gdb.execute("n")
gdb.execute("c")
flag = sorted(flag, key=lambda x: x[0])
print("".join([c[1] for c in flag]))
```

Which gives us the flag: `EKO{1s_th1s_ju5t_4_w4rm_up?}`
