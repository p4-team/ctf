import base64
print base64.b64decode("".
        join([chr(int(x, 8)) for x in open("README.txt").read().split(" ")]))
