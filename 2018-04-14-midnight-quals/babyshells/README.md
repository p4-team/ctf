# Babyshells - Pwn (50 + 0)p, 65 solves

> If you hold a babyshell close to your ear, you can hear a stack getting smashed

In this task we were given three binaries and three corresponding `host:port` pairs to pwn. These binaries
were in x86, ARM and MIPS architectures respectively, but they all were very simple. They had no NX, and 
jumped right into our supplied buffer. Googling "$ARCH + shellcode" and sending the result was enough to solve
the challenge.
