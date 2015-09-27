import urllib
from PIL import Image
import io, re

handle = urllib.urlopen("http://ctfquest.trendmicro.co.jp:43210/click_on_the_different_color")
data = handle.read()


def extractLink(data):
    x = re.search("window.location.href=(.*\\?)", data)
    return x.group(1)[2:-1]


def getPixel(picture_path):
    fd = urllib.urlopen(picture_path)
    image_file = io.BytesIO(fd.read())
    im = Image.open(image_file)
    colors_distribution = im.getcolors()
    non_white = [color for color in colors_distribution if color[1] != (255, 255, 255)]
    ordered = sorted(non_white, key=lambda x: x[0], reverse=False)
    print(ordered[0])
    width, height = im.size
    for index, color in enumerate(im.getdata()):
        if color == ordered[0][1]:
            y = index / width
            x = index % width
            return x, y


try:
    count = 0
    while True:
        print(count)
        link = extractLink(data)
        picture_path = "http://ctfquest.trendmicro.co.jp:43210/img/" + link + ".png"
        x, y = getPixel(picture_path)
        handle = urllib.urlopen("http://ctfquest.trendmicro.co.jp:43210/" + link + "?x=" + str(x) + "&&y=" + str(y))
        data = handle.read()
        count += 1
except Exception as e:
    print(e)
    print(data)
