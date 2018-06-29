from pwn import *
import hexdump
import string
import os
import json

#data = string.letters[:51] * 100000
data = os.urandom(100000)
data = "a" * 15 + data[15:]
data = data[:25 * 3]

def take(s, n):
    return s[:n], s[n:]

def takedd(s):
    x, s = take(s, 4)
    return struct.unpack("<I", x)[0], s

def recurse(s):
    b, s = take(s, 1)
    b = ord(b)
    print hex(b)
    r = []
    if b == 0xf:
        for i in range(4):
            rx, s = recurse(s)
            r.append(rx)
    elif b == 0:
        col, s = take(s, 3)
        col = [ord(c) for c in col]
        return col, s
    else:
        col, s = take(s, 3)
        col = [ord(c) for c in col]
        for i in range(4):
            if b & (1<<i):
                rx, s = recurse(s)
                r.append(rx)
            else:
                r.append(col)
    return r, s


def drawx(im, r, depth, x, y):
    sz = im.size[0] / 2**depth
    if len(r) == 3:
        for xx in range(x, x + sz):
            for yy in range(y, y + sz):
                im.putpixel((xx, yy), tuple(r))
    else:
        drawx(im, r[0], depth + 1, x, y)
        drawx(im, r[1], depth + 1, x+sz/2, y)
        drawx(im, r[2], depth + 1, x, y+sz/2)
        drawx(im, r[3], depth + 1, x+sz/2, y+sz/2)


def draw(w, h, r):
    sz = 1
    while sz < w or sz < h:
        sz *= 2
    im = Image.new("RGB", (sz, sz))
    drawx(im, r, 0, 0, 0)
    im.save("lol.png")

from PIL import Image, ImageDraw
def parse(s):
    magic, s = take(s, 4)
    w, s = takedd(s)
    h, s = takedd(s)
    print magic
    print w
    print h
    hexdump.hexdump(s[:300])
    r, s = recurse(s)
    print repr(s)
    print json.dumps(r, indent = 4)
    draw(w, h, r)

for i in range(2):
    if i == 1:
        data = data[:45] + "a" * 15 + data[60:]
    hexdump.hexdump(data[:25*3])
    r = remote("proprietary.ctfcompetition.com", 1337)
    r.sendline("P6")
    r.sendline("5 5")
    r.sendline("255")
    r.send(data)

    s = r.recvall()
    print "len", len(s)


    parse(s)
