## Flash (forensics, 100p, 809 solves)
`We were able to grab an image of a hard drive. Time to find out what's on it.`.

### PL Version
`for ENG version scroll down`

Dostajemy 128MB obraz dysku.
Nie myśleliśmy nawet o tym, żeby go montować, bo spodziewaliśmy się pustego dysku (pisząc writeup pokusiliśmy się o to i się nieźle zdziwilismy ). Pierwszą rzeczą jaka przyszła nam do głowy był `photorec`, który nie znalazł nic ciekawego, dlatego wykonalismy `strings flash_c8429a430278283c0e571baebca3d139.img | grep flag`.

Dostajemy flagę `flag{b3l0w_th3_r4dar}`.

### ENG Version

Image of 128MB disk was provided.
We were expecting it to be completly empty, so we didn't even bother mounting it (we actually tried that while writing this writeup and it turned out there were a lot of text files, which was great suprise). So according to the standard procedure, we tried using `photorec`,
but it did not find any images, so we executed `strings flash_c8429a430278283c0e571baebca3d139.img | grep flag`.

The last line of grep output was: `flag{b3l0w_th3_r4dar}`.
