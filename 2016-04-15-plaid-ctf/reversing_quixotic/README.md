## quite quixotic quest (Reversing, 300 points, 40 solves)

	Well yes, it certainly is quite quixotic. (Yes, the flag format is PCTF{} )

In this task, we had a modified `curl` binary. We were able to notice the main difference
with the original binary even without binary diffing - it was enough to run `qqq --help`
to notice the unusual option - `--pctfkey KEY`. Trying to run it with dummy key gives us
`wrong` message, so we tried to check in debugger how the key is checked.

We quickly noticed the following piece of code is executed if we give that argument:
```
0x08052aac mov dword [esp], str.Validating_key..._n
0x08052ab3 call sym.curl_mprintf
0x08052ab8 mov edx, dword [ebx + 0x128]
0x08052abe mov eax, obj.magic_buf ; obj.magic_buf
0x08052ac3 mov esp, eax
0x08052ac5 mov eax, edx
0x08052ac7 ret
```
After the `ret` instruction, we end up in two assembly instruction piece of code:
```
0x080ad0df mov esi, edx
0x080ad0e1 ret
```
Returning again, we are again in some short routine. It looks very similar to a ROP chain.
In fact, we can see some returns into the middle of `strlen` function with our
key as input, indicating we are on good track.

Looking up the `magic_buff` symbol, we notice it has about a quarter of megabyte in size,
which is a fair amount of code to step through. I wrote a script (`getrop.py`), which 
runs `gdb` to disassembly several instructions after each ROP address and save it in
`ropchain` file. Unfortunately, it ended up being some 7MB of text, so we needed to
filter it somehow.

Running debugger and looking at generated ropchain at the same time, I was able to
notice many repetitions, looking almost like unrolled loops, so I just editted the file
writing number of repetitions and the basic block. There were also many skipped instructions,
both by `pop` instructions, which skipped the next instruction, and by some `ret imm16`
instructions, which skipped a large amount of bytes at once.

In the end, the commented disassembly (`adnotations_ropchain` file) had only about 1000
lines, which was much more manageable. Still, I rewrote it to an even more readable
form - pseudo-disassembly in `disasm_written`. 

The basic thing the code did, was:
- checking if key length equals 0x35
- summing ASCII values of all the letters
- calculating MD5 of that sum xored with some constants
- checking whether that MD5's first dword equals some constant
- xoring our input with that MD5 as key
- comparing our xored input with some constants

From this point on, it was pretty simple. I modified `getrop.py` to also print those constants
and save them in `values`.
We can brute force the sum of characters and their MD5 - it turns out only one combination
returns correct first dword of MD5.
Final password is obtained through xoring that MD5 with extracted values.
```
$ python brute_md5.py 
10620
13567 c0050bdd747721646f14ff008c6978b9
And the flag is...
PCTF{just_a_l1ttle_thing_1_l1ke_t0_call_ropfuscation}w!d
```
