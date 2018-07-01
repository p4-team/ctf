## Sandbox (pwn, 5p)
	
	Escape from this broken sandbox
	notice: You have to solve the warmup task first. And try to get
	the flag at /home/sandbox/flag
	
We were given small [Linux binary](sandbox):
```
sandbox: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=d833f31d8d8592636906d44b40da9bcdbc0d686b, stripped
```

Based on task title and description we suspect that Warmup challenge solved previously may be part of this tasks.
We verify this by run Warmup exploit against new server.

As expected, exploit successfully retrieved flag from */home/warmup/flag* file.
The same exploit however fails to retrieve */root/home/sandbox/flag*.
We suspect that in order to solve the tasks, we need to bypass sandbox implemented by the provided binary.

### Sandbox Analysis

We used Radare2 to disassemble the binary.
The binary implements simple sandbox that inspects syscalls from monitored binary using ptrace.
This functionality is implemented by subroutine 0x00400b50.

Syscall inspection is as follows:
```
|           0x00400c3e      488d742410     lea rsi, [rsp + 0x10]       ; struct user ctx
|           0x00400c43      89df           mov edi, ebx
|           0x00400c45      e876010000     call fcn.ptrace_getregs
|           0x00400c4a      488b84248800.  mov rax, qword [rsp + 0x88] ; ctx.regs.orig_rax
|           0x00400c52      4883f805       cmp rax, 5                  ; = SYS32_open
|       ,=< 0x00400c56      7466           je 0x400cbe                 ; additional logic
|       |   0x00400c58      4883f801       cmp rax, 1                  ; = SYS32_exit
|      ,==< 0x00400c5c      7467           je 0x400cc5                 ; allow
|      ||   0x00400c5e      488d50fd       lea rdx, [rax - 3]
|      ||   0x00400c62      4883fa01       cmp rdx, 1                  ; in (SYS32_read, SYS32_write)
|     ,===< 0x00400c66      765d           jbe 0x400cc5                ; allow
|     |||   0x00400c68      4883f806       cmp rax, 6                  ; = SYS32_close
|    ,====< 0x00400c6c      7457           je 0x400cc5                 ; allow
|    ||||   0x00400c6e      4883f81b       cmp rax, 0x1b               ; = SYS32_alarm
|   ,=====< 0x00400c72      7451           je 0x400cc5                 ; allow
|   |||||   0x00400c74      4883f85a       cmp rax, 0x5a               ; = SYS32_mmap
|  ,======< 0x00400c78      744b           je 0x400cc5                 ; allow
|  ||||||   0x00400c7a      4883f87d       cmp rax, 0x7d               ; = SYS32_mprotect
| ,=======< 0x00400c7e      7445           je 0x400cc5                 ; allow
| |||||||   0x00400c80      89df           mov edi, ebx
| |||||||   0x00400c82      be09000000     mov esi, 9
| |||||||   0x00400c87      e8e4faffff     call sym.imp.kill
| |||||||   0x00400c8c      31ff           xor edi, edi
| |||||||   0x00400c8e      e81dfbffff     call sym.imp.exit
```

The monitored process is allowed to execute:

* SYS32_open, with additional check described below
* SYS32_exit
* SYS32_read
* SYS32_write
* SYS32_close
* SYS32_alarm
* SYS32_mmap
* SYS32_mprotect

