from crypto_commons.netcat.netcat_commons import nc, send, receive_until_match
from crypto_commons.oracle.lsb_oracle import lsb_oracle


def oracle(s, payload):
    send(s, 'l')
    receive_until_match(s, "\:\>\>", None)
    send(s, str(payload))
    send(s, str(1))
    send(s, str(1))
    data = receive_until_match(s, "\:\>\>", None)
    return "bit is wrong" in data


def multiplicate(x, e, n):
    return (pow(2, e, n) * x) % n


def main():
    url = "47.75.53.178"
    port = 9999
    s = nc(url, port)
    data = receive_until_match(s, "\:\>\>", None).split("\n")
    e = int(data[1])
    n = int(data[2])
    print(e, n)
    send(s, 'r')
    receive_until_match(s, "\:\>\>", None).split("\n")
    send(s, 'test')
    data = receive_until_match(s, "\:\>\>", None).split("\n")
    ct = int(data[0])
    lsb_oracle(ct, lambda x: multiplicate(x, e, n), n, lambda ct: oracle(s,ct))


main()