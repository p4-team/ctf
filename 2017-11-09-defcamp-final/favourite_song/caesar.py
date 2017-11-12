import codecs
import re

from crypto_commons.generic import chunk


def get_sounds():
    with codecs.open("killthegauls.xml", "r") as input_file:
        data = input_file.read()
        return re.findall("<step>(.*)</step>\s*.*\s*<octave>(.*)</octave>", data)


def main():
    sounds_list = get_sounds()
    print(sounds_list)
    final = []
    for sound in sounds_list:
        pitch = sound[0]
        octave = int(sound[1]) - 4
        if octave > 0:
            final_sound = pitch.lower()
        else:
            final_sound = pitch
        final.append(final_sound)
    parts = chunk("".join(final), 2)
    print(parts)
    scale = "DEFGABcdefgab"  # D-major
    x = []
    for part in parts:
        first = part[0]
        second = part[1]
        res = scale.index(first) << 4
        res += scale.index(second)
        x.append(res)
    flag = "".join([chr(c) for c in x])
    print(flag)


main()
