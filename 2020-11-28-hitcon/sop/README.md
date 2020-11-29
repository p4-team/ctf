# SOP, reverse, 305p

> Let me introduce a brand new concept - Syscall Oriented Programming!

This was a fun challenge. The binary was very simple. It implemented a small VM with 16 registers (last of which was program counter),
for which each operation was a syscall. The opcode structure was: 8 bits of syscall number, then up to 6 syscall arguments, which
could be constants, VM registers or VM register addresses.

We quickly wrote a bytecode disassembler in Python and found there were just a handful of syscalls used. Many of them didn't really make
sense (getppid?) and `strace`ing showed they resulted in SIGSYS for some reason.

It turned out the binary set up a mmapped region in which it wrote a tiny shellcode - SIGSYS handler (set up using sigaction syscall).
It also set up a seccomp filter. Reversing it (using kernel jit dump) showed it dispatches syscalls into yet another VM level -
so for example, `getgid` was actually `AND`. This allowed to bootstrap a reasonable run environment. We updated our disassembler
to show these higher-level opcodes and found out the program implemented a variant of XTEA cipher. The key was constant,
and the ciphertext embedded, so we could simply write the decryption code and get the flag.
