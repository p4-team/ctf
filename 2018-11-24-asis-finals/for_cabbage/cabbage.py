import base64
from time import time

import brotli

from crypto_commons.netcat.netcat_commons import nc, send, receive_until, receive_until_match


def main():
    s = nc("37.139.4.247", 31337)
    data = receive_until(s, "\n")
    print(brotli.decompress(data.decode("base64")))
    data = receive_until(s, "\n")
    print(brotli.decompress(data.decode("base64")))
    payload = int(time())
    print(payload)
    send(s, base64.b64encode(brotli.compress(str(payload))))
    data = receive_until_match(s, "\n\n")
    print(data)
    data = receive_until(s, "\n")
    print(brotli.decompress(data.decode("base64")))
    data = receive_until(s, "\n")
    print(brotli.decompress(data.decode("base64")))
    data = receive_until(s, "\n")
    print(brotli.decompress(data.decode("base64")))
    send(s, base64.b64encode(brotli.compress("Y")))
    data = receive_until(s, "\n")
    decompressed = brotli.decompress(data.decode("base64"))
    print('payload', decompressed)
    send(s, base64.b64encode(brotli.compress(decompressed)))
    data = receive_until(s, "\n")
    decompressed = brotli.decompress(data.decode("base64"))
    print(decompressed)
    data = receive_until(s, "\n")
    decompressed = brotli.decompress(data.decode("base64"))
    print(decompressed)


main()
