# primitive, crypto


This was quite an interesting challenge. We were given a Python code of a server running on their host.
It generated and sent a random permutation of 256 bytes and treated it as substitution cipher. Our task was to supply
a sequence of operations, that when applied to any byte `c`, would give `perm[c]`. The allowed operations
were:
- `ADD n`, `0 <= n < 256`,
- `ROL n`, `0 <= n < 8`,
- `XOR n`, `0 <= n < 256`.

All of these were modulo 256.

For example, let's say the the permutation was `(1, 2, 0, 3)` (for simplicity of the example, we use 2-bit numbers).
Then one of the solutions would be: `ADD 3, ROL 1, XOR 2`, since number 0 after these operations would give 1,
1 maps to 2, 2 to 0, and 3 stays 3.

It is hard to instantly think of a general algorithm to generate the needed sequence, so we had to split the
task into simpler ones. The first thing we can do is rewriting the permutation as product of transpositions.
For the example given above, this would be `swap(0, 1); swap(1, 2)`:
```
0 1 2 3
 x
1 0 2 3
   x
1 2 0 3
```

Now we need to just write a function that generates a sequence of operations that swaps two arbitrary numbers `x` and `y`,
leaving the rest of the permutation as it was. This is still a pretty hard problem, so we again decomposed it
into a set of simpler ones: we can first find operations `P(x, y)` that will map `x` to `0` and `y` to `1`
with the other numbers allowed to move freely, then swap `0` and `1` (with other numbers in constant positions),
then apply the first set of operations in inverse (that is, `P^-1(x, y)`).

Thus we have reduced original problem to finding `swap(0, 1)` and `P(x, y)` for any `x` and `y`.

We implemented a C++ code that brute forces possible solutions to these. The minimal `swap(0, 1)` implementation is
`ADD 254, ROL 7, ADD 1, ROL 1`.

While trying to search for `P(x, y)`, we noticed there are too many possible solution candidates for unoptimized
brute force to be feasible. We first ran it on smaller `N` (number of bits in the numbers), and then noticed that
it is enough to consider sets of operations of the following form: `ADD a, ROL b, XOR c, ADD d`. This massively
reduced the search space. After this and a few smaller optimizations, we managed to fit all possible candidates in memory
and calculated all `P(x, y)` (using `doit.cpp`) and saved them as Python array (in file `tab.py`).

The final script, combining the above insights, is available in `doit.py`.
