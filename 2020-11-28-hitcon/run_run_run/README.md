# Run Run Run!, reverse, 315p

> just run it and get the flag

We get a .prg file. It's not immediately obvious what kind of file it is (`file` and `binwalk` find no magic), but searching for some strings
from the binary we find out it's a Connect IQ program file for smart watches and similar devices. As it turns out, the file contains no
executable native code, no source and no well-known bytecode like Java's. Instead, it uses a custom VM (kind of similar to Java's). 
[CIQDB](https://github.com/pzl/ciqdb) parsed the file, from which I used the symbols, which was useful for reversing. I also
decompiled CIQ SDK official .jars to find bits of information about VM opcodes. Eventually, this allowed me to write a disassembler in Python
and reverse engineer the code.

The program was decrypting the flag, using increasing amounts of iterations for each flag character, making the delay too long after a few characters.
The decryption used a keystream made of insecure random number generator, which was simple to fast forward using fast matrix exponentiation.
