import codecs
import itertools
import re
from Crypto.Cipher import AES


def read_data(file):
    with codecs.open(file, "r") as input_file:
        input_file.readline()
        input_file.readline()
        data = input_file.readline()
        return data


def get_agreed_bytes(data_sent, bases_measured, bases_correct, v1, v2):
    agreed_bits = []
    for i in range(len(bases_correct)):
        if bases_correct[i] == 'v':
            if bases_measured[i] == '+':
                if data_sent[i] == '-':
                    agreed_bits.append(v1)
                else:
                    agreed_bits.append(abs(v1 - 1))
            else:
                if data_sent[i] == '/':
                    agreed_bits.append(v2)
                else:
                    agreed_bits.append((abs(v2 - 1)))
    return hex(int("".join([str(c) for c in agreed_bits]), 2))[2:-1]


def main():
    data_sent = read_data("q_transmission_1")
    bases_measured = read_data("q_transmission_2")
    bases_correct = read_data("q_transmission_3")
    flag = '269118188444e7af980a245aedce5fb2811b560ccfc5db8e41f102a23f8d595ffde84cb1b3f7af8efd7a919bd2a7e6d3'.decode(
        "hex")
    for x in itertools.product([0, 1], repeat=2):
        data = get_agreed_bytes(data_sent, bases_measured, bases_correct, x[0], x[1])
        try:
            printable = data.decode("hex")
            print('potential key', printable)
            iv = re.findall("iv:(.*?),", printable)[0]
            key = re.findall("key:(.*?),", printable)[0]
            print(iv, key)
            cipher = AES.new(key.decode("hex"), AES.MODE_CBC, iv.decode("hex"))
            print(cipher.decrypt(flag))
        except:
            pass


main()
