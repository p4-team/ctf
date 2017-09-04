# Baby DLP (crypto)


## ENG
[PL](#pl-version)

In the task we get [server code](server.py) to analyse.
In short we can send to the server a number `s` and server responds with `c = pow(2, flag ^ s, p)`.
Our goal is, of course, to recover the flag.

As the taks name suggests, if we could calculate discrete logarithm, we could easily get back the flag.

But it's not the only way.
Let's look closely what the server does - it XORs the exponent with a value we provide!
What would happen if we flip a single bit in the exponent?

- If we change `k-th` bit from 0 to 1 then we simply add `2**k` to the exponent. It means that `c' = pow(2, flag + 2**k, p) = c * pow(2, 2**k, p) mod p`
- Otherwise we must have changed `k-th` bit from 1 to 0.

Flipping a single bit is trivial, we simply need to send as input a number which has only a single high bit as `k-th` position, and this will flip the `k-th` bit of the `flag` on the server.

So the solution is:

1. Send `0` as input to recover original `c` value from the server
2. Send `1`,`2`,`4`,...,`2**k` as input and check if `result == c * pow(2, 2**k, p) % p` and if it is then `k-th` bit was originally `0`, otherwise it was `1`

```python
from Crypto.Util.number import size, long_to_bytes
from crypto_commons.netcat.netcat_commons import nc, send


def main():
    url = 'ppc2.chal.ctf.westerns.tokyo'
    port = 28459
    s = nc(url, port)
    p = 160634950613302858781995506902938412625377360249559915379491492274326359260806831823821711441204122060415286351711411013883400510041411782176467940678464161205204391247137689678794367049197824119717278923753940984084059450704378828123780678883777306239500480793044460796256306557893061457956479624163771194201
    g = 2
    send(s, '0')
    reference = int(s.recv(99999)[2:], 16) # original ciphertext
    payload = 1L
    bits = []
    for i in range(size(p)):
        print('testing ', i)
        send(s, hex(payload)[2:-1])
        result = int(s.recv(99999)[2:], 16)
        if result == (reference * pow(g, payload, p)) % p:
            bits.append('0')
        else:
            bits.append('1')
        payload <<= 1
    bts = "".join(bits)
    print(bts)
    print(long_to_bytes(int(bts[::-1], 2)))


main()
```

This gives us: `TWCTF{0f97c1c3ac2aedbd7fb8cd39d50f2b561d31f770}`

## PL version
