# Secret server (Crypto, 221p)

```
AES is unbreakable. Right?

nc 52.193.157.19 9999
```

In the task we get the [sever sources](secretserver.py) to work with.
It's rather short and pretty simple to understand.

1. The application asks us to solve a simple PoW
2. Application sends to us AES-CBC encrypted message `Welcome!!` with appropriate padding.
3. Application reads commands from us, decrypts them and if the command is correct it gets executed and we get back encrypted results.

Worth noting: 

1. IV is appended as the first block of the ciphertext!
2. The commands are first stripped and then only startswith is checked, so it doesn't matter if we have some more characters as long as prefix fits.
3. `unpad` does not check the padding at all, it just cut designated number of bytes, can be multiple whole blocks.

The fact that we can control the IV is very useful because it means we can modify the IV by XOR to enforce any decryption of the first block.
This is due to the way CBC mode it works -> after decrypting i-th block, the block is XORed with ciphertext of block i-1 (or with IV if it's the first block).
If we know what was the previous plaintext we can simply XOR k-th byte of IV with k-th byte of previous plaintext to "zero" the resulting byte, and XOR one more time with expected value to make AES-CBC get this expected byte at k-th position after decrypting.

We can easily use this feature to "change" the `Welcome!!` message into one of the available commands, in our case into `get-flag`, since we know the whole plaintext.
This gives us the ciphertext with flag from the server.

Next step is noticing that the flag prefix is `hitcon{` which means we know part of the plaintext for first block!
In fact we know enough of the plaintext to turn this block into a command again!
The easiest one to use was again `get-flag`.
Notice that we are one character short here, we can easily turn `hitcon{` into `get-fla` but we don't know what XOR we need to get the next character to become `g` since we don't know the first character of the plaintext flag.
But we can simply brute-force it, it's only 255 possibilities and only one of the will actually work and server will return the encrypted flag (and we already have this ciphertext so we can compare the output with it).

So we do something like:

```python
for i in range(255):
	iv[7] = ord(iv[7]) ^ ord('g') ^ i
	if command_ok(iv):
		print(chr(i))
		break
```

And we manage to recover the first byte of the flag -> `P`
Since the server does `.strip()` on our commands we can use the same technique now to get second byte of the flag, by preparing a new command with a space at the beginning.
So we change `hitcon{P` into ` get-fla` and again perform the same brute-force to get another character.

This approach works until we hit the end of the first block.
We can't push it any further because the second block is XORed with ciphertext of the first block, and we can't modify it without causing this block to decrypt badly.

But we figured that there is still the `unpad` issue here.
If we could force the last byte of the payload we send to be some arbitrary large value, it would cut the plaintext up to a character we want.
This would be very useful since we can use command like `get-md5` to calculate md5 of the rest of the plaintext.

If we could:

1. Change first block to a bunch of spaces and `get-md5` at the end of the block, with one character available at the end of the block. Force the padding to cut all other plaintext blocks. Then get all possible encrypted md5 sums for every possible value of this single character.
2. Change first block to a bunch of spaces and `get-md5` at the very end of the block, and force the paddin to cut all of the plaintext from other blocks leaving only a single character in the second block.

What happens we basically get: `get-md5X` where `X` is the first byte of the flag second block, and `get-md51`, `get-md52`, `get-md53`...

And we can simply compare the results to find the real value for `X`.
We can then cut one of the spaces in from of `get-md5` and extract another byte the same way.
It works until we run out of spaces to cut, but it's already enough to extract prefix of the next block plaintext, which basically gets us to the same point as we were at the very beginning with `hitcon{` prefix, so we can shift blocks to the left (first block of flag becomes IV) and perform the whole thing again!

The last problem is how can we force the `unpad` to cut as many characters from plaintext as we want.
The trick here is to notice that we can simply append blocks at the end!
Specifically we can append our good old `Welcome!!` message with the IV (so 2 blocks).
We know that this message has a standard padding applied, so we know the last byte of plaintext.
We can easily XOR last byte of the IV we're attaching at the end, to force the very last of the whole plaintext to be anything we want.
Of course this IV block we just glued will decrypt into some random bytes, but we don't care since we will cut it anyway.

This means we can cut the plaintext now at any position we want, and it's enough to run the attack described above.

It takes a while since we need to test any potential printable character for every byte in the flag but in the end we get:

`hitcon{Paddin9_15_ve3y_h4rd__!!}`

The whole attack code is [here](attack.py)
