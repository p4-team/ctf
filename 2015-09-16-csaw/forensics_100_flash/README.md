## Flash (forensics, 100p, 809 solves)
`We were able to grab an image of a harddrive. Find out what's on it.`.

### PL Version
`for ENG version scroll down`

Dostajemy 128MB obraz dysku.
Nie myśleliśmy nawet o tym, żeby go montować, bo spodziewaliśmy się pustego dysku (pisząc writeup pokusiliśmy się o to i się nieźle zdziwilismy ). Pierwszą rzeczą jaka przyszła nam do głowy był `photorec`, który nie znalazł nic ciekawego, dlatego wykonalismy `strings flash_c8429a430278283c0e571baebca3d139.img | grep flag`.

Dostajemy flagę `flag{b3l0w_th3_r4dar}`.

### ENG Version

Image of 128MB disk was provided.
We had not even thought about mounting it, because we were expecting that the disk will be empty (while writing this writeup, we actually did that, and there were a lot of text files which was great suprise). So according too the standard procedure, we have tried `photorec`,
but it have not found any images, so we executed `strings flash_c8429a430278283c0e571baebca3d139.img | grep flag`.

At the end of output was the `flag{b3l0w_th3_r4dar}`.
