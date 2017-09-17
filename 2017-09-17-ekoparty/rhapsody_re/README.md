# Warmup (RE, 415p, 52 solved)

Another classic reversing challenge.
We get a [binary](rhapsody), ELF x64, statically compiled.

Just like in warmup we can see a permutated flag in the strings:

```asm
00000000004a2739         db  0x73 ; 's'                                         ; DATA XREF=sub_400a59+28, sub_400bf4+28, sub_400d0c+28, sub_4010e0+28
00000000004a273a         db  0x00 ; '.'
00000000004a273b         db  0x31 ; '1'                                         ; DATA XREF=sub_400a9f+28, sub_400bae+28
00000000004a273c         db  0x00 ; '.'
00000000004a273d         db  0x34 ; '4'                                         ; DATA XREF=sub_400ae5+28, sub_400b68+28, sub_40116c+28, sub_4011f8+28, sub_401310+28
00000000004a273e         db  0x00 ; '.'
00000000004a273f         db  0x74 ; 't'                                         ; DATA XREF=sub_400c3a+28
00000000004a2740         db  0x00 ; '.'
00000000004a2741         db  0x4b ; 'K'                                         ; DATA XREF=sub_400c80+28
00000000004a2742         db  0x00 ; '.'
00000000004a2743         db  0x68 ; 'h'                                         ; DATA XREF=sub_400cc6+28
00000000004a2744         db  0x00 ; '.'
00000000004a2745         db  0x72 ; 'r'                                         ; DATA XREF=sub_400d52+28, sub_400fc8+28
00000000004a2746         db  0x00 ; '.'
00000000004a2747         db  0x7b ; '{'                                         ; DATA XREF=sub_400d98+28
00000000004a2748         db  0x00 ; '.'
00000000004a2749         db  0x33 ; '3'                                         ; DATA XREF=sub_400dde+28, sub_40100e+28
00000000004a274a         db  0x00 ; '.'
00000000004a274b         db  0x4f ; 'O'                                         ; DATA XREF=sub_400e24+28
00000000004a274c         db  0x00 ; '.'
00000000004a274d         db  0x6c ; 'l'                                         ; DATA XREF=sub_400e6a+28, sub_400ef6+28
00000000004a274e         db  0x00 ; '.'
00000000004a274f         db  0x66 ; 'f'                                         ; DATA XREF=sub_400eb0+28, sub_4011b2+28
00000000004a2750         db  0x00 ; '.'
00000000004a2751         db  0x67 ; 'g'                                         ; DATA XREF=sub_400f3c+28
00000000004a2752         db  0x00 ; '.'
00000000004a2753         db  0x30 ; '0'                                         ; DATA XREF=sub_400f82+28
00000000004a2754         db  0x00 ; '.'
00000000004a2755         db  0x6a ; 'j'                                         ; DATA XREF=sub_401054+28
00000000004a2756         db  0x00 ; '.'
00000000004a2757         db  0x75 ; 'u'                                         ; DATA XREF=sub_40109a+28
00000000004a2758         db  0x00 ; '.'
00000000004a2759         db  0x37 ; '7'                                         ; DATA XREF=sub_401126+28, sub_401284+28
00000000004a275a         db  0x00 ; '.'
00000000004a275b         db  0x6e ; 'n'                                         ; DATA XREF=sub_40123e+28
00000000004a275c         db  0x00 ; '.'
00000000004a275d         db  0x7d ; '}'                                         ; DATA XREF=sub_4012ca+28
```

And again we can find a very nice pattern for checking the flag:

```asm
000000000040137c         mov        eax, 0x0
0000000000401381         call       sub_400b2b
0000000000401386         test       eax, eax
0000000000401388         jne        loc_401394

000000000040138a         mov        eax, 0x0
000000000040138f         jmp        loc_4016a0

                     loc_401394:
0000000000401394         mov        eax, 0x0                                    ; CODE XREF=sub_401378+16
0000000000401399         call       sub_400c80
000000000040139e         test       eax, eax
00000000004013a0         jne        loc_4013ac

00000000004013a2         mov        eax, 0x0
00000000004013a7         jmp        loc_4016a0

                     loc_4013ac:
00000000004013ac         mov        eax, 0x0                                    ; CODE XREF=sub_401378+40
00000000004013b1         call       sub_400e24
00000000004013b6         test       eax, eax
00000000004013b8         jne        loc_4013c4

00000000004013ba         mov        eax, 0x0
00000000004013bf         jmp        loc_4016a0
```

and more similar checks.
Jump `jmp loc_4016a0` means of course we failed to get the character right.
Fortunately for us the functions we are calling here are all basically the same:

```asm
                     sub_400c80:
0000000000400c80         push       rbp                                         ; CODE XREF=sub_401378+33
0000000000400c81         mov        rbp, rsp
0000000000400c84         mov        eax, 0x0
0000000000400c89         call       sub_4009d3
0000000000400c8e         mov        byte [0x6cee20], al
0000000000400c94         mov        eax, 0x6cee41
0000000000400c99         movzx      edx, byte [rax]
0000000000400c9c         mov        eax, 0x4a2741
0000000000400ca1         movzx      eax, byte [rax]
0000000000400ca4         cmp        dl, al
0000000000400ca6         jne        loc_400cbf

0000000000400ca8         mov        eax, dword [0x6cdc70]
0000000000400cae         xor        eax, 0x5
0000000000400cb1         mov        dword [0x6cdc70], eax
0000000000400cb7         mov        eax, dword [0x6cdc70]
0000000000400cbd         jmp        loc_400cc4

                     loc_400cbf:
0000000000400cbf         mov        eax, 0x0                                    ; CODE XREF=sub_400c80+38

                     loc_400cc4:
0000000000400cc4         pop        rbp                                         ; CODE XREF=sub_400c80+61
0000000000400cc5         ret
                        ; endp
```

This function simply loads our input byte and then compares it with expected flag byte.
And those functions go in order!
There is a call to some strange function here, but in the end it doesn't matter, so no point bothering with it.

There was a small difference for the first check, because the function was a bit different, but we know the first character of the flag is `E` so we simply start with the second one.

This looks like a nice target for angr, but we couldn't run it, just like for warmup, so we did a gdb script one more time.

What we want to do:

1. Stop when the pattern of cmp-then-jump starts.
2. Step into the function.
3. Move to the `cmp` and check what input was expected, save it as flag byte.
4. Change our input byte for the expected one, so the checks pass and we can proceed.
5. Move to the next check.

We run:

```python
import gdb
import codecs
import string

flag = []
gdb.execute("break *0x401399")
gdb.execute("r <<< $(echo 'Eaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')")
for i in range(32):
    gdb.execute("s")
    for j in range(9):
        gdb.execute("n")
    character = chr(int(str(gdb.parse_and_eval("$al")),16))
    flag.append(character)
    gdb.execute("set $dl = $al")
    for j in range(12):
        gdb.execute("n")
print('E'+"".join(flag))
```

And we get: `EKO{1sth1sr34lfl4g0rjus7f4n74s34}`
