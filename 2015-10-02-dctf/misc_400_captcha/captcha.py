import os
import urllib
import urllib2
from PIL import Image
import io


def fix_colors(im):
    colors_distribution = im.getcolors(1000)
    ordered = sorted(colors_distribution, key=lambda x: x[0], reverse=True)
    best_colors = [color[1] for color in ordered]
    if (255, 255, 255) in best_colors:
        best_colors.remove((255, 255, 255))
    if (0, 0, 0) in best_colors:
        best_colors.remove((0, 0, 0))
    best_colors = best_colors[:2]
    pixels = im.load()
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            color = pixels[i, j]
            if color not in best_colors:
                pixels[i, j] = best_colors[0]
    return best_colors[0]


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
                # im.show()


def get_coords(im):
    pixels = im.load()
    black = (0, 0, 0)
    xs = []
    ys = []
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            color = pixels[i, j]
            if color == black:
                xs.append(i)
                ys.append(j)
    return min(xs), max(xs), min(ys), max(ys)


def test_configuration(im_pixels, start_x, start_y, symbol_len, symbol_h, symbol_pixels, symbol_x_min, symbol_y_min):
    counter = 0
    black = (0, 0, 0)
    for i in range(symbol_len):
        for j in range(symbol_h):
            if im_pixels[start_x + i, start_y + j] == black:
                if im_pixels[start_x + i, start_y + j] == symbol_pixels[symbol_x_min + i, symbol_y_min + j]:
                    counter += 1
                else:
                    counter -= 1
            elif symbol_pixels[symbol_x_min + i, symbol_y_min + j] == black:
                counter -= 1
    return counter


def get_matching(im_pixels, im, x_min, x_max, y_min, y_max, symbol, symbol_pixels, symbol_x_min, symbol_len,
                 symbol_y_min,
                 symbol_h):
    results = []
    for start_x in range(x_min - 1, x_max - symbol_len + 1):
        for start_y in range(y_min - 1, y_max - symbol_h + 1):
            if (start_x + symbol_len < im.size[0]) and (start_y + symbol_h < im.size[1]):
                result = test_configuration(im_pixels, start_x, start_y, symbol_len, symbol_h, symbol_pixels,
                                            symbol_x_min,
                                            symbol_y_min)
                results.append((result, start_x, start_y))
    if len(results) == 0:
        return 0, 0, 0
    return max(results)


def is_to_remove(symbol_pixels, x, y):
    black = (0, 0, 0)
    result = False
    for i in range(-1, 1):
        for j in range(-1, 1):
            result = result or symbol_pixels[x + i, y + j] == black
    return result


def remove_used(picture_pixels, symbol, offset_x, offset_y, symbol_len, symbol_h):
    white = (255, 255, 255)
    symbol_x_min, _, symbol_y_min, _ = get_coords(symbol)
    symbol_pixels = symbol.load()
    for i in range(offset_x, offset_x + symbol_len + 1):
        for j in range(offset_y, offset_y + symbol_h + 1):
            if is_to_remove(symbol_pixels, symbol_x_min + i - offset_x, symbol_y_min + j - offset_y):
                picture_pixels[i, j] = white


def find_letters(im, x_min, x_max, y_min, y_max, alphabet):
    picture_pixels = im.load()
    results = []
    for i in range(6):  # always 6 symbols
        scores = []
        for symbol, (symbol_image, (symbol_x_min, symbol_x_max, symbol_y_min, symbol_y_max)) in alphabet.items():
            symbol_pixels = symbol_image.load()
            symbol_len, symbol_h = symbol_x_max - symbol_x_min, symbol_y_max - symbol_y_min
            best_score_for_symbol, offset_x, offset_y = get_matching(picture_pixels, im, x_min, x_max, y_min, y_max,
                                                                     symbol,
                                                                     symbol_pixels,
                                                                     symbol_x_min, symbol_len, symbol_y_min,
                                                                     symbol_h)
            scores.append((best_score_for_symbol, symbol, offset_x, offset_y, symbol_len, symbol_h, symbol_image))
        best, symbol, offset_x, offset_y, symbol_len, symbol_h, symbol_image = max(scores)
        results.append((symbol, offset_x, best))
        print(symbol, best)
        remove_used(picture_pixels, symbol_image, offset_x, offset_y, symbol_len, symbol_h)
        # im.show()
    return results


def open_image(path):
    im = Image.open(path)
    im = im.convert('RGB')
    return im


def get_solution(im):
    filling = fix_colors(im)
    black_and_white(im, filling)
    x_min, x_max, y_min, y_max = get_coords(im)
    results = find_letters(im, x_min, x_max, y_min, y_max, alphabet)
    results = sorted(results, key=lambda x: x[1])
    for symbol, position, score in results:
        if score < 20:
            return None
    return "".join([x[0] for x in results])


alphabet = {file: open_image("../alphabet/" + file) for file in os.listdir("../alphabet")}
alphabet = {key[:-4]: (image, get_coords(image)) for key, image in alphabet.items()}

opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', 'PHPSESSID=f0nvdes57f0s24afi8tdrscua4'))
urllib2.install_opener(opener)
while True:
    try:
        f = opener.open("http://10.13.37.10/captcha.php")
        image_file = io.BytesIO(f.read())
        imtmp = open_image(image_file)
        im = open_image(image_file)
        if im.size[0] > 0 and im.size[1] > 0:
            # im.show()
            res = get_solution(im)
            if res is not None:
                print res
                params = {'captcha': res}
                encoded_params = urllib.urlencode(params)
                f = opener.open("http://10.13.37.10/", encoded_params)
                webpage = f.read()
                print(webpage)
                if "didn't" in webpage:
                    imtmp.show()
            else:
                print "skipping due to a low score"
    except:
        pass
