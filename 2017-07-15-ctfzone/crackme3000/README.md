# Crackme3000 (reverse, 724p)

> Our opponents have set up a private email server to store their correspondence.
> We need to gain access to it. Could you break their advanced authentication protocols?

> crackme3000

In this task we were given a single MIPS binary. It wasn't too big, but reversing it was still painful. Architecture
is not widely supported by RE tools, but task creators were actively trying to mislead us. For example,
the congratulations text was printed in two cases: either the input string was equal to some hardcoded
string formatted like a flag (which BTW was not the flag), or when a series of checks were fulfilled.

The binary used RC4 cipher as a part of password checking. Finding the key was tricky though - it turned out
to be the string `error: _ptr is not null` - yeah, seriously! I initially skipped that part of binary,
thinking it's just random compiler error checking subroutine. Nice idea for delaying the reversing.

The binary then tried to open some file, but didn't seem to do anything with it. Then it decrypted some data using
RC4 and xored it with `xor_key` buffer. The problem is, that buffer was set only if the operation of opening that file
did not succeed. The `xor_key` was then set to the result of `strerror` function call - as I guessed, 
Linux-like `No such file or directory` error message. Combining all this together, we wrote a quick script to get the flag.

This was a really cleverly annoying task. What a weird combination.
