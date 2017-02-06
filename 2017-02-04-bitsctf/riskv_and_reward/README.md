# Riskv and Reward (reversing, 80p)

> open-source all the things!!!

We solved this task in a fun way. Running `file` command on the supplied binary informed us that it's an ELF for
RISC-V architecture. We couldn't run it directly on our computer and installing an emulator was annoying (it didn't work
for some reason). So, we solved it in a blackbox way!

Running `strings -n 20 riskv_and_reward` gave us only one string: 
```
tjb3csFt0rrutrh_wiv5__fi}k_1ih`{xIcrhsoyBmyw1CyT3rvxStT_jq40_zrq(
```

Although it seems quite messed up, we quickly noticed it has some resemblance to the flag format: it has two curly braces,
and all the capital letters from `BITSCTF`. It seems it was permutated in some way. So, the only thing left to do was 
reversing the permutation. Running `hexdump` on the binary, we found an interesting part right after the aforementioned
string:
```
00001080  28 00 00 00 21 00 00 00  2f 00 00 00 34 00 00 00  |(...!.../...4...|
00001090  2d 00 00 00 36 00 00 00  06 00 00 00 1f 00 00 00  |-...6...........|
000010a0  25 00 00 00 3b 00 00 00  29 00 00 00 03 00 00 00  |%...;...).......|
000010b0  37 00 00 00 3e 00 00 00  1b 00 00 00 05 00 00 00  |7...>...........|
000010c0  22 00 00 00 13 00 00 00  14 00 00 00 3a 00 00 00  |"...........:...|
000010d0  31 00 00 00 30 00 00 00  1a 00 00 00 10 00 00 00  |1...0...........|
000010e0  08 00 00 00 23 00 00 00  07 00 00 00 24 00 00 00  |....#.......$...|
000010f0  3c 00 00 00 2c 00 00 00  00 00 00 00 18 00 00 00  |<...,...........|
00001100  43 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |C...............|
```
We noticed every number appears just once, so this was probably a transposition table. From now on, we had to just write a 
simple script to apply the permutation to get the flag.
