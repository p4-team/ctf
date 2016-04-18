# morset (Misc, 50pts, 86 solves)
	A mysterious signal… can you decode it? 
	Running at morset.pwning.xxx:11821

In this task we were told to conenct to certain server. The server sent us some
dots and dashes, so we immediately thought it could be Morse code. Decoding it, though,
gave us some gibberish alfanumeric string. They were generally very different, but
sometimes they were pretty similar. For example:
```
AIDQJB34I3OA5B0BVLPE3OGV6XX23TTIGE6I451CC6V0VPWVWWGL1123EL2K56OS6R3W123WF2B0P90XH6N
AIDQJB34I3OA5B0BVLPE3OGV6XX23TTIGE6I451CC6V0VPWVWWGL1123EL2K56OS6R41GDX88YQMO172Z3Z
```
We thought it could be some constant start of the message followed by some challenge.

Finally, we came up with an idea how to decode this text - since this was neither base64
nor base32, it could be base36! Used alphabet was `0-9A-Z`.
Final decoding and encoding code is in `doit.py` - it turns out
server was sending us questions such as "What is SHA256(grapefruit1234)?". After sending
answer in the same format, we got the flag.
