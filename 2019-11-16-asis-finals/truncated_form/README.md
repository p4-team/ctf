# Truncated form (PPC, 208p, 19 solved)

In the task we connect to the server and we have to transform given prime to a very particular format.

For example for prime `p = 868687909307764501147060349605653041999229151489950514965301649295439020807494131325814865675340673135715073631764902639875388586413387565682677871906332667975579403827585630488178998236686725443`

We're supposed to generate `222379878419*457#/5610-1800` where `457#` means `primorial(457)`.

Our approach is fairly simple:

1. Let's iterate over numbers `i` which we will subtract in the end (like -1800 in the example)
2. For each of those numbers we factor the `p+i` number into primes (up to some reasonable values)
3. For each of the prime factors we calculate primorial and then we find the divisor, which will contain all primes smaller than the factor we're analysing right now, except for the prime factors we found for `p+i`.
4. We form the string representation and check if it's short enough. If not, we continute.

```python
from crypto_commons.generic import get_primes, factor_p, long_range
from crypto_commons.netcat.netcat_commons import receive_until_match, nc, send, interactive

def solve(p, primes):
    best = 0
    for i in long_range(0, 999999999):
        factors, res = factor_p(p + i, primes)
        factors += [res]
        for j in range(len(factors)):
            x = factors[j]
            if x >= primes[-1]:  # skip last large factor
                break
            primo = primorial(x, False)
            divisor = 1
            for prime in primes:
                if prime > x:
                    break
                if prime not in factors:
                    divisor *= prime
            c = primo / divisor
            if divisor > p:
                continue
            a = (p + i) / c
            if (a * primorial(x, False) / divisor - i) != p:
                break
            result = str(a) + "*" + str(x) + "#/" + str(divisor) + "-" + str(i)
            if len(result) <= 29:
                return result
    return best
```

Once we send the right response to the server we get: `ASIS{f2nD_7H3___MaxMerit___!!!!!!}`
