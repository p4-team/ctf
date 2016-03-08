## ltseorg (crypto, 4 points, 93 solves)
	make some (charlie)hash collisions!

In this task we were given a code with function hashing strings and were asked to create
a hash collision. After reading the 
algorithm, we quickly noticed that the padding function was non-standard and flawed:
```
def pad_msg(msg):
	while not (len(msg) % 16 == 0): msg+="\x00"
	return msg
```
This simply added `\x00` bytes until message length is divisible by 16. That means that
two messages: "a" and "a\x00", although being different, create same hashes. After sending
them to the server, we receive the flag.
