# Baby RSA (crypto)


## ENG
[PL](#pl-version)

In the task we get [encrypted flag](flag.enc), [public key](pubkey) and encryption [source code](enc.rb) written in Ruby.

All math code is sound and the main part is just:

```ruby
p = rand(2**1024)
q = 19 * p + rand(2**512)

p = next_prime(p)
q = next_prime(q)

e = 65537
d = mod_inverse(e, (p - 1) * (q - 1))

n = (p.to_i * q.to_i)

flag = File.binread('flag').unpack1("H*").to_i(16) * 256
while flag * 256 + 255 < n
  flag = flag * 256 + rand(256)
end

enc = mod_pow(flag, e, n)
dec = mod_pow(enc, d, n)
fail unless dec == flag
File.write('pubkey', [n, e].to_json)
File.write('flag.enc', enc)
File.write('privkey', [n, d].to_json)
```

So it's a classic RSA encryption, just as indicated in the task name.
The flag is fully padded with random bytes, the primes are large and of similar order, most likely not factorizable directly.

Once we validated the math code and decided that it's ok and it doesn't help us that it uses Fermat primarity test (so `p` or `q` could be composite Carmichael numbers), the only vulnerability could be in key generation.

The `N` is generated as:

```python
p = rand(2**1024)
q = 19 * p + rand(2**512)
p = next_prime(p)
q = next_prime(q)
n = (p.to_i * q.to_i)
```

It's not a normal thing to derive `q` from `p`, so it might indicate some problem with this setup.

If we had there `q = 19*p` it would be obviously weak, since then `N = (p+delta1)*(19*q+delta2)` where deltas are reasonably small and we could divide `N` by 19 and try to user Fermat factorization to look for the primes.
But we have this `+ rand(2**512)` which seems to make it impossible to brute force.

However we notice that this added rand is actually small, at least compared to the `p` and `q` which are both ~1024 bit long.
Same goes for our `delta` values (coming from `.next_prime()`), they will be small as well.
It means that adding such numbers will only upset lower half of the bits of `p` and `q` leaving high bits intact.
This gives us an interesting property - since high bits are preserved, from high bits point of view we actually have the case `N = p*19*p`!

We can do `p_approx = gmpy2.iroot(N/19)` to obtain an approximation of `p` where high bits are correct. 
With this setup `q_approx = p_approx * 19 + 2**512` and this is basically the upper bound for `q` (lower bound would be just `q_approx * 19`)

From our local tests we can get about 515-520 bits intact this way.

So we have more than N/4 of the most significant bits of one of the primes, is this enough to recover the whole prime?

Let's look at this from the other side, we have value `q_approx` and we want to recover value `delta` such that `q = q_approx - delta` (or `+ delta` if we used the lower bound instead of upper bound)

If we make univariate polynomial in ring modulo `N` such that `F(x) = q_approx - x` then it's clear that the `delta` we're looking for is root of this polynomial, since `q` is a factor of `N` and thus `q mod N == 0`.

And the root we need is also not that big, we know it's actually the low bits of `q` we're missing, so at most `2**512`, which is less than `N/4`.
We know from Coppersmith theorem that we can efficiently find small roots of such polynomial, so we proceed with sage code:

```python
p_approx = isqrt(N/19)
q_approx = 19*p_approx + 2**512

F.<x> = PolynomialRing(Zmod(N), implementation='NTL')
f = x - q_approx
d = f.small_roots(X=2**hidden, beta=0.5)
```

And this should give us the `delta` value we were looking for and recover `q`.

Full solution is:

```python
hidden = 512
N = 386931010476066075837968435835568572278162262133897268076172926477773222237770106161904290022544637634198443777989318861346776496147456733417801969323559935547762053140311065149570645042679207282163944764258457818336874606186063312212223286995796662956880884390624903779609227558663952294861600483773641805524656787990883017538007871813015279849974842810524387541576499325580716200722985825884806159228713614036698970897017484020439048399276917685918470357385648137307211493845078192550112457897553375871556074252744253633037568961352527728436056302534978263323170336240030950585991108197098692769976160890567250487423
n = 386931010476066075837968435835568572278162262133897268076172926477773222237770106161904290022544637634198443777989318861346776496147456733417801969323559935547762053140311065149570645042679207282163944764258457818336874606186063312212223286995796662956880884390624903779609227558663952294861600483773641805524656787990883017538007871813015279849974842810524387541576499325580716200722985825884806159228713614036698970897017484020439048399276917685918470357385648137307211493845078192550112457897553375871556074252744253633037568961352527728436056302534978263323170336240030950585991108197098692769976160890567250487423
e = 65537
ct = 238128932536965734026453335534508678486770867304645614119195536048961186128744314667991999168452564298994773996973787655358503271491181214369796509942047091225518293577154563021214085132019889288510474458242494876257330038265066123460887568813277411779817556316602871932730284368524299559699693787556478631297630514938453794107136748994144175123917418701679413905695916367530746728699301383100433069740863537869450361306987480687067608102552418211244703552910903168179094472596152349098076535870469807035136435631458879919434041758274344589567529971195683495146426258135341109919085270442486183365562919531353370683625

p_approx = isqrt(N/19)
q_approx = 19*p_approx + 2**512

F.<x> = PolynomialRing(Zmod(N), implementation='NTL')
f = x - q_approx
d = f.small_roots(X=2**hidden, beta=0.5)
if d:
	d = d[0]
	print('delta',d)
	print('q = q_approx - delta', q_approx - d)
	q = q_approx - d
	p = int(N)/int(q)
	phi = (p-1)*(q-1)
	d = inverse_mod(int(e), int(phi))
	print(hex(long(pow(ct,d,n)))[2:-1].decode("hex"))
```

Which gives us `TWCTF{secretly_cherry-blossom-viewing}`

## PL version
