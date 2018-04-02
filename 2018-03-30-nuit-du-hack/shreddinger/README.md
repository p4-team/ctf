# Shreddinger, 500p, dev

> The infamous Shredder tried to destroy important documents ! Please, help us recover them and prevents their evil scheme.

In this task we were given a simulated piece of paper cut into a hundred strips,
as though it went through idealized shredding machine. We were supposed to
piece them together to obtain original image, then read the written message -
all within ten seconds.

Our solution was based on simulated annealing - basicly start with a random
permutation of pieces, then try to randomly swap two of them and check if 
the resulting picture is better than previous one - if not, keep the old
configuration, else the new. With small probability we also mutated it anyway,
to escape local minima. Another kind of move was 180 degree rotation of random
subsequence of strips.

Score of a configuration was defined as sum of differences of pixels on seams.
Since this is a pretty expensive operation to calculate, we preprocessed the
pieces and calculated partial scores of each pair of strips assuming they're
neighbours. This was still too slow, so we rewrote the SA part to C++.

Finally, when we stitched together the image, we still had to OCR it. Usual
tools - tesseract and friends - were useless for this font, so we manually
created the font images and wrote our own OCR in Python.

The whole script was rather hacky and kind of slow (it was usually taking 
almost the full 10 seconds), it was failing randomly, but after a couple of 
tries, we managed to pass the checks.
