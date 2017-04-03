# Public Key Infrastructure (crypto)

## ENG
[PL](#pl-version)

In the task we get [code](task.py) running on the server.

We can "register" a new user, and for given `login name` and set of binary bytes `n` we get RSA-encrypted with `(65537, n)` digital signature of string `'MSG = {n: ' + n + ', name: ' + name + '}'`.
Bytes `n` are simply casted to int.

We can also "login" by providing `login name`, `n` and a proper signature, and this will give us the flag if we login as `admin`.
Obviously we can't register "admin" and there is no way around the check here.

The Digital Signature Algorithm is implemented with no issues here, so there is no vulnerability there.
It took us a while to figure out the mistake and how to exploit it.
The problem in the code is here:

```python
def makeK(name, n):
  return 'K = {n: ' + n + ', name: ' + name + ', secret: ' + SECRET + '}'
```

Value `k` should be secret and unpredictable for every signature, because if we can obtain 2 signatures with the same `k`, we can very simply recover the value of `k`.
In our case this condition is not really fulfilled, because md5 algorithm is prone to collisions.
It it also Merkle-Damgard hash prone to length extension, and therefore if we can get a collision on two inputs, the hash values will stay the same even if we add more data at the end, as long as we add the same data.
This means that if we can find a collision on prefix `'K = {n: ' + n` for two different `n` values, we will get identical `k` values (if we use the same `name`) because the suffixes are always the same.

We used `fastcoll/hashclash` to generate the collisions for the prefix `'K = {n: ' + n` with random bytes as `n` value.

There is, however, one slight issue -> we actually can't use a totally random `n` value!
After all the server is using this value for RSA encryption of the signature, so if we can't factor `n` we won't be able to decrypt the signature we need.
Therefore, we wrote a simple script which was checking the `n` values we got in the collision in factordb to make sure it is factored:

```python
def is_ok(data):
	if data.strip() == "CF *":
		return False
	if data.strip() == "CF":
		return False
	return True

def check_n(file):
	payload = open("colisions/"+file, "rb").read()[8:]
	n = int(payload.encode('hex'), 16)
	r = get(url="https://factordb.com/index.php?query="+str(n))	
	soup = BeautifulSoup(r.text)
	data = soup.getText().split("\n")
	return is_ok(data)
```

With this after a while we manage to get two nice collisions with proper `n` values: [col1](col1), [col2](col2).

They both are fully factored in factordb so we get factors:

```
factors1 = [234616432627, 705869477985961204313551643916777744071330628233585786045998984992545254851001542557142933879996265894077678757754161926225017823868556053452942288402098017612976595081470669501660030315795007199720049960329731910224810022789423585714786440228952065540955255662140767866791612922576360776884260619L]

factors2 = [119851, 236017, 5854608817710130372948444562294396040006311067115965740712711205981029362712183315259168783815905208719000197236691607700100836391807927746833977891792631066541406816904680111217125634549418611669208807316369565620310660295144628581977856740654199823679135895590513942858128229967305158632385155587L]
```

With this we can use standard RSA for first one, and multiprime RSA for the second one, and decode the signatures from the server.
The signature is a pair `(s,r)` or in our case a single value `r*Q + s` which can be easily split into `s` and `r` by div and mod.

Directly from the way the value `s` is calcualted  we have:

```
s_1 = modinv(k,q) * (H(msg_1) + private_key*r) mod q
s_2 = modinv(k,q) * (H(msg_2) + private_key*r) mod q
```

We can transform this further:

```
(s_1 - s_2) modq = (modinv(k,q) * (H(msg_1) + private_key*r) - modinv(k,q) * (H(msg_2) + private_key*r)) modq
```

then:

```
(s_1 - s_2) modq = modinv(k,q) * (H(msg_1) + private_key*r - H(msg_2) - private_key*r) modq
```

which removes the unknown `private_key*r` part leaving:

```
(s_1 - s_2) modq = modinv(k,q) * H(msg_1) - H(msg_2) modq
```

And therefore we get the equation for `k`:

```
k modq = ((H(msg_1) - H(msg_2)) * modinv((s_1 - s_2), q)) modq
```

If we have `k` we can easily recover the `private_key` again transforming the equation:

```
s = modinv(k,q) * (H(msg) + private_key*r) mod q
```

because now we know all the values, so we can transform this to:

```
private_key = ((s * k) - H(m)) * modinv(r, q)
```

Now if we have the private key we can sign any message we want.
Keep in mind that the value of `SECRET` which server uses to calculate `k` is not needed for us at all.
The value of `k` can be any number, so we can make:

```python
def simple_sign(name, n, priv):
    k = 5 # why not? ;)
    r = pow(G, k, P) % Q
    s = (modinv(k, Q) * (h(makeMsg(name, n)) + priv * r)) % Q
    return r * Q + s
```

And this will give us the proper signature for the data.
We calculate `admin_sig = simple_sign("admin", "1", private_key)`, and login with it to get the flag:

`DrgnS{ThisFlagIsNotInterestingJustPasteItIntoTheScoreboard}`

The whole solver script is [here](solver.py)

## PL version

W zadaniu dostajemy [kod](task.py) działająy na serwerze.

Możemy "zarejestrować" nowego użytkownika, a dla danego `loginu` oraz pewnych danych binarnych `n` dostaniemy zaszyfrowane za pomocą RSA z `(65537, n)` cyfrowy podpis dla stringa `'MSG = {n: ' + n + ', name: ' + name + '}'`.
Bajty `n` są tutaj zwyczajnie rzutowane do inta.

Możemy także "zalogować" się podając `login`, `n` oraz poprawny podpis i to da nam flagę jeśli zalogujemy się jako `admin`.
Oczywiście nie możemy zarejestrować loginu "admin" i nie ma da się tego obejść.

Digital Signature Algorithm jest tu zaimplementowan bez widocznych błędów ani różnic, więc nie ma tam żadnej podatności.
Zajęło nam trochę czasu znalezienie luki i wymyślenie jak ją wykorzystać.
Problem jest tutaj:

```python
def makeK(name, n):
  return 'K = {n: ' + n + ', name: ' + name + ', secret: ' + SECRET + '}'
```

Wartość `k` powinna być sekretna i nieprzewidywalna dla każdego podpisu, ponieważ jeśli jesteśmy w stanie uzyskać 2 podpisy z tym samym `k`, możemy łatwo wyliczyć to `k`.
W naszym przypadku ten warunek nie jest spełniony bo md5 jest podatne na kolizje.
Jest to take hash konstrukcji Merkle-Damgard podatny na length extension a to oznacza, że jeśli uzyskamy kolizje dla pewnych dwóch zbiorów danych wejściowych to wartość hasha md5 dla nich będzie równa nawet jeśli dodamy na koniec jakieś dane, o ile dodajemy te same dane.
To oznacza że jeśli znajdziemy kolizje dla prefixu `'K = {n: ' + n` dla dwóch różnych wartości `n` to uzyskamy identyczne wartości `k` dla nich (jeśli używamy takiego samego `name`) bo suffixy są takie same.

Użyliśmy `fastcoll/hashclash` do generowania kolizji dla prefixu `'K = {n: ' + n` z losowymi bajtami jako `n`.

Jest tutaj jednak pewien problem -> nie możemy użyć zupełnie dowolnego `n`!
Należy pamiętać, że serwer odsyła nam podpis zaszyfrowany przez RSA z użyciem `n`, więc jeśli nie umiemy sfaktoryzować `n` to nie będziemy mogli zdekodować podpisu.
W związku z tym napisaliśmy skrypt który sprawdzał w factordb wartości `n` dla których dostaliśmy kolizje, zeby upewnić się, że mamy dla nich faktoryzacje:

```python
def is_ok(data):
	if data.strip() == "CF *":
		return False
	if data.strip() == "CF":
		return False
	return True

def check_n(file):
	payload = open("colisions/"+file, "rb").read()[8:]
	n = int(payload.encode('hex'), 16)
	r = get(url="https://factordb.com/index.php?query="+str(n))	
	soup = BeautifulSoup(r.text)
	data = soup.getText().split("\n")
	return is_ok(data)
```

Dzięki temu po pewnym czasie udało nam się uzyskać kolizje z pasujacymi `n`: [col1](col1), [col2](col2).

Obie są w pełni sfaktoryzowanne:

```
factors1 = [234616432627, 705869477985961204313551643916777744071330628233585786045998984992545254851001542557142933879996265894077678757754161926225017823868556053452942288402098017612976595081470669501660030315795007199720049960329731910224810022789423585714786440228952065540955255662140767866791612922576360776884260619L]

factors2 = [119851, 236017, 5854608817710130372948444562294396040006311067115965740712711205981029362712183315259168783815905208719000197236691607700100836391807927746833977891792631066541406816904680111217125634549418611669208807316369565620310660295144628581977856740654199823679135895590513942858128229967305158632385155587L]
```

Dzięki temu możemy użyć klasycznego RSA dla pierwszego podpisu i multiprime RSA dla drugiego, żeby zdekodować podpisy wysłane przez serwer.

Podpis to para `(s,r)` lub jak w naszym przypadku jedna wartość `r*Q + s` którą łatwo rozłożyć na `s` i `r` za pomocą dzielenia i reszyt z dzielenia przez `Q`.

Bezpośrednio z tego jak liczymy `s` podczas generowania podpisu mamy:

```
s_1 = modinv(k,q) * (H(msg_1) + private_key*r) mod q
s_2 = modinv(k,q) * (H(msg_2) + private_key*r) mod q
```

Co można przekształcić do:

```
(s_1 - s_2) modq = (modinv(k,q) * (H(msg_1) + private_key*r) - modinv(k,q) * (H(msg_2) + private_key*r)) modq
```

a następnie uprościć:

```
(s_1 - s_2) modq = modinv(k,q) * (H(msg_1) + private_key*r - H(msg_2) - private_key*r) modq
```

Co pozwala pozbyć się nieznanej części `private_key*r`, zostawiając:

```
(s_1 - s_2) modq = modinv(k,q) * H(msg_1) - H(msg_2) modq
```

A ty samym równanie dla `k` to:

```
k modq = ((H(msg_1) - H(msg_2)) * modinv((s_1 - s_2), q)) modq
```

Mając `k` możemy teraz łatwo wyliczyć `private_key`, znów przekształcając równanie dla `s`:

```
s = modinv(k,q) * (H(msg) + private_key*r) mod q
```

Ponieważ znamy wszystkie parametry możemy przekształcic to do postaci:

```
private_key = ((s * k) - H(m)) * modinv(r, q)
```

I teraz mając wyliczony klucz prywatny możemy podpisać co tylko chcemy.
Warto pamiętać, że nie potrzebujemy wartości `SECRET` za pomocą której serwer oblicza wartość `k`.
Wartość `k` może być zupełnie dowolna więc możemy napisać:

```python
def simple_sign(name, n, priv):
    k = 5 # why not? ;)
    r = pow(G, k, P) % Q
    s = (modinv(k, Q) * (h(makeMsg(name, n)) + priv * r)) % Q
    return r * Q + s
```

I taka funkcja pozwoli poprawnie podpisywać dane.
Obliczamy więc `admin_sig = simple_sign("admin", "1", private_key)`, i logując się tym podpisem dostajemy flagę:

`DrgnS{ThisFlagIsNotInterestingJustPasteItIntoTheScoreboard}`

Cały skrypt solvera jest [tutaj](solver.py)
