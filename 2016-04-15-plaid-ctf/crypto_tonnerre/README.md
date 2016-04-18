## Tonnerre (Crypto, 200 points, 119 solves)

	We were pretty sure the service at tonnerre.pwning.xxx:8561 (source) was totally secure. 
	But then we came across this website and now we’re having second thoughts... 
	We think they store the service users in the same database?

###ENG
[PL](#pl-version)

This task consisted of two parts: website vulnerable to SQL injection and server authenticating via `zero knowledge proof protocol`.

Using [script](doit.py) we quickly exploited the SQL vulnerability to dump information about the only user stored in database: `username`, `verifier` and `salt` (although we didn't need salt).

The next part was forcing [server script](public_server.py) to authenticate us and get the flag.
The idea of zero knowledge proof is that the server aka `verifier` knows a `secret` and challenges the user to prove that the user also knows the `secret`.
This has to happen without disclosing the `secret` itself so no part of the `secret` should ever be transmitted.
The general approach to this problem is that the `verifier` provides a random task that can be solved only by someone with `secret`.

In our case the server prompted us for some number (denoted as `pC`) and calculated:

```
c=(pC*v)%N
if c not in forbidden set:
	r=random(2,N-3)
	pS=(g**r)%N
	res=(pS+v)%N
	secret=((pC*b)**r)%N
	key=f(res, secret)
```

It then sent us `res` and asked for resulting key.
If we knew the `secret` factorization of `N` then we could simply use EGCD to recover `r` exponent (like in RSA), but of course we don't know it.

We know `N` and `g` from the source code, while `v` is the verifier value we extracted via SQL injection.

It is easy to see that if we know `res`, we can calculate `pS`.
This is because `pS` has to be less than `N` (it is reminder from division modulo `N`) and we know the value of `v` which is in the same order as `N`.
This implies that `pS+v` has to be between `v` and `2N-1` and thus the modular division reminder of `res=(pS+v) mod N` can be:

- Bigger than `v` which means that `pS` was small enough that the sum `pS+v` did not exceed `N` and this means the `pS = res - v`
- Smaller than `v` and this means the actual sum was greater than `N` and got cut by modulo and therefore `pS = res - v + N`

Our case was the second one.

Now the task can be stated  as follows:
```
Given pS, N, v, g
knowing pS=g**r % N,
 find (pC*v)**r % N for any pC.
```

We can see that the numbers we need to find and the one we know are quite similar - they are both something to the power of `r` modulo `N`. 
If we make bases equal, we would succeed. 
Indeed, it is quite easy to find solution of equation:

```
pC*v=g (mod N)
```

We can multiply both sides by modular inverse of `v` mod `N` and get:

```
pC*v*modinv(v)=g*modinv(v) (mod N)
pC=g*modinv(v) (mod N)
```

Unfortunately, this solution would not be accepted, as this particular `pC` is in forbidden set.
So are also the obvious solutions like `pC=0` which would give `0**r % N = 0`

Since the only thing we can use is the value of `g**r (mod N)` it's clear that the `pC*v` has to be connected with `g`.
We also know that the most natural operation when dealing with modular powers are powers so we figure that we could square our "known" equation, to get:
```
pS**2=(g**2)**r (mod N)
```

So we know the value of `(g**2)**r (mod N)` and we need to convince the server to ask us to provide this value, so we need to provide such `pC` so that `pC*v mod N == g**2 mod N`

Repeating steps above to this equation, we get:

```
pC=(g**2)*modinv(v) (mod N)
```

And therefore is we provide such `pC` the server will ask us for the value of:

```
(pC*v)**r = ((g**2)*modinv(v)*v)**r = (g**2)**r = (g**r)**2 = pS**2 (mod N)
```

And since we know `pS`, the task is solved and the flag is `PCTF{SrP_v1_BeSt_sRp_c0nf1rm3d}` - actual implementation is [here](solve.py).

###PL version

Zadanie składało się z dwóch części: strony podatnej na SQL injection oraz serwera autentykującego za pomocą `zero knowledge proof protocol`.

Korzystając ze [skryptu](doit.py) szybko exploitowalismy podatność SQL i pobralismy informacje na temat jedynego użytkownika z nazy danych - `username`, `verifier` i `salt` (akurat salt nie był nam potrzebny).

Następny krok to zmuszenie [skryptu serwera](public_server.py) aby nas zautentykował i podał flagę.
Idea zero knowledge proof polega na tym, ze server czyli `verifier` zna pewien `sekret` i daje użytkownikowi do rozwiązania zadanie które ma potwierdzić że użytkownik także zna `sekret`.
To musi odbywać się bez odkrycia `sekretu` więc żadna jego część nie może zostać transmitowana.
Ogóle podejście do tego problemu polega na tym, że `verifier` generuje losowe zadanie możliwe do rozwiązania tylko przez kogoś z `sekretem`

W naszym przypadku serwer pytał o pewną liczbę (oznaczoną dalej jako `pC`) i obliczał:

```
c=(pC*v)%N
if c not in forbidden set:
	r=random(2,N-3)
	pS=(g**r)%N
	res=(pS+v)%N
	secret=((pC*b)**r)%N
	key=f(res, secret)
```

Następnie przesyłał nam wartość `res` i pytał o wynikowy klucz.
Gdybyśmy znali `sekret` czyli faktoryzacje `N` moglibyśmy użyć EGCD do odzyskania wykładnika `r` (jak w RSA), ale oczywiście nie możemy tego zrobić.

Wiemy ile wynoszą `N` oraz `g` z źródła serwera, podczas gdy `v` zostało przez nas wyciągnięte z bazy danych przez SQL Injection.

Łatwo zauważyć że jeśli znamy `res` to możemy łatwo policzyć `pS`.
Wynika to z faktu, że `pS` musi być mniejsze od `N` (to reszta z dzielenia przez `N`) oraz znamy wartość `v` która jest tego samego rzędu co `N`.
To oznacza, że `pS+v` musiby być pomiędzy `v` i `2N-1` a z tego wynika że reszta z dzielenia modulo `res=(pS+v) mod N` może być:

- Większa od `v` co znaczy, że `pS` było małe i suma nie przekroczyła `N` i tym samym `pS = res - v`
- Mniejsza od `v` co znaczy, że suma była większa od `N` i została obcięta przez modulo i tym samym `pS = res - v + N`

W naszym przypadku prawdziwa była sytuacja numer 2.

Teraz zadanie można przedstawić jako:
```
Mając dane pS, N, v, g
wiedząc że pS=g**r % N,
 znajdź (pC*v)**r % N dla pewnego pC.
```

Możemy zauważyć, że liczby których szukamy i które znamy są dość podobne - i tutaj i tutaj mamy `r`-te potęgi modulo `N`.
Gdybyśmy mogli ustalić identyczne podstawy potęg rozwiązalibyśmy zadanie.
Łatwo wyliczyć potrzebną wartość `pC` z równania:

```
pC*v=g (mod N)
```

Możemy obustronnie pomnożyć to przez modinv `v` mod `N` i dostajemy:

```
pC*v*modinv(v)=g*modinv(v) (mod N)
pC=g*modinv(v) (mod N)
```

Niestety takie rozwiązanie znajduje się w zbiorze zabronionych wartości dla `pC`.
Podobnie jest z innymi oczywistymi rozwiązaniami jak `pC=0` które dałoby łatwe do przewidzenia `0**r % N = 0`

Jako że jedyna wartość którą możemy wykorzystać to `g**r (mod N)` jest jasne że `pC*v` musi mimo wszystko być powiązane z `g`.
Wiemy też, że najbardziej naturalną operacją kiedy mamy do czynienia z potęgowaniem jest potęgowanie, dochodzimy więc do wniosku, że moglibyśmy podnieść znane równanie do kwadratu dostając:

```
pS**2=(g**2)**r (mod N)
```

Wiemy więc teraz ile wynosi `(g**2)**r (mod N)` i potrzebujemy przekonać serwer aby spytał nas o tą właśnie wartość, więc musimy dostarczyć takie `pC` że `pC*v mod N == g**2 mod N`

Wykonujac kroki podobne jak powyżej dla nowego równania dostajemy:

```
pC=(g**2)*modinv(v) (mod N)
```

I tym samym jeśli podamy tak wyliczone `pC` serwer zapyta nas o:

```
(pC*v)**r = ((g**2)*modinv(v)*v)**r = (g**2)**r = (g**r)**2 = pS**2 (mod N)
```

A wartość `pS` jest nam znana więc zadanie jest rozwiązane i flaga to `PCTF{SrP_v1_BeSt_sRp_c0nf1rm3d}` - całe rozwiązanie dostępne [tutaj](solve.py)

