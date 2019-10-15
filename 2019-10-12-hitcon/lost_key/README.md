# Lost key (crypto, 334p, 10 solved)

Unfortunately we were unable to finish this task, but we managed to get the first part - recovery of `N`, and just for future reference we're include this part in a writeup.

## Overview

In the task we get [source code](chall.py).
We can connect to a service and we get back RSA encrypted flag.
We can also send our own payload and get it encrypted as well.
Our payload has restricted length and always includes prefix `X: `.

## General approach

The general method for recovering `N` in such case, is to obtain some multiples of `N` and calcuate their GCD.
If we had total control over the payload we could simply ask for encryption of `A` and of `A^2` and calculate `(A^e mod N)^2 - ((A^2)^e mod N)`.
Such difference, by definition, has to be a multiple of `N`, because you can shift the exponentiation order and move modulo:

```
(A^e mod N)^2 mod N = (A^e)^2 mod N = (A^e mod N)^2 mod N = (A^e)^2 mod N = (A^2)^e mod N`
```

So if we apply `mod N` to `(A^e mod N)^2` we should get the same value as in `((A^2)^e mod N)` therefore it has to be `((A^2)^e mod N) + k*N` and if we subtract `((A^2)^e mod N)` we'll get plain `k*N`.

However, we don't control the payload so much, it has the prefix!

## Modulus recovery

The idea for modulus recovery is just as above - we want to get from the server a pair of different ciphertexts which `mod N` would have the same value.
Subtracting them will yield `k*N`.

We are going to leverage homomorphic property of textbook RSA:

```
A^e mod N * B^e mod N = (A*B)^e mod N
```

Let's assume we have 4 different values such that: `A*B = C*D` and each of those values is a valid plaintext with the appropriate prefix.

If we encrypt those values separately with textbook RSA and combine them the property will still hold, so:

```
(A^e mod N * B^e mod N) mod N = (A*B)^e mod N
(C^e mod N * D^e mod N) mod N = (C*D)^e mod N

and since

A*B = C*D

then

(A*B)^e mod N == (C*D)^e mod N
```

However, the values `(A^e mod N) * (B^e mod N)` and `(C^e mod N) * (D^e mod N)` without applying the `mod N` operation on the product will not be the same!

This is exactly the property we're looking for.
So the goal is to find values `A, B, C, D` we could use.

The idea we came up with is to create each one of them as a combination of 2 other values in a way that:

```
A = x*y
B = z*v
C = x*v
D = y*z
```

This way obviously `A*B = x*y*z*v = C*D`.

Now we need to make sure each of the values matches the prefix.
In order to do that we figured we can factor the prefix into primes, and then create `x,y,z,v` as combination of some factors, so that each of `A, B, C, D` will contain full set of factors.

Of course values `A, B, C, D` have o be different, so we need to include also some random padding at the end of each of them:


```python
    prefix = bytes_to_long("X: ")
    factors, _ = factor(prefix)
    random.shuffle(factors)
    base1 = multiply(factors[:len(factors) / 2])
    base2 = multiply(factors[len(factors) / 2:])
    assert base1 * base2 == prefix
```

Now with those base values we can do:

```python
    shift = 5
    x = base1 * 256 ** shift + 0
    y = base2 * 256 ** shift + 0
    z = base1 * 256 ** shift + 1
    v = base2 * 256 ** shift + 1

    A = x * y
    B = z * v
    C = x * v
    D = y * z
    assert (A * B == C * D == x * y * z * v)
```

And we have the plaintexts we wanted.
Now we just need to encrypt them and calculate `(CTA * CTB) - (CTD * CTC)` to get a multiple of `N`.

After that the only thing left is to calculate gcd over those values to recover `N`: `28152737628466294873353447700677616804377761540447615032304834412268931104665382061141878570495440888771518997616518312198719994551237036466480942443879131169765243306374805214525362072592889691405243268672638788064054189918713974963485194898322382615752287071631796323864338560758158133372985410715951157`

This value can easily be factored into:

```
p = 531268630871904928125236420930762796930566248599562838123179520115291463168597060453850582450268863522872788705521479922595212649079603574353380342938159
q = 52991530070696473563320564293242344753975698734819856541454993888990555556689500359127445576561403828332510518908254263289997022658687697289264351266523
```

Unfortunately we were unable to recover `e` and finish the challenge.
Solver for the described part is [here](modulus.py)
