import codecs

from PIL import Image


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


def similar_color(c1, c2):
    return [abs(c1[i] - c2[i]) for i in range(3)]


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


def main():
    colors = ["red", "orange", "yellow", "green", "cyan", "blue", "purple", "white"]
    lu = (396, 124)
    ld = (406, 619)
    rd = (892, 609)
    ru = (888, 121)
    prev = []
    printed = False
    with codecs.open("out.txt", "w") as output_file:
        import sys
        file_path = sys.argv[1]
        img = Image.open(file_path)
        pixels = img.load()
        result = []
        for row_id in range(8):
            rows = []
            for col_id in range(8):
                col1 = (ld[0] * row_id / 7.0 + lu[0] * (1 - row_id / 7.0))
                col2 = (rd[0] * row_id / 7.0 + ru[0] * (1 - row_id / 7.0))
                column = int(col1 + (col2 - col1) / 7.0 * col_id)
                row1 = (ru[1] * col_id / 7.0 + lu[1] * (1 - col_id / 7.0))
                row2 = (rd[1] * col_id / 7.0 + ld[1] * (1 - col_id / 7.0))
                row = int(row1 + (row2 - row1) / 7.0 * row_id)
                sum = (0, 0, 0)
                size_x = 20
                size_y = 20
                cnt = 0
                for delta_x in range(-size_x, size_x):
                    for delta_y in range(-size_y, size_y):
                        color = pixels[column + delta_x, row + delta_y]
                        grey = (130, 130, 130)
                        if max(similar_color(grey, color)) < 40:
                            continue
                        # pixels[column + delta_x, row + delta_y] = (0, 0, 0)
                        sum = (sum[0] + color[0], sum[1] + color[1], sum[2] + color[2])
                        cnt += 1
                divisor = cnt
                avg = (sum[0] / divisor, sum[1] / divisor, sum[2] / divisor)
                result_color = convert_color(avg)
                if result_color in ["orange", "yellow"]:
                    print "Handle", row_id, col_id
                    result_color = handle_orange_and_yellow(pixels, column, row)
                # rows.append((result_color))
                rows.append(colors.index(result_color))
            result.append(rows)

        data = "[" + ",".join([",".join(map(str, r)) for r in result]) + "]"
        output_file.write(data + "\n")
        print(data)
        printed = True
        prev = result
        # img.show()
        # print("\n".join(map(str, result)))
        # print("\n")
    pass


main()
