# Minesweeper (crypto, 350)

> Find which bombs are real and which are duds---without exploding any of them!

> For those wondering why this is cryptography: This technique can be used to
> detect eavesdropping on a quantum channel, without tipping the eavesdroppers
> off.

This time we were given source code of a go simulation of over 100 bombs, that can be dud or live, similar to 
[this experiment](https://en.wikipedia.org/wiki/Elitzur%E2%80%93Vaidman_bomb_tester).
We have to guess all of them without detonating any. For this, we can use two photons and a number of quantum gates.
Wikipedia article describes how it can be done in 33% probability,
but we need far more than that if we want to guess 100 times correctly.

I found a [Kwiat article](http://www.rle.mit.edu/qem/documents/kwiat-prl-74-4763.pdf), which describes a physical process
that could be used in this problem. Although I'm not an expert at quantum physics, my basic understanding of the principle
is that you shine a photon on polarizer rotated just a bit from the original 
photon polarization. About `sin^2(theta)` of the intensity appears on the other side, and the rest (`cos^2(theta)`) 
reflects back. Now, if the other side contains a bomb, it will be tipped off with probability of (`sin^2(theta)`), which
for small `theta` is approximately equal to `theta^2`. If it does not detonate, we are back at square one - photon is
definitely on the original side.

If we repeat this experiment a number of times (`pi/theta`), then if the bomb wasn't there, the photon will finally 
rotate phase by the whole pi, but if the bomb was there, it will stay at original phase (provided the bomb didn't explode,
which it can do with probability on the order of `theta/pi`).

Still, I had to implement this experiment using given gates. I found 
[another article](http://www.arturekert.org/quantum/lecturenotes/note2.pdf), which shows how to build a polarizer
using Hadamard and phase rotator gates - use sequence Hadamard:Rotate:Hadamard. See `conn.py` for details. 
Anyway, running the code a couple of times (it fails randomly) gave us a flag.
