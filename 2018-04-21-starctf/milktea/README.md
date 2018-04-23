# milktea, re

In this task we got quite obfuscated, though small, binary. It asked for a password and checked whether it
is correct. As an easy to overlook obfuscation, it patched its GOT `memcmp` entry to point to a custom function,
which actually checks whether `arg1 == arg2 ^ const_buf`. Other than that, the reverse engineering boiled down to
simplifying as many expressions from the executed statements as possible. In the end, most of them turned out
to be xors with constants, which eventually cancelled out to zero. The final encryption code was quite simple
and fit in a few lines of C code. All operations were invertible, so we wrote the decryption function, which
yielded the flag. The whole solution code is available in `doit.cpp`.
