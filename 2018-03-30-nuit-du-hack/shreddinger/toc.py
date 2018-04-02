import numpy as np
from PIL import Image
import sys
import math
import glob
import scipy.misc
import pytesseract

import subprocess
import matplotlib.pyplot as plt
import random


def captcha(image):
    letters = "ABCDEF1234567890"
    let = {}
    for l in letters:
        f = Image.open("charset/%c.png" % l).convert("L")
        f = np.array(f.getdata(), dtype=np.uint8).reshape(f.size[::-1])
        let[l] = f < 255

    chars = []
    while True:
        #plt.imshow(image)
        #plt.show()
        best = []
        for l in let:
            letter = let[l]
            area = letter.shape[0] * letter.shape[1]
            i = 9
            #for i in range(image.shape[0] - letter.shape[0] + 1):
            for j in range(image.shape[1] - letter.shape[1] + 1):
                diff = image[i:i+letter.shape[0], j:j+letter.shape[1]] ^ letter
                diff = np.sum(diff) / float(area)
                best.append((diff, l, i, j))

        best.sort()
        diff, l, i, j = best[0]
        if diff > 0.1:
            break
        chars.append((j, l))
        print diff, "".join(c[1] for c in sorted(chars))
        image[i:i+let[l].shape[0], j:j+let[l].shape[1]] = 0

    return "".join(c[1] for c in sorted(chars))


def solve(directory):
    files = sorted(glob.glob(directory + "/*"))
    images = []
    for i, f in enumerate(files):
        f = Image.open(f).convert("L")
        f = np.array(f.getdata(), dtype=np.uint8).reshape(f.size[::-1])
        images.append(f)

    images.append(np.full((1400, 10), 255))
    images = [images[-1]] + images


    n = len(images)
    weights = {}
    for i in range(n):
        for j in range(n):
            for ri in range(2):
                for rj in range(2):
                    if ri == 0:
                        l = images[i][:, 9]
                    else:
                        l = images[i][::-1, 0]
                    if rj == 0:
                        r = images[j][:, 0]
                    else:
                        r = images[j][::-1, 9]
                    weights[(i, j, ri, rj)] = np.sum(np.abs(l - r))

    with open("/tmp/spec", "w") as f:
        f.write(str(n)+"\n")
        for i in range(n):
            for j in range(n):
                for ri in range(2):
                    for rj in range(2):
                        f.write(str(weights[(i, j, ri, rj)])+"\n")
        
    ss = subprocess.check_output(["./a.out"])
    ss = [int(c) for c in ss.split()]
    perm = ss[:n]
    rots = ss[n:]

    imgs = []
    for i in perm:
        imgs.append(images[i])
    for i, r in enumerate(rots):
        if r:
            imgs[i] = np.rot90(imgs[i], 2)
    image = np.concatenate(imgs, axis=1)
    image = image[680:720, :]

    if np.min(image[35, :]) != 0:
        image = np.rot90(image, 2)

    image = image < 255

    scipy.misc.imsave("temp.png", image)

    txt = captcha(image)
    print "Final captcha:", txt
    return txt

from requests import Session
import os



os.system("rm -r /tmp/chall")
os.system("mkdir /tmp/chall")


s = Session()
s.get("http://shreddinger.challs.malice.fr/")
r = s.get("http://shreddinger.challs.malice.fr/challenge_accepted")


with open('/tmp/challenge.zip', 'wb') as f:
    f.write(r.content)
os.system("unzip /tmp/challenge.zip -d /tmp/chall")

code = solve("/tmp/chall")

r = s.post("http://shreddinger.challs.malice.fr/", data={"shredded_token":code})
print(r.content)

#                             <strong>Congratz !</strong> The flag is : NDH{H0ly_fr@cking_PONY_!--D3Ath-to-the_0n3_whO-ordered_piZzas-w!th_pineapple_!}

