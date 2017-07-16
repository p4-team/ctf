# Decrypt the undecryptable (reverse, ppc, 724p)

> Oh noes! It looks like we've lost decryption keys to our super-secret archive that contains all the blackmail material we've accumulated over the years!
> Luckly, the encryption system was built with the government money by the lowest bidder, so maybe it contains some flaws.

> decrypt_the_undecryptable.tar

In this task we were given a randomish BMP picture and a binary for en-/de-crypting.

I didn't even really look at the binary - one quick glance at the image was enough to see distinct repetition patterns.
This very likely meant it was encrypted using some block cipher in ECB mode or, alternatively, xored using short repeating
key. I quickly found an offset containing the repeating part, produced a quick and dirty Python script to xor
the whole image with that 128-byte long block and save the result. The final image was not perfect, but good enough to be
able to read the message.
