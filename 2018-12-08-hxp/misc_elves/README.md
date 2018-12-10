# Tiny elves (misc, 50+2p, 59 solved)

In the challenge we get a [source code](tiny_elves_fake.py) running on the server.
The code is quite simple:

```python
#!/usr/bin/python3
import os, tempfile, subprocess

try:
    data = input(">").strip()
    if len(data) > 12: raise Exception("too large")

    with tempfile.TemporaryDirectory() as dirname:
        name = os.path.join(dirname, "user")
        with open(name, "w") as f: f.write(data)
        os.chmod(name, 0o500)
        print(subprocess.check_output(name))

except Exception as e:
    print("FAIL:", e)
    exit(1)
```

The application reads up to 12 bytes from us, then saves them to a file and executes this file.
Obviously we can't make a real ELF file in 12 bytes, but there is another "type" of files that linux can execute, and there is no actual check if we provided ELF file.

The obvious idea is to use shebang to run some commands. 
For example we can send `#!/bin/ls .` and this would list files in CWD for us.
There are two issues here:

- The flag file is `flag.txt` which is 8 bytes long name, so we definitely can't directly use this name in the command.
- No shell expansion tricks will work, so no wildcards like `*` or `?` will help us.

This leads us to the conclusion that we need to run a command which can take additional input from stdin.

Obvious candidates would be `vi`, `ed` or `ex` but the paths are too long.
Finally we found in the manual that `sh` has parmeter `-s` which does exactly what we need - reads input from stdin.

So we can send `#!/bin/sh -s` and then proceed with `cat flag`.

One last trick was that there was no echo until we close the subshell.
The flag was: `hxp{#!_FTW__0k,_tH4t's_tO0_3aZy_4U!}`
