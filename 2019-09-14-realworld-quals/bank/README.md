# Bank (crypto, 94p)

In the challenge we get two files.
First one contains [properly looking Schnorr signature code](schnorr.py) and the second one is the [server code](multi-schnorr.py).

The application generates a new private-public key for the server and then in look:

- asks us for our public key
- ask for action to perform

We can perform 3 actions:

1. Send `DEPOSIT` message signed with our private key and server will verify this signature agains the public key we send initially.
2. SEND `WITHDRAW` message signed with our private key and with server private key, and server will verify this with our public key combined with server public key (in this context it means our ECC Public Key Point will be added to the server Point).
3. As for server public key.

There are 2 key points to notice here:

1. In given connection (so while server maintains his private-public key pair) we can perform multiple operations and each one of the for `different` public key. This is because public key is requested every time.
2. Adding and subtracting points on Elliptic Curve is not a difficult operation. It's "division" that is the hard operation that security is based on. This means if we have points `P` and `Q` it's very simple to calculate point `S` such that `P+S = Q`. Subtraction is simply addition of point with `y` coordinate negated, so `S = P-Q = (xp,yp)+(xq,-yq)`

The layout of the attack is pretty simple:

1. Generate some private-public keypair for ourselves (`P` and `pP`).
1. Send our public key `P` and request server public key, let's call it point `Q`.
2. Send our public key `P` and send `DEPOSIT` message signed with our private key `pP`.
4. Calculate point `S = P-Q = (xp,yp)+(xq,-yq)`
5. Send point `S` as our public key and send `WITHDRAW` operation signed with our private key `pP`.
6. Now the server will add their public key `Q` to our public key `S` to verify our message. But `S+Q = P-Q+Q = P`, our public key, for which `pP` is the corresponding private key.
7. The message will be properly verified and we will get back the flag.

We implement this by:

```python
def main():
    host = "tcp.realworldctf.com"
    # host = "localhost"
    port = 20014
    s = nc(host, port)
    data = receive_until(s, "\n").strip()
    prefix = data[-16:]
    print(data)
    print(prefix)
    res = breakPoW(prefix)
    s.sendall(res)
    
    sk, pk = generate_keys()
    real_key_message = (str(pk[0]) + "," + str(pk[1]))
    send(s, base64.b64encode(real_key_message))

    send(s, base64.b64encode("1"))
    deposit_signature = schnorr_sign("DEPOSIT", sk)
    send(s, base64.b64encode(deposit_signature))

    send(s, base64.b64encode(real_key_message))

    send(s, base64.b64encode("3"))
    data = receive_until_match(s, "one of us: .*\n")
    serverPk = re.findall("one of us: (.*)\n", data)[0].replace("(", "").replace(")", "").replace("L", "")
    serverPk = (int(serverPk.split(",")[0]), int(serverPk.split(",")[1]))
    Q = point_add(pk, (serverPk[0], (-serverPk[1]) % p))
    
    fake_key_message = (str(Q[0]) + "," + str(Q[1]))
    send(s, base64.b64encode(fake_key_message))

    withdraw_signature = schnorr_sign("WITHDRAW", sk)
    send(s, base64.b64encode("2"))
    send(s, base64.b64encode(withdraw_signature))
    interactive(s)


main()
```

And we get back the flag: `rwctf{P1Ain_SChNorr_n33Ds_m0re_5ecur1ty!}`
