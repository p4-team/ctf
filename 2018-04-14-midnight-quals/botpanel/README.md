# Botpanel - Pwn (300 + 0), 17 solves

> These cyber criminals are selling shells like hot cakes off thier new site. Pwn their botpanel for us so we can stop them

In this task we were given a binary and `host:port` where it is running. Connecting there we get a banner
and password prompt. After analyzing the binary, we notice that there is a format string bug - typing `%s` would 
either crash or print garbage.

It turns out the expected password is stored in a local variable, so we could use `%7$s` to get the correct password echoed:

```
		Panel password: %7$s
		Incorrect! 4 attempts left
		Your attempt was: >@!ADMIN!@<
```
Logging in, we get a simple menu, but anything we try is restricted due to running in "trial mode". Analyzing the binary, it
seems the boolean holding the current mode is initialized in the login function - since there's the format bug, we could
overwrite it using `%6$n`.

After doing this, we get "registered mode" menu. It allows to send invites to arbitrary host:port - which spawn a new
thread which connects back to specified IP. The invited menu in turn allows to send feedback. The feedback option
first asks for length, then the feedback string. It is immediately suspicious, but there are checks for the length
being in reasonable size, so no obvious buffer overflow is there. However, the read buffer length is a global variable,
meaning we can send normal length in one connection, get it to pass the checks, then send large length in second connection,
and finally send large buffer in the first one. This allows us to overflow the buffer, overwriting the return address and
allowing the ROP.

There were a couple of other roadblocks still. First of all, there was a stack cookie. Thankfully, on Linux the stack
cookie is constant for the whole process duration, so we were able to leak it during the login phase at the start,
using `%15$x`. Second problem was that the ASLR was turned on, so we had to find the address the binary was loaded at.
We did it in the same way, via leaking return address during login procedure: `%19$x`.

The binary was rather small, so there was not enough gadgets to easily make a reliable exploit - our solution
increments (bytewise) `puts` function GOT entry so that it points to `system`. Because it is bytewise incrementation,
the possible carry is ignored, so the result may be wrong. Still, the exploit works about half the time.
The whole code is available in `doit.py`.
