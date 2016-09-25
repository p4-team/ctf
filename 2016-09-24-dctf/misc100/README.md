#  The nospecial virus (Misc 100)

> I have been infected with a virus like CryptoLocker and now they ask for money to give me the password to this archive so I can get the password required to decrypt all my files. Please help! 

> Format Response: DCTF{md5(solution)} 

> https://dctf.def.camp/quals-2016/decrypt_files.rar

This task had an encrypted RAR archive with a single 7-byte file stored in it. Similar tasks happened in the past, for
instance: [here](https://github.com/p4-team/ctf/tree/master/2016-06-04-backdoor-ctf/crypto_crc) or
[there](https://github.com/p4-team/ctf/blob/820f3215e3c45f18e3073d55c7c3e745d37fb878/2016-08-21-bioterra-ctf/zip/README.md).
We simply modified code used in these tasks, and it turned out one of the contents found using `a-z0-9` alphabet was
the correct one.
