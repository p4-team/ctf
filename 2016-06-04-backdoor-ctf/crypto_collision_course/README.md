# Collision course

In this task, we were given a hasher binary (`foobar`) and a file, for which we had to find
a collision (`collider`), that is a file, which passed as input to `foobar` gives the same hash.
There could be many solutions, but only one of them makes sense (is an English text).

Analyzing the assembly, we can rewrite the binary into the following pseudocode:

```
def hash(block):
	block^=A
	ROR(block, 7)
	block+=B
	ROL(block, 7)
	block*=C
	return block

state=0
for 4-byte block in input:
	h=hash(block)
	state^=h
	ROR(state, 7)
	print state
```

Since state is printed out after every iteration, we know every state. Let's denote them as
s0, s1 and so on, where s0=0 (initial state).
```
s(i+1)=ROR( s(i)^hash(block), 7 )
ROL( s(i+1), 7 )=s(i)^hash(block)
hash(block) = s(i) ^ ROL( s(i+1), 7 )
```
So, since we know all s(i), we easily calculate all hashes of 4-byte blocks. Since 4 bytes are
in the brute-force range (and the search space could be significantly lowered by considering
only printable characters), we implemented the hash in `main.cpp` and brute-forced all fitting
input blocks. Output was not unique, but it was easy to choose the correct answer from the few
possibilities.
