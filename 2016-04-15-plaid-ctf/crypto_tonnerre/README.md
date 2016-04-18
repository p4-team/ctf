## Tonnerre (Crypto, 200 points, 119 solves)

	We were pretty sure the service at tonnerre.pwning.xxx:8561 (source) was totally secure. 
	But then we came across this website and now we’re having second thoughts... 
	We think they store the service users in the same database?

###ENG
[PL](#pl-version)

This task consisted of two parts: website vulnerable to SQL injection and server
using certain cryptographic verification.

Using `doit.py` we quickly exploited the SQL vulnerability to dump information about the
only user stored in database: `username`, `verifier` and `salt` (although we didn't need salt).

The next part was forcing `public_server.py` to accept our input.
It prompted us for a number (I denote it `pC`) and calculated:
```
c=(pC*v)%N
check if c in forbidden set
r=random()
pS=(g**r)%N
res=(pS+v)%N
secret=((pC*b)**r)%N
key=f(res, secret)
```
It then sent us `res` and asked for resulting key. We knew `N` and `g` from the source code,
while `v` is the verifier we extracted from SQL injection.

It is easy to see that if we know `res`, we also know `pS`. Therefore, the task can be stated 
as follows:
```
Given pS, N, v, g
knowing pS=g**r % N,
 find (pC*v)**r % N for any pC.
```
We can see that the numbers we need to find and the one we know are quite similar - they are
both something to the power of `r` modulo `N`. If we make bases equal, we would succeed.
Indeed, it is quite easy to find solution of equation:
```
pC*v=g (mod N)
```
We can multiply both sides by modular inverse of `v` and get:
```
pC*v*modinv(v)=g*modinv(v) (mod N)
pC=g*modinv(v) (mod N)
```
Unfortunately, this solution would not be accepted, as this particular `pC` is in forbidden set.
However, we can square our "known" equation, to get:
```
pS**2=(g**2)**r (mod N)
```
Repeating steps above to this equation, we get:
```
pC=(g**2)*modinv(v) (mod N)
```
The number we need to find, is then:
```
(pC*v)**r = ((g**2)*modinv(v)*v)**r = (g**2)**r = (g**r)**2 = pS**2 (mod N)
```
Since we know `pS`, the task is solved - actual implementation is in `solve.py`.

###PL version
