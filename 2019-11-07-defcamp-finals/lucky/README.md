# Lucky (web, 304p, 5 solved)

A rather strange problem.
We get access to a service which supposedly has closed its routing and it is returning only `index.php` page and `404.php`, and anything apart from `index.php` rediects to 404.
After some fuzzing we finally noticed that requesting `404.php` with `HTTP/1.0` request directly has some strange behaviour - we can get 2 different responses.
One is returned as `HTTP/1.0` and the other `HTTP/1.1`.

We spend lots of time trying to understand how this can be useful -> we thought that maybe sometimes we're hitting the proxy/load balancer which is redirectig everything to 404, but other times we're reaching the php server directly, and maybe we could force Keep-Alive on the connection and send more requests for this server.

However, it turned out to be much weirder. 
The flag was being broadcasted in binary format in the form of `1.0` or `1.1` HTTP protocol version:

```python
from crypto_commons.netcat.netcat_commons import nc

known = set()
bits = []
while True:
    s = nc("167.172.172.196", 8889)
    s.sendall("GET /404.php HTTP/1.0\r\nHost: aaa\r\n\r\n")
    x = s.recv(9999)
    if "500" in x:
        bits = []
        continue
    else:
        print(bits)
    print(x)
    if x not in known:
        known.add(x)
        if "1.0" in x:
            bits.append(0)
        else:
            bits.append(1)
    s.close()
```

There were some issues here: the server was crashing/stalling all the time, and we were missing bits and pieces of the flag.
After each crash the server would also broadcast a different, random piece of the flag bitstream.

We had to recover the original bits by combining triplets (we were getting data once per second and bits were changed every 3 seconds) and accunting for misssing onces (due to timing issues).

Then we had to combine the bits into flag bytes:

```python
offset = 0
real_bits = []
counter = 0
prev = bits[0]
for bit in bits:
    if bit != prev:
        if counter % 3 == 1:
            counter -= 1
        elif counter % 3 == 2:
            counter += 1
        for _ in range(counter / 3):
            real_bits.append(prev)
        counter = 1
    else:
        counter += 1
    prev = bit
print(real_bits)

chunks = chunk_with_remainder(real_bits[offset:], 8)
res = ""
for chunk in chunks:
    c = chr(int("".join(map(str, chunk)), 2))
    if c in string.lowercase or c in string.digits or c in "DCTF{}":
        res += c
    else:
        res += 'X'
print(res)
```

Notice that we had to include a heuristic for missing values in triplets (it happened sometimes) and also to test all 8 start offsets (we don't know if the first bit we recovered is not somewhere in the middle of a flag character).

Since the server was crashing, the flag was broadcasted in pieces.
It took about 3h to recover enough pieces to solve a small jigsaw puzzle like:

```
DCTF{aa0f350d4
                                                          3b463e50820
                                                            463e50820}
                                       a90d80afbf98643f8bf
             447e4df83l              d8a90d80afbf9864
              47e4df83e7543f   
                        543fa86a26c14d8a9
                               a26c14d8a90d
                            a86a26c14d8a90
```

and re-assemble the flag: `DCTF{aa0f350d447e4df83e7543fa86a26c14d8a90d80afbf98643f8bf3b463e50820}`
