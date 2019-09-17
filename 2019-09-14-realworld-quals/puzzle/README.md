# Puzzle (re, 126p)

In the challenge we get to play a simple sliding puzzle game.
It's a browser game so we can get the [game script](main.dart.js).
It seems to be transpiled dart code to JS, which makes lots of code to look at.

However once you look closely, most of the code doesn't really do anything useful, some standard functions, some objects creations, and very little actual functional code.
From the code, and from playin the game we can notice that there are a bunch of REST endpoints:


- `/api/new_game` we GET a session cookie and a game board to solve
- `/api/validate` we POST set of moves we performed and the server checks if this is a valid solution to puzzle assigned to our session ID
- `api/submit` we POST our username for the Hall-of-Fame.

First two endpoints are not particularly interesting, but the last one is.
Once we win the game, we can submit our name, and surprisingly the server sends something back:

```
{"err":null,"msg":"Congratulations!","success":true,"data":"I3LZuNvvtmms1SAsE+KP8/aTUZrl7ijPFrByKFRppelWHoT6ez/U0FXywLrn5n+S/4MGtSHb/19CGXc5S9lB7WdIy63qFQIIsFx8k2vJmzpYHaoL5pYHwLxGcSxAH4OD2SJyN6E4TsZkbqrZv/4mHCb7phDqgg5o+WfTyP/3KNRhgu1pbJntnDz5Ya19lHU5LdIW5t34SSH54nbLiowbGJ9SFDrnZNEkzOHDfQBKZf3yxCm3/ogxth8Xfjq/D0VTs1BN+2IgBZS7J59fjaI3QbbFU1AC0ZG4Xu1ULem7ogvTI1ppAkddiYPDuFW0cEehZnNIKOj1S5AEKjpXE1vHiIUnV54+OcmqE1eFUdKYBQIwMjYdK+z8wCCXOVV2e/iMFiZeRQia/Xpbm+GfYH7YUD/Ztnpb51vsdU0BVN6SUjDePVeUamKsNhOU1qy8uyE+JsTPohUNKsdeY8Nw0o/jctcOqk64/v5ppY6XhoU3tev+f+x1lRE0EbRpYkSRX+qgx5EyiTiLAtWUuQrjzbZOoupMH81WSQ3OD5Td9IV5rcC1QthJ4ZfKbWIf4oUm565LEYC+grIu0miy+BNX78BTuz46sG/viN4PoBhC7jh7OCOdRUxFZamarEgipiXcqjvTcSpM731jYJKBL3cwHEf8Wrm47ifMkQHmGRvz1yLvPmV6Ubg87n8sGoMO0h5uV/uWLLrIuzKy2lOAayapFiVyLOxqfV24d/xx+6KtzQOy7PXPKn8haXzNCxP5ZEVTzkCwlpldfXydcX0dShmp31ZaJYKeLJSWDMWN3pybu0Ts0vn7rUenjuLWQrTj+s/as0wUS6FumLERmsWdla0DVOQUPlBiMdFlrrEMdJzFNDz+p6Z0b7+BF5y633PFrs81yjJauuIDN0FMFjVsyffZFkFHf8EvWJApT03N29BaM6rm0d8waFe2Q0QYEwSQ+PLmf7BwuTCdpYWoI4T5KZ5Yq5ijJdpzD3tpJ4ukEGigmC0a9rCdfSl0uQYt4784EHex4bsuKqBth3P/KiDRVgwB66arnZtJ3LGr9ZYsZl/auJm7xsYH1zN6blTqV+ZnS1fTH4VQvPH90ITT7HBNkIXSdwYUlL5LaZyHc5wpGTPy5fYx1BP1acsB387zpK1VjTNNllEMa2K/qjybrJ2L/eeLR3FdI3dIkDy01BQp8oUnZJFnknICWr2ce7soJM1B6zS8Ov9cqjsHPrJmLO88B8XoSn1RZ92c66YT670oiJeFn/Yx52/9UUJtCAIfSUWVeE9ScCoCGQ+4f0FjlYHafT4JUYfADrZ8ziRxAMCTQ+NLvidRAnkI3EBQN8fh8VQBuI+2SrHgIkDf9ogf5d3PDi8/gD0fONyqETFFWgtteSdegwBBynKiN42mbnjAXZdObgp30ibo//22onf4yfiCjKozhQGFfuQ+zRojKWkfp3QMyNduMIRQ/IAx5wtzMEqobyHEH8ppSpkEUFWbVOS8PmB9Jws4NXgGlcIIZ0aw3Eg03o6Sg6JaDPZJ5exJwvhEDkr7AlYWzm6wXq4QcYVg1dJEI7nrqzLVcq4VYhuxMYIcaMqp/aq312hPKxalf+58/8M+cusLZRQu6ZdGfPzQMkQf7jwZ23znPWKUl+MW2Jjxt7Sb8a2wiPGcm7jxu52l8ayHiPGltYzxp76/8Yu3kvGngqzxq46/8bSTlvGzi47xraa58Z2Fj/GfrYLxuo+U8ZiVsPG7h4zxqbiV8aOcrPGtsJjxpYy38bGSq/GqjbfxuL+J8Z2frPGjtZHxiqSS8aa4hvGRsozxroWw8ZSYlfGhkrbxrYmn8bCgqw=="}
```

