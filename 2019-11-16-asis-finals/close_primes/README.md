# Close primes (PPC, 136p, 34 solved)

In the challenge we can connect to the server and it provides us with a task.
We're supposed to send 512 bit prime `p` such that with the next prime `q` it will have the property that:

`sqrt(q) - sqrt(p) >= 0.000000000000000000000000000000000000000000000000000000000000000000000000016`

From quick tests we noticed that this difference is larger for smaller primes, so we need to search from the smallest 512 bit primes.
It is also, for obvious reasons, larger when the gap between `p` and `q` is large.

We didn't do anything fancy here, we simply run a brute force:

```python
mp.prec = 1024
p = gmpy2.next_prime(2 ** 511)
while True:
    q = gmpy2.next_prime(p)
    eps = mpf("0.000000000000000000000000000000000000000000000000000000000000000000000000016")
    if mp.sqrt(q) - mp.sqrt(p) >= eps:
        print(q - p, eps - (mp.sqrt(q) - mp.sqrt(p)))
        print(mp.sqrt(q) - mp.sqrt(p))
        print(mp.sqrt(q) - mp.sqrt(p) >= eps)
        print(p)
        break
    p = q
```

And after a short moment we got back `6703903964971298549787012499102923063739682910296196688861780721860882015036773488400937149083451713845015929093243025426876941405973284973216824506199727`

Sending this value to the server gives us: `ASIS{C4n_y0U_prOv3__Andrica__Conjecture?}`
