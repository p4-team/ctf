# Rescue Shell, 100p, exploit

In this task we were given a binary showing a password prompt. There was a 
simple buffer overflow, allowing us to ROP and first dump GOT `fread` address, then
overwrite it with libc single gadget offset.