This is a bit unexpected because it seems the game doesn't really do much with it.
It's not a new board, nothing pops up.
So we dig deeper, what exactly happens with this weird payload:

```js
    E.JZ.prototype = {
        $1: function (a) {
            var u, t, s
            H.a(a, "$ijM")
            u = H.J(a.a)
            t = this.a
            s = t.c
            if (u) E.XA(s, !1, "Bruce Lee", "Enter Your Name", a.b).bR(new E.JY(t, a), null)
            else E.nU(s, a.b, null)
        },
        $S: 289
    }
    E.JY.prototype = {
        $1: function (a) {
            var u, t, s, r, q, p, o, n, m, l, k, j, i, h, g
            H.P(a)
            if (a != null && a.length !== 0) {
                u = this.b.c
                if (u.length !== 0) {
                    t = C.fX.bJ(u)
                    u = t.length
                    if (0 >= u) return H.o(t, 0)
                    s = t[0]
                    r = H.h([], [[P.p, P.r]])
                    for (q = H.cD(C.M, t, "a8", 0), p = 0; p < s; ++p) {
                        o = p * s
                        n = o + 1
                        o = o + s + 1
                        P.dq(n, o, u)
                        C.a.h(r, H.cT(t, n, o, q).b8(0))
                    }
                    o = s * s + 1
                    P.dq(o, u, u)
                    m = H.cT(t, o, u, q).b8(0)
                    q = m.length
                    u = new G.GU(m, 0, q)
                    o = q + 0
                    if (o > q) H.a5(P.l_(o, null))
                    l = new B.OC(u.gZ(u)).TA()
                    k = H.h([], [P.r])
                    for (u = a.length, p = 0; p < u; ++p) C.a.h(k, C.f.a4(a, p))
                    for (u = l.length, q = r.length, o = k.length, j = 0, p = 0; p < s; ++p) {
                        for (i = 0, h = 0; h < s; ++h) {
                            n = o > h ? k[h] : 0
                            if (p >= q) return H.o(r, p)
                            g = r[p]
                            if (h >= g.length) return H.o(g, h)
                            g = g[h]
                            if (typeof g !== "number") return H.d(g)
                            i += n * g
                        }
                        if (p >= u) return H.o(l, p)
                        if (i === l[p]) ++j
                    }
                    u = this.a
                    if (j === s) E.nU(u.c, "Congratulations again on you-know-what!", "RealWorld Slide Puzzle Solved")
                    else A.AK(a).bR(new E.JU(u), null).fX(new E.JV(u))
                } else {
                    u = this.a
                    A.AK(a).bR(new E.JW(u), null).fX(new E.JX(u))
                }
            }
        },
        $S: 59
    }
```

