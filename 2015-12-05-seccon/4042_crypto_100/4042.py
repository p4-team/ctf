import codecs


def convert_single_char(start_pos, bits):
    end_pos = 9
    continuation = int(bits[start_pos])
    character = bits[start_pos + 1:start_pos + 9]
    c = int(character, 2)
    if continuation:
        character = bits[start_pos + 9:start_pos + 18]
        c <<= 8
        c += int(character, 2)
        end_pos += 9
    return unichr(c), end_pos


def convert_utf9(data):
    data_in_bin = bin(data)[2:]
    print(data_in_bin)
    print(len(data_in_bin))
    init = 0
    result = u""
    while init < len(data_in_bin):
        character, end_pos = convert_single_char(init, data_in_bin)
        result += character
        init += end_pos
    print(result)


def main():
    with codecs.open("4042.txt") as file:
        data = file.read()
        data = data.replace("\n", "")
        number = int(data, 8)
        print(number)
        convert_utf9(number)


main()
#SECCON{A_GROUP_OF_NINE_BITS_IS_CALLED_NONET}