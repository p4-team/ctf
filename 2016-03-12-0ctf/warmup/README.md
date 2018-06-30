## Warmup (pwn, 2p)
	
	warmup for pwning!
	Notice: This service is protected by a sandbox, you can only
	read the flag at /home/warmup/flag
	
We were given small [Linux binary](warmup):
```
warmup: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), statically linked, BuildID[sha1]=c1791030f336fcc9cda1da8dc3a3f8a70d930a11, stripped
```

### Vulnerability

The file is 724 bytes long.
For such small files, usual strategy is to start by understanding the code in order to identify vulnerability.

We used IDA to disassemble the binary.
Soon we identified classic buffer-overflow in subroutine 0x0804815A:
```
.text:0804815A read_user_data  proc near               ; CODE XREF: start+2Bp
.text:0804815A
.text:0804815A fd              = dword ptr -30h
.text:0804815A addr            = dword ptr -2Ch
.text:0804815A len             = dword ptr -28h
.text:0804815A buffer          = byte ptr -20h
.text:0804815A
.text:0804815A                 sub     esp, 30h
.text:0804815D                 mov     [esp+30h+fd], 0 ; fd
.text:08048164                 lea     eax, [esp+30h+buffer]
.text:08048168                 mov     [esp+30h+addr], eax ; addr
.text:0804816C                 mov     [esp+30h+len], 34h ; len
.text:0804816C                                         ; VULNERABILITY: len > sizeof(buffer)
.text:08048174                 call    sys_read
.text:08048179                 mov     [esp+30h+fd], 1 ; fd
.text:08048180                 mov     [esp+30h+addr], offset aGoodLuck ; "Good Luck!\n"
.text:08048188                 mov     [esp+30h+len], 0Bh ; len
.text:08048190                 call    sys_write
.text:08048195                 mov     eax, 0DEADBEAFh
.text:0804819A                 mov     ecx, 0DEADBEAFh
.text:0804819F                 mov     edx, 0DEADBEAFh
.text:080481A4                 mov     ebx, 0DEADBEAFh
.text:080481A9                 mov     esi, 0DEADBEAFh
.text:080481AE                 mov     edi, 0DEADBEAFh
.text:080481B3                 mov     ebp, 0DEADBEAFh
.text:080481B8                 add     esp, 30h
.text:080481BB                 retn
.text:080481BB read_user_data  endp
```

The identified vulnerability allows for reading 0x14 bytes after end of buffer.
This includes return address from this subroutine that is stored on stack.

We didn't find any other vulnerabilities in provided binary.

### Exploitation Approach

We started the binary and captured process memory map of the process when vulnerable function is executing:
```
# cat /proc/[PID]/maps
08048000-08049000 r-xp 00000000 00:13 924601                             /root/ctf/warmup/fix
08049000-0804a000 rw-p 00000000 00:13 924601                             /root/ctf/warmup/fix
f77ce000-f77d0000 r--p 00000000 00:00 0                                  [vvar]
f77d0000-f77d1000 r-xp 00000000 00:00 0                                  [vdso]
ffe1b000-ffe3c000 rw-p 00000000 00:00 0                                  [stack]
```

It looks as we don't have any WRITE+EXECUTE pages.
Repeating this second time shows that locations other than binary itself are randomized.

For such cases, typical approach is by using gadgets that may be present in the binary itself.

### Exploit Implementation

The identified vulnerability allows for controlling just 0x10 bytes after the overwritten return address.
Searching for available gadgets indicates that task difficulty is to construct useful ROP chain in controlled buffer.
E.g. if we use subroutine 0x0804811D to read additional data, there are too few available bytes left for opening and reading flag file.

To overcome this limitation we decided to return back to program entry at 0x080480D8 instead.
This allows for filling longer stack area by repeatedly overflowing the buffer, such that each read is lower down the stack.
Once complete ROP is ready, we jump to the first gadget.

The ROP chain has the following steps:

1. read string */home/warmup/flag* into data area of exploited binary
2. write *SYS_open* bytes using 0x08048135 to set eax register
3. execute 0x08048122 that performs syscall using pre-set eax, this will open */home/warmup/flag* for read
4. read content of flag file using data area of exploited binary as buffer, we assume that file opened in previous step uses descriptor 3
5. write content of buffer to standard output

Attached [exploit.py](exploit.py) was used to retrieve flag during CTF.
