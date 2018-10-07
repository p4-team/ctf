# Bwv2342 (reverse, 499p, 4 solved)

In the challenge we get a [binary](bwv2342) which was obfuscated by movfuscator.
We also get a netcat address for the server running the binary.

We tried using some de-movfuscators but to no avail.
Therefore we decided to try blackbox approach.

Using `ltrace` and `strace` we could see that the binary opens `flag.txt`, so to do some local tests we should make sych file.
Sadly tracing didn't show anything useful apart from that.

The binary reads input from us and prints as output `notes` as for example `C#1` or `G 2`.

Once we created local flag file and checked what results we get from the binary, when providing proper flag prefix vs. random data, we noticed that there is a difference.
We usually get a `lower` note for the proper data.
It can be handled even easier, since basically the result for correct prefix is simply different, and all others are the same!

If for example we send `h` then result will be `X`, and if we send any other character the result will be `Y`.

This means we can easily brute-force the flag byte by byte with:

```python
import re
import string
from collections import defaultdict

from crypto_commons.netcat.netcat_commons import nc, send, receive_until_match, receive_until


def main():
    url = "bwv2342.ctf.hackover.de"
    port = 1337
    s = nc(url, port)
    s.recv(9999)
    prefix = ''
    charset = string.letters + string.digits + string.punctuation + " "
    while True:
        corr = {}
        symbols = defaultdict(int)
        for c in charset:
            send(s, prefix + c)
            res = receive_until(s, "\n")
            receive_until_match(s, "Please enter your guess:\n")
            symbol = re.findall("(.*)", res)[0]
            corr[symbol] = c
            symbols[symbol] += 1
        print(symbols)
        print(corr)
        for symbol, c in symbols.items():
            if c == 1:
                prefix += corr[symbol]
                break
        print(prefix)


main()
```

We simply test all possible character from charset, and count the results.
The proper result is the one with `counter = 1`.

After a moment we recover: `hackover18{M0V_70_7h4_w0h173mp3r13r73_Kl4v13r}`
