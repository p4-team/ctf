# zip (300, coding)

> We found a strange zip file. Sadly the content is encrypted. As only criminals encrypt their stuff we need to decrypt this urgently.
> Flag format is FLAGB**************S.

In this task we got a zip file containing a couple of other small zip files. All of them were encrypted, but their size
was only up to 5 bytes - just like in recent 
[Backdoor CTF task](https://github.com/p4-team/ctf/tree/master/2016-06-04-backdoor-ctf/crypto_crc). See that writeup for
details.

After decrypting, this is what we got:

```
1 main(
2 ){int
3 n=24
4 ;whil
5 e(n--
6 ){put
7 char(
8 
9 
10 ]^n);
11 }}
```
Files 8 and 9 were missing. However, basing on flag format from task description, we could guess what should go in these
empty places:
```
In [1]: s="FLAGB"

In [2]: for i, c in zip(range(23,0,-1), s):
   ...:     print chr(ord(c)^i)
   ...:     
Q
Z
T
S
Q
```
It might be a bit of guess, but we see that the last letter is the same as the first one, indicating period equal to 4.
If we put `"STZQ` in file 8, and `"[n%4` in file 9, then both files have size equal to 5, just like the others, and
the output of compiled program matches flag format.
```
main(){int n=24;while(n--){putchar("STZQ"[n%4]^n);}}
// Prints FLAGBHEC^TY_ZP][V\QWRXUS
```
