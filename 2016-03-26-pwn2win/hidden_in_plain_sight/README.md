## Hidden in Plain Sight (Forensics)
	tl;dr read the file before it's been decrypted

In this task, we're only given a mega download link.(https://mega.nz/#!6N0gmRLK!VsN9gLdiYbxMVTA-AdsRjsvezMpdEqiR9ngwrS6gR7k)

The hint is: `you need to know the basic principle behind how MEGA works in order to solve this challenge. Flag.txt is the flag, but it is hidden... in plain sight ;)`

Mega doesn't store keys to decrypt your data, you are given them with the url, in our case it's `AdsRjsvezMpdEqiR9ngwrS6gR7k`. The files are download to a sandbox using *FileSystem API*.

After the download is complete, the file is then decrypted using aes and passed to the normal download folder.

The downloaded flag loogs like gibberish: `}Żv#ĘÖ›{QřČxJZzŃ\M÷2Ž¸IĆ&N˛<­z´ŕ´„ĽĹ*‹—ýk/ĂĂµ`

Let's then try viewing the flag before it's been decrypted by using Chrome developer tools.

![img1](screen1)

Bingo!