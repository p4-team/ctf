# Fireplace (reverse, ppc, 763p)

> As it is in love and war, all is fair during the elections, especially when it comes to an opportunity to get rid of a candidate who is three points ahead of you. Your secret agent in this candidate’s campaign office informed you of some secret documents which prove that your rival is guilty of bribery. Unfortunately, one of his assistants noticed these documents and threw it into the fireplace before leaving the office, but your agent managed to damp down the fire and grab the pieces. Restore the document and help you candidate to win!

> fireplace.tar

In this task we were given a binary and a random-looking BMP picture. The binary accepted a single command line 
argument - filename. When given any BMP picture, it would encrypt it somehow and overwrite the original picture.

Reverse engineering the binary showed it generates an internal square picture using Windows standard `rand` function
for pixel values. The input image, when interpreted as a matrix of 24-bit RGB values is then multiplied (as in
matrix multiplication) with that square image and saved as the output. All operations are done modulo `2**24`.

So, we get the following equation: `Input * Square = Output`. Since we know the Output matrix (it's the 
random-looking BMP) and Square (Windows `rand` is deterministic - LCG), we can multiply both sides of the equation
by modular inverse of Square matrix to get: `Input = Output * modinv(Square)`. We implemented this in mixture
of Python and Sage and retrieved the original image.