From `if (u) E.XA(s, !1, "Bruce Lee", "Enter Your Name", a.b).bR(new E.JY(t, a), null)` we jump to `E.JY(t, a)` which is just below.
Fortunately IntelliJ handles jumping around this code just fine :)
This part `if (j === s) E.nU(u.c, "Congratulations again on you-know-what!", "RealWorld Slide Puzzle Solved")` looks promising.
Maybe if we can reach this condition we can get the flag.

We proceed with reversing this function.
Once you get rid of all type and error checks, and follow some of the functions is becomes pretty clear:

First by `t = C.fX.bJ(u)` we decode base64.

Then with `s = t[0]` we read size and number of chunks, it was always `#` so 35.

Next:

```js
for (q = H.cD(C.M, t, "a8", 0), p = 0; p < s; ++p) {
    o = p * s
    n = o + 1
    o = o + s + 1
    P.dq(n, o, u)
    C.a.h(r, H.cT(t, n, o, q).b8(0))
}
```

Prefix of the data (minus the first character) is split into `s` chunks each with `s` bytes, so in our case 35 chunks of 35 bytes each.

Then happens `l = new B.OC(u.gZ(u)).TA()` which does some magic on the last 140 bytes of the data, and gets back array of 35 integers.

After that there is `for (u = a.length, p = 0; p < u; ++p) C.a.h(k, C.f.a4(a, p))` which basically fills array `k` with characters of the `username` we provided for the scoreboard.

The last part is:
```js
for (u = l.length, q = r.length, o = k.length, j = 0, p = 0; p < s; ++p) {
    for (i = 0, h = 0; h < s; ++h) {
        n = o > h ? k[h] : 0
        if (p >= q) return H.o(r, p)
        g = r[p]
        if (h >= g.length) return H.o(g, h)
        g = g[h]
        if (typeof g !== "number") return H.d(g)
        i += n * g
    }
    if (p >= u) return H.o(l, p)
    if (i === l[p]) ++j
}
```

If we clear this up a bit we end up with:

```js
j = 0
for (p = 0; p < s; ++p) {
    i = 0
    for (h = 0; h < s; ++h) {
        i += r[p][h]*k[h]
    }
    if (i === l[p]) ++j
```

Let's assume for a moment `k` has size 35, after all we could just put `0` a the end.
What really happens here is simply that Matrix 35x35 denoted by coefficients `r` is multiplied by vector `k` and the result vector is compared to array `l`.
And we've seen at the beginning that `if (j === s) E.nU(u.c, "Congratulations again on you-know-what!", "RealWorld Slide Puzzle Solved")` so if all 35 elements match we have the flag.

We suspected that the flag is the name we send to the server, and for the valid flag this matrix equation will work.
We had problems with reversing the function for creating array `l`, but we ended up simply dumping the values from the debugger, after the game calculated them for us.

We end up with code:

