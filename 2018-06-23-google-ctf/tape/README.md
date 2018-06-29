# Tape, misc, 355p

> We've found this priceless, old magnetic tape in our archives. We dumped the contents, but the data is corrupted and we can't read it. We only have this old tape reader tool, but source code was lost long ago. The program has only 944 bytes, so reversing it should be trivial, right?

We got a FLAGZ.DAT file and a remarkably small ARM executable. Reversing it, we found it reads the file in
88 byte chunks, first 80 of which is xor of two plaintext lines, and the final 8 is CRC64 value of plaintext line.
It would be enough to decrypt the file, but unfortunately the binary says there are CRC errors - and indeed,
some characters get misprinted.

Initially, there was only usually a single wrong character per line, which was easy to brute force (`solx.cpp`). Further lines
had two or three, which with some charset narrowing and occasional manual help (it was English text, after all), was
managable.

The final line however, was not really bruteforceable at all:
```
: You probably just want the flag.  So here it is: CTF{dZXi----------PIUTYMI}. :
```
Dashes mark unknown bytes. We know the CRC64 of the text though, so we downloaded the `crchack` tool,
brute forced two characters of the flag, and asked `crchack` to find the remaining eight. If everything
is printable - that's the answer. See `script.py` for implementation.
