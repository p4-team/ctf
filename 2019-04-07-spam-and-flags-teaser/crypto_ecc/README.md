# Secure Password DB (crypto, 357p, 7 solved)

In the challenge we get access to a webpage where you can check if your password was leaked.
We can access the [source code](index.php) of the page.

The idea behind this page is quite simple:

- We provide a password
- This password is transformed into a point `Q` on an Elliptic Curve `E` on the client side
- This point is multiplied by a random client secret `enc_key` on the client side, so that the server never sees the cleartext password point, so we have now `R=enc_key*Q`
- This point `P` gets encrypted using server-side secret `k` by calculating new point `S=k*R`
- Using the first letter of the password we provided, the server fetches a bucket of all passwords starting with this letter, and returns encrypted version of those passwords
- Now we remove the `enc_key` part from point `S` by `decrypting` this point using secret `enc_key`, so we simply multiply point `S` by `modinv(enc_key, E.order())`
- Finally we can compare the encrypted passwords we got from the server, with the point we have, if any of them matches it means our password was in the DB

The vulnerability here comes from the fact that the server doesn't actually check if the point we provide is a valid point on the curve `E`.
We send some point `R` and server simply calculates `k*R` for us.
And if we look at how calculations are made, the coefficient `B` is not used in scalar multiplication.

This means we can do attack described in https://www.iacr.org/archive/crypto2000/18800131/18800131.pdf

We can create a new Elliptic Curve `E'` using a different value for `B`, but such that order of this curve will have a small divisor `r`.
We can then ask the server to encrypt a point of this subgroup.
In such case we can calculate a Discrete Logarithm in a small subgroup and recover `k mod r`, where `k` is the secret key.

```python
P = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
A = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC

quotients, mods = [], []

for B in range(7): # for random B
    print('B',B)
    try:
        E = EllipticCurve(GF(P), [A, int(B)]) # new curve
        order = E.order()
        factors = prime_factors(order)
        print('Factors', factors)
        for prime in factors:
            if prime > 10 and prime < 2**20: # skip large subgroups
                try:
                    print("Solving for prime", prime)
                    G = E.gen(0) * int(order / prime) # point of the subgroup
                    G1x, G1y = encryptPoint((G[0], G[1]))
                    G1 = E(G1x, G1y)
                    solution = G.discrete_log(G1)
                    print("K mod " + str(prime) + " = " + str(solution))
                    mods.append(prime)
                    quotients.append(solution)
                    print('Known relations', quotients, mods)
                except Exception as e:
                    pass # wrong point
    except:
        pass # wrong curve
```

We can then repeat this process for different values of `r` and different curves `E'` and collect a lot of relations `ci = k mod ri`.
Once we have enough of them we can use Chinese Reminder Theorem to recover the value of `k` (we need enough pairs `(ci, ri)` so that `r1*r2*...*rn >= k`)

```python
CRT_list(quotients, mods)
```

By running this we recovered the secret `86962807399445295025648724453367621898` which is actually a printable string `Almost there :)\n`.

Now the last part is just grabbing encrypted passwords from the server and decrypting them.
Since we know the curve and the secret, we can just calculate `modinv(secret, E.order())` and multiply encrypted passwords by this scalar.
Then we just take the `X` coordinate of the result point and print as string:


```python
inv = inverse_mod(secret, E.order())
pws = grab('S')
for x,y in pws:
    Q = E(x,y)
    X = Q*inv
    print(long_to_bytes(X[0]))
```

And one of the entries is the flag: `SaF{I_use_a_small_group_of_pws}`

Complete automatic solver [here](ecc.sage)
