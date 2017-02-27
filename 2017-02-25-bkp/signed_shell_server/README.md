# Signed shell server (pwn, 200)

> I'll only execute shell commands that are authenticated with my hmac-sha1 key.
> I'll sign a few benign commands for you, but after that, you're on your own!

As described in the task description, we were given a binary that would execute anything we
give it, but only if authenticated with HMAC. We were given `ls` and a few other commands - nothing useful though.

The two global variables of particular interest were `char buff[256]` and immediately following `bool md5_vs_sha1`.
The latter one was set based on `argc` - on server it was set to 1, which meant md5 was used as HMAC hash.
The `buff` array was the place to which our input was sent to.

It turns out we could overwrite the `md5_vs_sha1` flag with a zero by sending exactly 256 bytes of data, as the server,
trying to be helpful, null-terminates the buffer: `buff[chars_read]=0;`. So, we were able to use sha1 now.

The second bug was in the `execute` function too. The stack layout was generally: 
`char hash_buff[20]; void (*denied)(); void (*granted)();`. For some reason - I couldn't find a reasonable explanation - 
if the hash used was sha1, the hash was saved one byte later, i.e. at `hash_buff+1`. Since sha1 length is 20 bytes, that
means we should be able to overwrite the `denied` function pointer's lowest byte (it was then called when HMAC was incorrect).
By sending random data, we had about 1/256 chance of that byte becoming the same as `granted` function's, thus executing 
our command. So, we simply generated `cat flag` with a lot of random spaces and tabs to the rights, hoping it gives
correct result. Eventually, it did.
