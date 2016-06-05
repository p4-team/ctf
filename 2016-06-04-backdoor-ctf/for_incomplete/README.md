# Incomplete

In this task, we were given a pcap file containing a couple of HTTP requests. They mostly got 
"Partial Content" response, but asked for the same file. That meant we could extract the requested
file, but with some small holes.

We have manually extracted the parts of files from the pcap into `24`, `38` and so on. Then,
we wrote a Python script (`join.py`) 
joining them together, filling the empty places with 0xcc bytes (and
also printing their offsets, to avoid false positives). Quick inspection of the hexdump showed
it was probably a PNG file - it contained IDAT and IEND strings, for example. We were unable
to open it though, because it lacked header and was not even recognized as a valid PNG.

After adding the constant header in hexeditor, we still had problems with opening it - there
were complaints about invalid CRC in IDAT chunk. Well, we calculated it as well 
(using `pngcheck` utility) and fixed
it (it was in position, where 4 bytes were missing). Later, we had to fix chunk names (easy,
since all of them were IDAT, so no guessing here), and their lengths (also simple, because
in this PNG they all were the same size - 16000 bytes). The final missing byte was not
a metadata though, but one of the data bytes. Since PNG chunks contain checksum, we could
just brute force the missing byte and see if it gives us the correct checksum.

Fixing the image just in hexeditor would take us some time, so we wrote a simple script
`fix.py`. It did nothing more than I described here, but semi-automatically, so that I can work
on clean PNG every time.

The final result is `png3`. Note that it is too tall, because we had to guess the size - it was
erased. The image is clearly visible though, so we submitted flag with no problems.
