# Programming02, PPC

In this challenge there is a hypothetical pinpad that looks like this:

```
123
456
789
*0#
```

We have to count the number of unique passwords that:
 - end with `8`, `*` or `#`
 - every character is reachable from the previous one using a chess knight moves (for example, after `1` there can only be `6` or `8`)

We are also supposed to give the result modulo `10**39`, and the maximum password length may be `10**16` or so

The obvious solution is recursive bruteforce:

```
f(_, 1) = 1
f(1, n) = f(6, n-1) + f(8, n-1)
f(2, n) = f(7, n-1) + f(9, n-1)
f(3, n) = f(4, n-1) + f(8, n-1)
f(4, n) = f(3, n-1) + f(9, n-1) + f(0, n-1)
...
```

But that's waaay to slow, even for n <= `10**2` not to mention `10**16`.

We could improve it with memoisation up to maybe `10**8`, but that's still way to slow.

To really solve this challenge we have to reduce the complexity to something sublinear.
Fortunately, we can use the very old programming trick to do this.

First, let's simplify the challenge (that's not technically required but makes the code nicer).
Most of the characters on the pinpad are isomorphic:

```
ABA
CDC
CDC
ABA
```

Characters with the same letter "behave" in the same way. List of possible transitions is:

```
A -> [C, D]
B -> [C, C]
C -> [A, C, B]
D -> [A, A]
```

We can represent this as a transition matrix (in `Zn(10**39)`, because we're supposed to give result modulo `10**39`):

```
R = Integers(10**39)
mat = Matrix(R, [
    [0, 0, 1, 2],
    [0, 0, 1, 0],
    [1, 2, 1, 0],
    [1, 0, 0, 0],
])
```

And the starting vector is (the list of possible endings for 1 character passwords):

```
start = vector(R, [2, 0, 0, 1])
```

To get list of possible endings for 2 character password, we can multiply it by our matrix:

```
pass2char = mat * start
print "number of possible passwords with length 2: ", sum(pass2char)

pass3char = mat * pass2char
print "number of possible passwords with length 3: ", sum(pass3char)
```

Now, this is still linear. But matrix exponentation isn't (remember fastpow), so we can just:

```
passNchar = sum((mat ^ (n-1)) * start
```

The final solution in sage is (minus server commmunication code):

```python
R = Integers(10**39)
start = vector(R, [2, 0, 0, 1])
mat = Matrix(R, [
    [0, 0, 1, 2],
    [0, 0, 1, 0],
    [1, 2, 1, 0],
    [1, 0, 0, 0],
])
for i in range(1, 20):
    print int(sum((mat ^ i) * start))
```
