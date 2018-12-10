# Curve12833227 (crypto, 150+37p, 12 solved)

In the challenge we get [code](vuln.py) and the [result](flag.enc).

What the code does is encrypt the flag using AES and the AES key is encrypted via a custom elliptic curve using generator point `(4,10)`.
We don't get the curve equation, only the addition and multiplication functions, but we can easily derive the curve parameters from that.

It's very simple to do from the point doubling part:

```python
if u == w: 
    m = (3*u*w + 4*u + 1) * i(v+x)
```

Of course since `u==w` then `3*u*w + 4*u + 1 = 3u^2 + 4u + 1`.
Doubling a point on an elliptic curve requires calculating a tangent to the curve in this point, which means calculating a first derivative.

Since `3x^2 + 4x + 1` is the derivative we can easily integrate it to get `x^3 + 2x^2 + x +C` as the curve equation.

So we know that `y^2 = x^3 + 2x^2 + x + C`.

We also know that point `(4,10)` is on the curve, so we can apply this point to the curve to calculate `C = 100 - (64 + 2*16 + 4) = 0`.

So finally the curve is `y^2 = x^3 + 2x^2 + x = x(x^2+2x+1) = x(x+1)^2`

The issue now is that this curve has a singularity in `(-1,0)`.
We follow the approach similar to: https://crypto.stackexchange.com/questions/61302/how-to-solve-this-ecdlp

And we get the solution code:

```python
p = 2^128 - 33227
P.<x> = GF(p)[]
f = x^3 + 2*x^2 + x
P = (4, 10)
Q = (104708042197107879674895393611622483404, 276453155315387771858614408885950682409)

f_ = f.subs(x=x-1)
print f_.factor() # 340282366920938463463374607431768178228

P_ = (P[0] +1, P[1])
Q_ = (Q[0] +1, Q[1])

t = GF(p)(340282366920938463463374607431768178228).square_root()
u = (P_[1] + t*P_[0])/(P_[1] - t*P_[0]) % p
v = (Q_[1] + t*Q_[0])/(Q_[1] - t*Q_[0]) % p

print v.log(u)
```

Which after a while gives us the discrete logarithm of `35996229751200732572713356533972460509`.

With this we can decrypt the flag:

```python
k = 35996229751200732572713356533972460509
aes = AES.new(long_to_bytes(k).ljust(16, '\0'), AES.MODE_CBC, '\0'*16)
flag = "202bb05919b6f021d22a8baa7979ef6810761eb4c653b0fc5eebf2bc6ac6ecb052f887eedd075174abd884f84547df2d".decode("hex")
print(len(flag))
plaintext = aes.decrypt(flag)
print(plaintext)
```

And we get: `hxp{51n9uL4r1ti3s_r3duC3_tH3_G3nUs}`
