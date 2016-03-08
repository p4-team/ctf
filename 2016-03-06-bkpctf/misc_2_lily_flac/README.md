## lily.flac (misc, 2 points, 28 solves)
	more than just a few bleebs ;)

In this task we were given a FLAC file containg a, somewhat weird, music. Looking at it
in Audacity, we noticed that there is a very different spectrum in the beginning and end of
the file - so there was probably some data hidden. We converted the file to wav, since it's 
easier to work with uncompressed data.

Looking at the first couple of hundred of bytes, we notice there are a lot of 0x80 and 0x7f
bytes. In 8-bit wav, they mean a very quiet sound, but since we suspected the file to contain
hidden binary data, we thought they would mean 0x00 and 0xFF bytes, respectively - as though 
they got xored with 0x80 (in the hindsight, it seems to be just the fact that wav files contain
*signed* data, which shifts all the values by aforementioned 0x80).

Xoring the wav with 0x80, we found that the first bytes of sound data are now: 
`\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00` - an ELF! We stripped wav header from the file and
ran the ELF, which in turn gave us the flag.
