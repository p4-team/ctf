# Matrix LED (re, 462p, 3 solves)

```
MatrixLED.7z
https://youtu.be/C6cux2fM7fg
Update(2018-09-01 20:05 UTC):
The contents of flag.jpg was incorrect, therefore we show below a part of flag.jpg.
00000000: d091 577d 5889 e647 24e3 a93b c1f8 112f  ..W}X..G$..;.../
00000010: 86d0 f06b e859 0728 2962 9b1d a7bf 74b8  ...k.Y.()b....t.
=============================== snip ==============================
0000d100: 761c 538c c367 0f9b 945c 3a3f ca6f 40db  v.S..g...\:?.o@.
0000d110: 3de9 1a4c beab                           =..L..
And the flag is updated.
The new flag is
from hashlib import md5
print 'TWCTF{{{}}}'.format(md5(open('flag.jpg', 'rb').read()).hexdigest())
```

## Overview

In this task we got an AVR binary file (a stripped ELF) and a link to YouTube video. The movie showed
an 8x8 LED matrix, blinking with various colors a couple of times per second. We also had a Python script
that showed communication between computer and board - basically sending random key and plaintext flag file.

## AVR Binary

Reverse engineering the binary was tedious, but relatively straightforward - the flag was displayed on
the matrix in 16 byte blocks, using 8 distinct colours to represent 3 bits. There was also an 8-byte cheksum
appended to each block. The flag blocks were encrypted before showing.

We reverse engineered the encryption algorithm. It was similar to AES in structure, as it had rounds
consisting of four operations. There were 20 rounds though and each of these was somewhat modified from
real AES. Three of them were short enough we transcribed them to Python pretty quickly: these were
(a) XOR with key and some constants, (b) xoring state bytes, (c) permuting state bytes. The remaining
round was too large to reverse, but fortunately it was a simple loop over each status byte, changing
each according to the same function - i.e. Sub from AES. The concrete implementation was convoluted, so we
used `simavr` to simulate the function for each possible input and hardcoded the S-Box in the script.

Each operation was reversible, so writing decryption algorithm was simple and the result is in [doit.py](doitp.py) and [aes.py](aes.py)

## Parsing video

The only thing that remained was transcribing colors from the movie.
We downloaded the movie and dumped all frames using ffmpeg.

Then we wrote a script that for each frame and each LED position calculated average color and classified to one of 8 possibilities.
Initially we wanted to probe just a single pixel or a small slice, but this didn't work very well, because the diodes had white/different colors inside.
Eventually we decided to calculate average color of the whole LED (get all pixels in a rectangle, and then skip all grey ones) and then calculate Euclidean distance from reference colors:

```python
def convert_color(color):
    red = (240, 110, 120, "red")
    green = (40, 240, 175, "green")
    blue = (85, 110, 240, "blue")
    cyan = (70, 215, 240, "cyan")
    yellow = (235, 230, 150, "yellow")
    orange = (230, 200, 130, "orange")
    white = (220, 220, 240, "white")
    purple = (230, 150, 240, "purple")
    colors = [red, green, blue, cyan, yellow, orange, white, purple]
    best_match = (255 * 3, "lol")
    for c in colors:
        diff = color_delta(c, color)
        if diff < best_match[0]:
            best_match = diff, c[3]
    return best_match[1]


def color_delta(c1, c2):
    diff = 0
    for i in range(3):
        diff += abs(c1[i] - c2[i])
    return diff
```

This was mostly correct, but yellows and oranges were often mixed up. 
We wrote a special case for it, using median of green channel to classify LED as one of these:

```python
def handle_orange_and_yellow(pixels, column, row):
    size_x = 20
    size_y = 20
    greens = []
    for delta_x in range(-size_x, size_x):
        for delta_y in range(-size_y, size_y):
            color = pixels[column + delta_x, row + delta_y]
            grey = (130, 130, 130)
            white = (255, 255, 255)
            if max(similar_color(grey, color)) < 20:
                continue
            if max(similar_color(white, color)) < 100:
                continue
            greens.append(color[1])
    x = sorted(greens)[int(len(greens) * 0.75)]
    if x <= 230:
        return "orange"
    else:
        return "yellow"
```

Full script in [here](shal.py)

## Decoding the flag

There were still some errors though, but very little (less than a percent). 
We had to get perfect match though, otherwise the flag would be wrong. 
Thankfully, there was checksum appended to the raw blocks. 
Unfortunately, the code for its generation was very convoluted and long, so we didn't reverse it. 
Instead, we used `simavr` as a blackbox again. 
If the checksum did not match, we tried changing up to two yellows or oranges to the other color, and see if it helped. 
In all but four frames, this was enough, so we transcribed those manually and [decrypted](outfix.txt)

The leds flipped about every 4 frames, so we had to filter out duplicates and potential half-frames.
Finally we could use [reconstruct script](reconstruct.py) on the [1](out0-3000.txt), [2](out3000-6000.txt), [3](out6000-9000.txt), [4](out9000-12000.txt), [5](out12000-15000.txt), [6](outfix.txt) to recover the flag: `TWCTF{7a4f1c3ffe386f1c15bbbb67b43281b4}`