```python
def chunk(data):
    size = ord(data[0]) # 35
    data = data[1:]
    return [map(ord,data[i*size:(i+1)*size]) for i in range(size)]


def L_array():
    return [490779, 449544, 378616, 505701, 442824, 417100, 425919, 310738, 422060, 439231, 476374, 471758, 448953, 381263, 392002, 500692,
            361840, 504268, 433685, 407340, 449560, 414519, 464043, 435063, 495561, 382956, 408913, 305426, 421382, 334988, 450928, 345621,
            398518, 447079, 460843]


def solve_checksum(data):
    s = ord(data[0])
    r = chunk(data)
    l = L_array()
    m = Matrix(r)
    solution = m\vector(l)
    return "".join(chr(int(c)) for c in solution)


def main():
    data = "I3LZuNvvtmms1SAsE+KP8/aTUZrl7ijPFrByKFRppelWHoT6ez/U0FXywLrn5n+S/4MGtSHb/19CGXc5S9lB7WdIy63qFQIIsFx8k2vJmzpYHaoL5pYHwLxGcSxAH4OD2SJyN6E4TsZkbqrZv/4mHCb7phDqgg5o+WfTyP/3KNRhgu1pbJntnDz5Ya19lHU5LdIW5t34SSH54nbLiowbGJ9SFDrnZNEkzOHDfQBKZf3yxCm3/ogxth8Xfjq/D0VTs1BN+2IgBZS7J59fjaI3QbbFU1AC0ZG4Xu1ULem7ogvTI1ppAkddiYPDuFW0cEehZnNIKOj1S5AEKjpXE1vHiIUnV54+OcmqE1eFUdKYBQIwMjYdK+z8wCCXOVV2e/iMFiZeRQia/Xpbm+GfYH7YUD/Ztnpb51vsdU0BVN6SUjDePVeUamKsNhOU1qy8uyE+JsTPohUNKsdeY8Nw0o/jctcOqk64/v5ppY6XhoU3tev+f+x1lRE0EbRpYkSRX+qgx5EyiTiLAtWUuQrjzbZOoupMH81WSQ3OD5Td9IV5rcC1QthJ4ZfKbWIf4oUm565LEYC+grIu0miy+BNX78BTuz46sG/viN4PoBhC7jh7OCOdRUxFZamarEgipiXcqjvTcSpM731jYJKBL3cwHEf8Wrm47ifMkQHmGRvz1yLvPmV6Ubg87n8sGoMO0h5uV/uWLLrIuzKy2lOAayapFiVyLOxqfV24d/xx+6KtzQOy7PXPKn8haXzNCxP5ZEVTzkCwlpldfXydcX0dShmp31ZaJYKeLJSWDMWN3pybu0Ts0vn7rUenjuLWQrTj+s/as0wUS6FumLERmsWdla0DVOQUPlBiMdFlrrEMdJzFNDz+p6Z0b7+BF5y633PFrs81yjJauuIDN0FMFjVsyffZFkFHf8EvWJApT03N29BaM6rm0d8waFe2Q0QYEwSQ+PLmf7BwuTCdpYWoI4T5KZ5Yq5ijJdpzD3tpJ4ukEGigmC0a9rCdfSl0uQYt4784EHex4bsuKqBth3P/KiDRVgwB66arnZtJ3LGr9ZYsZl/auJm7xsYH1zN6blTqV+ZnS1fTH4VQvPH90ITT7HBNkIXSdwYUlL5LaZyHc5wpGTPy5fYx1BP1acsB387zpK1VjTNNllEMa2K/qjybrJ2L/eeLR3FdI3dIkDy01BQp8oUnZJFnknICWr2ce7soJM1B6zS8Ov9cqjsHPrJmLO88B8XoSn1RZ92c66YT670oiJeFn/Yx52/9UUJtCAIfSUWVeE9ScCoCGQ+4f0FjlYHafT4JUYfADrZ8ziRxAMCTQ+NLvidRAnkI3EBQN8fh8VQBuI+2SrHgIkDf9ogf5d3PDi8/gD0fONyqETFFWgtteSdegwBBynKiN42mbnjAXZdObgp30ibo//22onf4yfiCjKozhQGFfuQ+zRojKWkfp3QMyNduMIRQ/IAx5wtzMEqobyHEH8ppSpkEUFWbVOS8PmB9Jws4NXgGlcIIZ0aw3Eg03o6Sg6JaDPZJ5exJwvhEDkr7AlYWzm6wXq4QcYVg1dJEI7nrqzLVcq4VYhuxMYIcaMqp/aq312hPKxalf+58/8M+cusLZRQu6ZdGfPzQMkQf7jwZ23znPWKUl+MW2Jjxt7Sb8a2wiPGcm7jxu52l8ayHiPGltYzxp76/8Yu3kvGngqzxq46/8bSTlvGzi47xraa58Z2Fj/GfrYLxuo+U8ZiVsPG7h4zxqbiV8aOcrPGtsJjxpYy38bGSq/GqjbfxuL+J8Z2frPGjtZHxiqSS8aa4hvGRsozxroWw8ZSYlfGhkrbxrYmn8bCgqw=="
    data = data.decode("base64")
    print(solve_checksum(data))


main()
```

And once we run this we get back: `rwctf{wr1te-0nce~DEBUG+ev3ry|wh3re}`