The additional check for *SYS32_open* is implemented by subroutine 0x00400aa0:
```
/ (fcn) fcn.sandbox_inspect_open 176
|           ; CALL XREF from 0x00400cc0 (fcn.sandbox_inspect_open)
|           0x00400aa0      53             push rbx
|           0x00400aa1      89fb           mov ebx, edi
|           0x00400aa3      4881ec001100.  sub rsp, 0x1100
|           0x00400aaa      488d742410     lea rsi, [rsp + 0x10]       ; struct user ctx
|           0x00400aaf      64488b042528.  mov rax, qword fs:[0x28]
|           0x00400ab8      48898424f810.  mov qword [rsp + 0x10f8], rax
|           0x00400ac0      31c0           xor eax, eax
|           0x00400ac2      e8f9020000     call fcn.ptrace_getregs
|           0x00400ac7      488b742438     mov rsi, qword [rsp + 0x38] ; ctx.regs.rbx
|           0x00400acc      488d9424f000.  lea rdx, [rsp + 0xf0]
|           0x00400ad4      4531c0         xor r8d, r8d
|           0x00400ad7      b900100000     mov ecx, 0x1000
|           0x00400adc      89df           mov edi, ebx
|           0x00400ade      e88d030000     call fcn.sandbox_read_vm
|           0x00400ae3      488dbc24f000.  lea rdi, [rsp + 0xf0]
|           0x00400aeb      31f6           xor esi, esi
|           0x00400aed      e86efcffff     call sym.imp.realpath       ; BUG: depends on process
|           0x00400af2      4885c0         test rax, rax
|       ,=< 0x00400af5      7438           je 0x400b2f
|       |   0x00400af7      bfb40f4000     mov edi, str._home_warmup_flag ; "/home/warmup/flag" @ 0x400fb4
|       |   0x00400afc      b912000000     mov ecx, 0x12
|       |   0x00400b01      4889c6         mov rsi, rax
|       |   0x00400b04      f3a6           repe cmpsb byte [rsi], byte ptr [rdi]
|      ,==< 0x00400b06      741f           je 0x400b27
|      ||   0x00400b08      488d742410     lea rsi, [rsp + 0x10]
|      ||   0x00400b0d      89df           mov edi, ebx
|      ||   0x00400b0f      4889442408     mov qword [rsp + 8], rax
|      ||   0x00400b14      48c744243800.  mov qword [rsp + 0x38], 0   ; block pathname access
|      ||   0x00400b1d      e8ce020000     call fcn.ptrace_setregs
|      ||   0x00400b22      488b442408     mov rax, qword [rsp + 8]
|      `--> 0x00400b27      4889c7         mov rdi, rax
|       |   0x00400b2a      e8c1fbffff     call sym.imp.free
|       `-> 0x00400b2f      488b8424f810.  mov rax, qword [rsp + 0x10f8]
|           0x00400b37      644833042528.  xor rax, qword fs:[0x28]
|       ,=< 0x00400b40      7509           jne 0x400b4b
|       |   0x00400b42      4881c4001100.  add rsp, 0x1100
|       |   0x00400b49      5b             pop rbx
|       |   0x00400b4a      c3             ret
\       `-> 0x00400b4b      e8c0fbffff     call sym.imp.__stack_chk_fail ;[9]
```

We discovered potential issue with the above, where results of *realpath* subroutine may change depending on process.
Typical example is accessing **/proc/self** that links to different location depending on PID of calling process.

We didn't find any other issues in provided binary.

### Bypass Approach

We spent some time experimenting with different pathnames that may be interpreted differently for different processes.
Finally we decided to use following pathname:
```
/proc/self/task/[MONITORED_PROCESS_PID]/root
```

The above pathname:

* points to root directory when referred by monitored process and
* does not exists when referred by sandbox process, allowing for syscall to continue without modification.

As we don't know PID of monitored process, we will attempt to bruteforce this PID from within our exploit.

### Exploit Implementation

Out exploit is based on code from Warmup flag, were we modified ROP chain and added new stage.

The ROP chain has the following steps:

1. read next stage into data area of exploited binary
2. write *SYS_mprotect* bytes using 0x08048135 to set eax register
3. execute 0x08048122 that performs syscall using pre-set eax, this will modify permission of data area to READ+WRITE+EXECUTE
4. jump to next stage

The next stage has the following steps:

1. bruteforces MONITORED_PROCESS_PID to open */proc/self/task/[MONITORED_PROCESS_PID]/root/home/sandbox/flag*
2. read the flag into memory
3. write content of buffer to standard output

Attached [exploit.py](exploit.py) was used to retrieve flag during CTF.
