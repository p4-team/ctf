# Better ZIP, crypto, 231p

> The legacy ZIP crypto is long broken, so we've fixed it

In this task we got Python implementation of ZIP compressor, which used custom cryptography. We don't know the 
password they used, so we cannot decompress it, but we can see the file list - `flag.png`.

The cryptography was quite simple. There were 8 Linear Feedback Shift Registers, initialized basing on
the password. They were only 20 bit in length, so we could brute force it, if we had enough plaintext known.
Luckily, PNG has a few predictable places at the beginning and the end. Unfortunately, the first 20 bits,
which are mostly constant headers, we know already from the ZIP file structure, so they are useless.

The bits we used as known, were:
- 20 and 21, set to 0000, top two bytes of image height
- 24, set to 08, bit depth
- 25, set to 02, color type (RGB)
- 26, set to 00, compression
- 27, set to 00, filter type
- 28, set to 00, interlacing
- 33, set to 00, high byte of next chunk's length
- and final 12 bytes, which is the whole IEND chunk

This was 20 bits in total, which allowed us to write `parse.py` and narrow down the LFSR parameter
possibilities to just a couple each - or a couple hundred combinations in total. We brute forced them
all - `final.py` - and if it produced a valid PNG, we were done.
