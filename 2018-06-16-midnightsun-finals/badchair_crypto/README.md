# Badchair (crypto)

In this challenge we get data secured via Shamir Secret Sharing scheme:

```
{"threshold": 5, "split": ["jUEumBCZY6GRlXbB/uobM53gis/RldnMAfBAnkg=", "e3WhwYy6YUQGedMXkGnxJO6v0ov4cgteapL17wI="], "shares": 9}
{"threshold": 5, "split": ["mrygQzFoasgDY23te4MGqTFXjpS/pMalQiN9Sks=", "XjpXSuBzyfRAbKj7hODzcf0cv0NZsXQDEQiIdtA="], "shares": 9}
{"threshold": 5, "split": ["U64tceO4Ddtr4V6FMXSTJre4f6t4nPczWgtIkfo=", "t3hrQmsqonoBCl7T4f3bLqMShchtOtF3WesMGEs="], "shares": 9}
{"threshold": 5, "split": ["TcOzpm1jNtwsj0cdiLfd6oVHLGMMKRt52t9kU4E=", "RqJ1WKlufadMFwFLbIjvBs82BH/yP8CAT6kyv3M="], "shares": 9}
```

The important part of the code is:
```python
class KeySplitter:
    
    def __init__(self, numshares, threshold):
        self.splitter = Shamir(numshares, threshold)
        self.numshares = numshares
        self.threshold = threshold

    def split(self, key):
        xshares = [''] * self.numshares
        yshares = [''] * self.numshares
        for char in key:
            xcords, ycords = self.splitter.split(ord(char))
            for idx in range(self.numshares):
                xshares[idx] += chr(xcords[idx])
                yshares[idx] += chr(ycords[idx])
        return zip(xshares, yshares)
    
    def jsonify(self, shares, threshold, split):
        data = {
            'shares': shares, 
            'threshold': threshold, 
            'split': [
                base64.b64encode(split[0]),
                base64.b64encode(split[1])
            ]
        }
        return json.dumps(data)

if __name__ == "__main__":
    splitter = KeySplitter(9, 5)
    splits = splitter.split(FLAG)
    for i in range(0, 4):
        print splitter.jsonify(9, 5, splits[i])

```

So we know that the flag is encrypted one char at a time.
The last piece of the puzzle is the fact that `Shamir` object is created only once here, and therefore the polynomial is chosen only once.

For those unfamiliar with SSS, the algorithm is pretty simple:

1. We have some secret value X we want to encrypt in such a way, that it can be decrypted only if a certain number of people combine their "shares". Facebook uses this for example to enable recovering a lost account. You can provide your friends with some "shares", and each of the shares is not enough to recover the password, but multiple shares together can. You can give more shares to some people if you want, as long as it's not enough to decrypt the data with a single batch.

2. Technically this is done by polynomial interpolation. A random polynomial of order N is created and the secret value is placed as term of degree 0. Each of the shares is simply a random point on this polynomial. For polynomial of order 1 (linear function) you need 2 points to recover the polynomial, by solving a linear equation. At the same time there is an infinite number of such polynomials passing only through a single point. This scales up - there is always only a single polynomial of order N passing through N+1 points, but if we've got less points, it's impossible to find the right polynomial.

What we have in this task are some shares, so points on the polynomial for each of the flag letters.
The vulnerability is the fact that there is only one polynomial used for all of the letters (except the term of order 0).

If we can find this polynomial we can brute-force the flag character by character, because we can just create a polynomial with a random letter as term of order 0 and then check if all the points we have are on the courve or not.
If they are, then we've got the right polynomial and we guessed the letter correctly.

In order to recover the polynomial coefficients we can notice that the flag format is `midnight{...}` which means it has 2 letters `i`!
And since the polynomial is always the same, we actually got double the number of points for letter `i`, and this is actually enough to interpolate the polynomial!

First we parse the input files:

```python
def recover_splits(input_file_data):
    splits = []
    for (s0, s1) in re.findall('"split": \["(.*?)", "(.*?)"\]', input_file_data):
        splits.append((base64.b64decode(s0), (base64.b64decode(s1))))
    return splits


def recover_points_per_key_character(data):
    splits = recover_splits(data)
    points_per_char = []
    for point_id in range(len(splits[0][0])):
        points = []
        for idx in range(numshares):
            split = splits[idx]
            points.append((ord(split[0][point_id]), ord(split[1][point_id])))
        points_per_char.append(points)
    return points_per_char
```

And for this we get list of points per single flag character.
Now we get the points for `i` letters in flag format:

```
[(65, 117), (188, 58), (174, 120), (195, 162)]
[(16, 140), (49, 224), (227, 107), (109, 169)]
```

We can now interpolate those in `GF(2^8)` because this is where all the operations are taking place here and from this we get a polynomial `31x^4+173x^3+111x^2+219x+105` which makes sense, because `chr(105) == 'i'` as expected.

Now we can proceed to brute-force rest of the flag:

```python
def main():
    result = ""
    with codecs.open("shares.txt") as input_data:
        points_per_character = recover_points_per_key_character(input_data.read())
        print("\n".join(map(str, points_per_character)))
        for points_for_single_char in points_per_character:
            for c in string.printable:
                # 31x^4+173x^3+111x^2+219x+C
                p = Polynomial(
                    [IntegerInRing(ord(c)), IntegerInRing(219), IntegerInRing(111), IntegerInRing(173),
                     IntegerInRing(31)])
                failed = False
                for x,y in points_for_single_char:
                    if p(IntegerInRing(x)).value != y:
                        failed = True
                        break
                if not failed:
                    result += c
    print(result)
```

And we get `midnight{ehhh_n0t_3ven_cl0se}`

