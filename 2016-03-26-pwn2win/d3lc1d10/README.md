------------------------
[Steganography] d3lc1d10 - 25 points
------------------------

> We found an abandoned file on an old Club’s server. Our informant said it was possible to extract a phone ( XXXX XXXX ) number from it. Get the number and find out the address that he belongs.

> Note: The flag is in this format: CTF-BR{address with space and comma}

In this task we were given a small file. Hexdump on it was not very useful, but `cat`ting it showed some emoji.
Admins gave hint on IRC: "esolang", so we searched for esoteric languages using emoji as code. Not much time later,
we found `emojicode`. Downloading compiler and running the code, we got 8 digits as the output. Since task's description
asaked for address, we Googled those 8 digits and found out it was phone number of some Brazil place. We searched their
website and found their location. Pasting the address as a flag we got another 25 points.
