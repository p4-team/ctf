import urllib
from PIL import Image
import io
from pytesseract import pytesseract
import urllib2
import re


def get_filling(pixels, i, j, best_colors, x_range):
    left = pixels[(i - 1) % x_range, j]
    right = pixels[(i + 1) % x_range, j]
    if left in best_colors and left != best_colors[0]:
        return left
    elif right in best_colors and right != best_colors[0]:
        return right
    else:
        return best_colors[0]


def fix_colors(im):
    colors_distribution = im.getcolors()
    ordered = sorted(colors_distribution, key=lambda x: x[0], reverse=True)
    best_colors = [color[1] for color in ordered]
    if (255, 255, 255) in best_colors:
        best_colors.remove((255, 255, 255))
    best_colors = best_colors[:2]
    pixels = im.load()
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            color = pixels[i, j]
            if color not in best_colors:
                pixels[i, j] = get_filling(pixels, i, j, best_colors, im.size[0])
    return best_colors[0]


def on_blacklist(text):
    if len(text) != 4:
        return True
    blacklisted = ["I", "0", "O", "Z", "Q", "2", "S", "3", "G", "9", "1", "l", "C", "X", "V", "B", "8", "U"]
    for character in blacklisted:
        if character in text:
            return True
    matcher = re.match("[a-zA-Z0-9]+", text)
    if matcher is None or len(matcher.group()) != 4:
        return True
    return False


def black_and_white(im, filling):
    black = (0, 0, 0)
    white = (255, 255, 255)
    pixels = im.load()
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            color = pixels[i, j]
            if color == filling:
                pixels[i, j] = white
            else:
                pixels[i, j] = black


while True:
    try:
        lastScore = 0
        cookies = urllib2.HTTPCookieProcessor()
        opener = urllib2.build_opener(cookies)
        urllib2.install_opener(opener)
        opener.open("http://ctfquest.trendmicro.co.jp:8080/acf2e28903f698eda9bdefc043b6edc3/signin")
        params = dict(username="p4test", password="p4test", this_is_the_login_form=True)
        params.update({c.name: c.value for c in cookies.cookiejar})
        encoded_params = urllib.urlencode(params)
        opener.open("http://ctfquest.trendmicro.co.jp:8080/acf2e28903f698eda9bdefc043b6edc3/signin", encoded_params)
        while True:
            f = opener.open("http://ctfquest.trendmicro.co.jp:8080/acf2e28903f698eda9bdefc043b6edc3/challenge")
            data = f.read()
            print(data.replace("\n", " "))
            # <h2>6/500</h2>
            m = re.search("<h2>(\d+)/\d+</h2>", data)
            if m is not None:
				s = m.group(1)
                print(s)
                if int(s) < lastScore:
                    lastScore = int(s)
                    im.show()  # debug, display failed captcha to improve blacklist
                else:
                    lastScore = int(s)
            f = opener.open("http://ctfquest.trendmicro.co.jp:8080/acf2e28903f698eda9bdefc043b6edc3/image")
            image_file = io.BytesIO(f.read())
            im = Image.open(image_file)
            im = im.convert('RGB')
            filling = fix_colors(im)
            black_and_white(im, filling)
            text = pytesseract.image_to_string(im,
                                               config="-psm 8 --user-patterns /cygdrive/d/tess/pattern.txt /cygdrive/d/tess/conf.txt")
            text = text.replace(" ", "")
            if not on_blacklist(text):
                print(text)
                params = {"captcha": text}
                params.update({c.name: c.value for c in cookies.cookiejar})
                encoded_params = urllib.urlencode(params)
                opener.open("http://ctfquest.trendmicro.co.jp:8080/acf2e28903f698eda9bdefc043b6edc3/challenge",
                            encoded_params)
            else:
                print "Possibly wrong decode " + text + " skipping"
	except:
        pass
