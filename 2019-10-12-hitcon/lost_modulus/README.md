# Lost modulus (crypto, 200p, 64 solved)

In the task we get [source code](prob.py) and its [output](output).
The code is simply RSA encryption of the flag.

## Analysis

The key observation from the code is:

```python
def __str__(self):
    return "Key([e = {0}, n = {1}, x = {2}, y = {3}])".format(self.e, self.d, self.iqmp, self.ipmq)
```

Second output parameter is `self.d` even though it's labelled as `n = {1}`.
This means that we know `e, d, iqmp and ipmq`, but we don't know `n`.

As name of the challenge suggests, they goal is to recover `n` to complete the private key and decrypt the flag.

## Solution equation

In order to do that we need to do a bit of math.
There is not much to go with, since the only values related to `n` we have are `iqmp` and `ipmq`.

Let's use their definition:

```
ipmq = modinv(p,q)
ipmq*p == 1 mod q
ipmq*p = 1 + k*q [some integer k with bound k<q]
k*q = ipmq*p - 1 [some integer k with bound k<q]
```

Same for `iqmp`:

```
iqmp = modinv(q,p)
iqmp*q == 1 mod p
iqmp*q = 1 + m*p [some integer m with bound m<p]
m*p = iqmp*q - 1 [some integer m with bound m<p]
```

Let's now multiply those 2 equations:

```
(ipmq*p) * (iqmp*q) = (1+k*q) * (1+m*p)
ipmq*iqmp*p*q = k*m*p*q + k*q + m*p + 1
ipmq*iqmp*N = k*m*N + k*q + m*p + 1
```

Let's move `N` to one side:

```
N*(ipmq*iqmp - k*m) = k*q + m*p + 1
```

On the left side of the equation we have `N*x` and since those are all integer equations, it means `x` has to be integer as well.
This means that the right side of the equations has to also be a multiple of N.

Now the **key** observation in this task:

Let's remember the bounds for `k` and `m` -> `k<q` and `m<p`.

On the right side we have `k*q + m*p + 1`.
What is the upper bound? It has to be smaller than `q*q + p*p +1`.
We can assume, from the task setup, that `p` and `q` are of similar bitlength, and thus `q*q` and `p*p` can't be much bigger than `N`, and therefore the whole right side of the equation can't be much bigger than `2*N` even in the most pessimistic case (with `k=q` and `m=p`), and since it's all integers it can be either `N` or `2*N` and nothing more.
It's very unlikely that we hit the upper bound, so we can safely assume that in reality it's equal to `N`.

So we have now:

```
k*q + m*p + 1 = N
```

Now let's substitute back `k*q = ipmq*p - 1` and `m*p = iqmp*q - 1`:

```
(ipmq*p - 1) + (iqmp*q - 1) + 1 = N
ipmq*p + iqmp*q - 1 = N
```

Let's now look into another relation:

```
N = p*q
phi(N) = (p-1)*(q-1)
```

From this we know that:

```
phi(N) = N - p - q + 1
N = phi(N)+p+q-1
```

Let's modify a bit our previous result:

```
ipmq*p + iqmp*q - 1 = N
ipmq*(p-1+1) + iqmp*(q+1-1) - 1 = N
ipmq*(p-1) + ipmq + iqmp*(q-1) + iqmp - 1 = N
```

And combine this with relation between `N` and `phi`:

```
ipmq*(p-1) + ipmq + iqmp*(q-1) + iqmp - 1 = phi(N) + p + q - 1
```

For simplicity let's introduce:

```
p-1 = X
q-1 = Y
phi(N) = phi
```

And thus:

```
phi = X*Y
X = phi/Y
```

And now:

```
phi = ipmq*X + ipmq + iqmp*Y + iqmp -1 -(X+1+Y)
phi = ipmq*(phi/Y) + ipmq + iqmp*Y + iqmp - 1 -(phi/Y + 1 + Y)
```
Let's now multiply this by `Y`:

```
phi*Y = ipmq*phi + ipmq*Y + iqmp*Y^2 + iqmp*Y - Y -(phi + Y + Y^2)
phi*Y = ipmq*phi + ipmq*Y + iqmp*Y^2 + iqmp*Y - Y - phi - Y - Y^2
```

Move this to one side and combine:

```
Y^2*(iqmp-1) + Y(ipmq + iqmp - phi - 2) + ipmq*phi - phi = 0
```

