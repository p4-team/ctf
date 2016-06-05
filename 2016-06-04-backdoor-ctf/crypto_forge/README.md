# Forge

In this task we were asked to create CRC collisions. We had file `mandog.png` and had to create a
valid PNG, whose crc32 was the same.

CRC32 is designed to be easily updatable - the crc32 function doesn't have to recalculate the whole
checksum when new data arrives. It is important in this case, because it means we can just 
append some trash data after the IEND PNG chunk (which png parsers ignore), and calculation
of the new CRC is very quick, since the loop will have to go over just the new bytes.

We wrote a simple brute force (`check.cpp`), which in a few minutes created valid 10-byte strings,
which appended to the original image did not check its CRC. Result:
```
[adam@adam-Y510P ~/CTF/backdoor/forge]λ crc32 mandog*
a8eaac0a	mandog_izzhqyprfw.png
a8eaac0a	mandog.png
a8eaac0a	mandog_szscanpdgm.png
a8eaac0a	mandog_wispqhyawl.png
a8eaac0a	mandog_wyeucyrljm.png
a8eaac0a	mandog_xqtawyeyhq.png
[adam@adam-Y510P ~/CTF/backdoor/forge]λ sha1sum mandog*
5fc968ee9f33628f374f97b9c78c6f7a9930e869  mandog_izzhqyprfw.png
0c2308197b15718953dd77d48269b37a92db8fda  mandog.png
174141fc4c5757b68dfffbf1204ed0640536d17d  mandog_szscanpdgm.png
c91f67636a816f5aab1041723f5efb8fbd697b25  mandog_wispqhyawl.png
da06f9a68ce394f12949b130fd94f306bc27bfc2  mandog_wyeucyrljm.png
f28ca952eec0d19d5b265bf936da40cd147fa0c5  mandog_xqtawyeyhq.png
```
Unfortunately, there was a second level too. This time, we had to generate 8 files having the 
same MD5 sum (not necessarily the same as orginal file). Searching the Internet revealed some
research on this topic - in particular, there was a nice utility called
[fastcol](https://marc-stevens.nl/research/). It only generates two suffixes, which appended
make the same md5, but we could easily adapt it to our purposes by running it several times,
creating in the end 8 files:
```
[original][suffix1A][suffix2A][suffix3A]
[original][suffix1A][suffix2A][suffix3B]
[original][suffix1A][suffix2B][suffix3A]
[original][suffix1A][suffix2B][suffix3B]
[original][suffix1B][suffix2A][suffix3A]
[original][suffix1B][suffix2A][suffix3B]
[original][suffix1B][suffix2B][suffix3A]
[original][suffix1B][suffix2B][suffix3B]
```
Full code is in `doit.py`. Results:
```
[adam@adam-Y510P ~/CTF/backdoor/forge/lvl2]λ md5sum collision_*
0c98a972db583485b9e3e40fe276137a  collision_0.png
0c98a972db583485b9e3e40fe276137a  collision_1.png
0c98a972db583485b9e3e40fe276137a  collision_2.png
0c98a972db583485b9e3e40fe276137a  collision_3.png
0c98a972db583485b9e3e40fe276137a  collision_4.png
0c98a972db583485b9e3e40fe276137a  collision_5.png
0c98a972db583485b9e3e40fe276137a  collision_6.png
0c98a972db583485b9e3e40fe276137a  collision_7.png
[adam@adam-Y510P ~/CTF/backdoor/forge/lvl2]λ sha1sum collision_*
ca3e10e251928fa00b83f8393a7fa0866fd0e3b8  collision_0.png
e9d30bf12afa70d0c873848ef89e6c57e7b184fe  collision_1.png
f0cdb53c0ed2e2ac200eeacfc2a7d05d31316902  collision_2.png
aa6c6ea0b3af31fad2ae839535cf5789d2d15ff6  collision_3.png
0b66cbe4054d6b2fa5ad8308fde46fbb043e8d4a  collision_4.png
33d3294af9aae77276a913c9c6bd03514b06a292  collision_5.png
e032a2b878134e601fec416d8b08e2d7eb91c16f  collision_6.png
32ad04e28daacb4e60b6adcdf5dfd8a7b1578981  collision_7.png
```
