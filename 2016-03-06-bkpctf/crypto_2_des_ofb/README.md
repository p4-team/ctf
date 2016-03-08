## des ofb (crypto, 2 points, 189 solves)
	Decrypt the message, find the flag, and then marvel at how broken everything is. 

We were given encryption code and a ciphertext. It used DES cipher in OFB mode. OFB means
that IV was encrypted using key, its result then encrypted using the key again, then again
and so on. Ciphertext is obtained through xoring those encrypted blocks with plaintext.
Longer description is available on [Wikipedia](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Output_Feedback_.28OFB.29).

Code was very simple and DES cipher is not easily breakable, so we looked into hex dump of
ciphertext:
```
00000000  70 2b 7b ef 93 27 53 d3  43 13 5c 5b 41 16 43 57  |p+{..'S.C.\[A.CW|
00000010  04 26 3e a1 d6 7f 1b dd  45 13 5b 47 15 42 5f 5d  |.&>.....E.[G.B_]|
00000020  04 35 2e e8 85 7f 1a d3  5f 09 38 63 5d 53 43 50  |.5......_.8c]SCP|
00000030  41 36 7b aa 82 62 00 9c  7f 5c 50 58 50 44 17 51  |A6{..b...\PXPD.Q|
00000040  4a 64 2f e5 93 2b 1e d5  5f 57 12 40 5a 16 44 4d  |Jd/..+.._W.@Z.DM|
00000050  42 22 3e ff fc 5f 1b d9  11 60 5e 5d 5b 51 44 18  |B">.._...`^][QD.|
00000060  45 2a 3f ad b7 79 01 d3  46 40 12 5b 53 16 58 4d  |E*?..y..F@.[S.XM|
00000070  50 36 3a ea 93 64 06 cf  11 75 5d 46 41 43 59 5d  |P6:..d...u]FACY]|
00000080  08 4e 14 ff d6 7f 1c 9c  45 52 59 51 15 77 45 55  |.N......ERYQ.wEU|
00000090  57 64 3a ea 97 62 1d cf  45 13 53 14 66 53 56 18  |Wd:..b..E.S.fSV.|
000000a0  4b 22 7b f9 84 64 06 de  5d 56 41 18 3f 77 59 5c  |K"{..d..]VA.?wY\|
000000b0  04 26 22 ad 99 7b 03 d3  42 5a 5c 53 15 53 59 5c  |.&"..{..BZ\S.SY\|
```
This is just the beginning, but there are obvious patterns - for example every character
in 4th and 5th columns were unprintable. This should not happen if we used secure cipher,
so there must have been some problem. As DES used 8-byte blocks and ciphertext had
pattern with period of 16, that means DES used a particularly bad key, which made the keystream
periodic with period of 2, i.e. `DES(DES(IV, key), key)==IV`. 

What that means, is that we can treat the ciphertext as xored with 16-byte key. Using simple
heuristic (most frequent character in each column was likely space), we managed to decrypt
most of the plaintext. We then fixed the rest of the key manually - full code available in
`decrypt.py`. The plaintext was Hamlet's beginning, with flag appended.