Now we have simply an equation `a*x^2 + bx + c == 0` and we can directly solve it, assuming we know the value of `phi`.

## Phi(n) recovery

Fortunately we can easily calculate `phi` one using the fact that:

```
e*d mod phi == 1
e*d == 1+k*phi
k*phi == e*d-1
```

Now although the value of `k` may be big, we can approximate it using some value which should be of similar bitlen to `phi` we're looking for.
Once such value would of course be `N`, but we don't know that.
Other such value is for example `d`, since it was calculated as `inverse(self.e, (self.p-1)*(self.q-1))` so it has to be smaller than `phi`.

We iterate over possible phi using:

```python
def find_phi(e, d):
    kfi = e * d - 1
    k = kfi / (int(d * 3))
    print('start k', k)
    while True:
        fi = kfi / k
        try:
            d0 = gmpy2.invert(e, fi)
            if d == d0:
                yield fi
        except:
            pass
        finally:
            k += 1
```

Keep in mind there can be many values `phi` where `d == modinv(e,phi)`, so we need to test all of them, but with our start approximation for `k` we should hit the right one quite fast.

## Solving quadratic equation

Now that we can provide possible `phi` values, we can get back to our quadratic equation and solve it:

```python
def solve_for_phi(ipmq, iqmp, possible_phi):
    a = iqmp - 1
    b = ipmq + iqmp - 2 - possible_phi
    c = ipmq * possible_phi - possible_phi
    delta = b ** 2 - 4 * a * c
    if delta > 0:
        r, correct = gmpy2.iroot(delta, 2)
        if correct:
            x1 = (-b - r) / (2 * a)
            x2 = (-b + r) / (2 * a)
            if gmpy2.is_prime(x1 + 1):
                q = x1 + 1
                p = possible_phi / x1 + 1
                return p, q
            elif gmpy2.is_prime(x2 + 1):
                q = x2 + 1
                p = possible_phi / x2 + 1
                return p, q
```

Now if we plug this all together:

```python
def main():
    e = 1048583
    d = 20899585599499852848600179189763086698516108548228367107221738096450499101070075492197700491683249172909869748620431162381087017866603003080844372390109407618883775889949113518883655204495367156356586733638609604914325927159037673858380872827051492954190012228501796895529660404878822550757780926433386946425164501187561418082866346427628551763297010068329425460680225523270632454412376673863754258135691783420342075219153761633410012733450586771838248239221434791288928709490210661095249658730871114233033907339401132548352479119599592161475582267434069666373923164546185334225821332964035123667137917080001159691927
    ipmq = 22886390627173202444468626406642274959028635116543626995297684671305848436910064602418012808595951325519844918478912090039470530649857775854959462500919029371215000179065185673136642143061689849338228110909931445119687113803523924040922470616407096745128917352037282612768345609735657018628096338779732460743
    iqmp = 138356012157150927033117814862941924437637775040379746970778376921933744927520585574595823734209547857047013402623714044512594300691782086053475259157899010363944831564630625623351267412232071416191142966170634950729938561841853176635423819365023039470901382901261884795304947251115006930995163847675576699331
    ct = 0x32074de818f2feeb788e36d7d3ee09f0000381584a72b2fba0dcc9a2ebe5fd79cf2d6fd40c4dbfea27d3489704f2c1a30b17a783baa67229d02043c5bc9bdb995ae984d80a96bd79370ea2c356f39f85a12d16983598c1fb772f9183441fea5dfeb5b26455df75de18ce70a6a9e9dbc0a4ca434ba94cf4d1e5347395cf7aafa756c8a5bd6fd166bc30245a4bded28f5baac38d024042a166369f7515e8b0c479a1965b5988b350064648738f6585c0a0d1463bd536d11a105bb926b44236593b5c6c71ef5b132cd9c211e8ad9131aa53ffde88f5b0df18e7c45bcdb6244edcaa8d386196d25297c259fca3be37f0f2015f40cb5423a918c51383390dfd5a8703
    for potential_phi in find_phi(e, d):
        res = solve_for_phi(ipmq, iqmp, potential_phi)
        if res:
            p, q = res
            n = p * q
            print(long_to_bytes(pow(ct, d, n)))
            break
```

We get the flag: `hitcon{1t_is_50_easy_t0_find_th3_modulus_back@@!!@!@!@@!}`

Complete [solver here](solver.py)
