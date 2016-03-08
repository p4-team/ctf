## Jit in my pants (reversing, 3 points, 38 solves)
	Because reversing an obfuscated jit'ed virtual machine for 3 points is fun! 

In this task we got an ELF binary. Looking at it's disassembly was really hard - lots
of obfuscated code was put there - I thought that for 3 points we were supposed to use
something easier. 

Tracing the binary, we notice a lot of `gettimeofday` calls. This was a function checking
current time - something which should not be present in legitimate key checking code.
I created a simple replacement function (`tofd.c`), which I then LD_PRELOAD'ed to achieve
deterministic execution.

In my solution, I used instruction counting to get the flag. The idea is, that the code
checks flag characters one by one, exitting early if a character is wrong. We can exploit
this - when we supply a good prefix of the flag, the binary will execute slightly longer 
than with a wrong one. Using `doit.py` and Intel's pin, we brute forced the solution
one char at a time in around an hour (this could take shorter time, but I wanted to stay
on the safer side and used `string.printable` as the character set).
