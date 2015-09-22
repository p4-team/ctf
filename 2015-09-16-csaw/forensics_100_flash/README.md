## Flash (forensics, 100p, 809 solves)
Treść zadania brzmi `We were able to grab an image of a harddrive. Find out what's on it.`.
Dostajemy 128MB obraz dysku. Nie myślałem nawet o tym, żeby go montować, bo spodziewalem sie pustego dysku (pisząc writeup pokusiłem się o to i się nieźle zdziwiłem :P ). Pierwszą rzeczą jaka przyszła mi do głowy był `photorec`, który nie znalazł nic ciekawego, dlatego wykonałem `strings flash_c8429a430278283c0e571baebca3d139.img | grep flag`.

Dostajemy flagę `flag{b3l0w_th3_r4dar}`.

