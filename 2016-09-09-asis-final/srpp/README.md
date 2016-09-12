## Dam (Crypto, 277p)

###ENG
[PL](#pl-version)

We are given quite complicated file, but after simplification, the only important part is this:

```python
params = getParams(nbit)
N, g, k = params
email = 'admin@asis-ctf.ir'
client.send('params = (N, g, k) = ' + str(params) + '\n')
salt = urandom(32)
N, g, _ = params
x = Hash(salt, email, password)
verifier = pow(g, x, N)

client.send('Send the email address and the public random positive value A seperated by "," as "email, A": ' + '\n')
ans = client.recv(_bufsize).strip()
print ans
email, A = ans.split(',')
A = int(A)
assert (A != 0 and A != N), client.send('Are you kidding me?! :P' + '\n')
assert email == 'admin@asis-ctf.ir', client.send('You should login as admin@asis-ctf.ir' + '\n')
b = getRandomRange(1, N)
B = (k * verifier + pow(g, b, N)) % N

client.send('(salt,  public_ephemeral) = (%s, %d) \n' % (salt.encode('base64')[:-1], B))

u = Hash(A, B)

client.send('Send the session key: ' + '\n')
K_client = client.recv(_bufsize).strip()
assert K_client.isdigit(), client.send('Please send a valid positive integer as session key.' + '\n')
K_client = int(K_client)

S_s = pow(A * pow(verifier, u, N), b, N)
print 'S_s', S_s
K_server = Hash(S_s)
print 'K_server', K_server

client.send('Send a POC of session key: ' + '\n')
M_client = client.recv(_bufsize).strip()

assert M_client.isdigit(), client.send('Please send valid positive integer as POC.' + '\n')
M_client = int(M_client)

assert (K_server == K_client), client.send('The session key is not correct!' + '\n')
assert (M_client == Hash(Hash(N) ^ Hash(g), Hash(email), salt, A, B, K_client)), client.send('The POC is not correct!' + '\n')

M_server = Hash(A, M_client, K_server) # TODO: check server POC in clinet side

client.send('Great, you got the flag: ' + flag + '\n')
client.close()
```

This looks complicated, and hard to break, but let's look again. There are basically two checks we have to pass:

```python
assert (K_server == K_client), client.send('The session key is not correct!' + '\n')
assert (M_client == Hash(Hash(N) ^ Hash(g), Hash(email), salt, A, B, K_client)), client.send('The POC is not correct!' + '\n')
```

And the second one is no-issue (because every variable used in assert is given to us by challenge!). So we only have to calculate `K_client`.
How are we going to achieve this? Well this looks impossible - algorithm here is almost bulletproof. Almost - except one small scar...

```python
S_s = pow(A * pow(verifier, u, N), b, N)
```

A here is controlled by us. What if we could send A=0? Recovering `S_s` would be trivial (`0*anything == 0`). Alternatively we could send A=N. Unfortunatelly, challenge authors have thought about it:

```python
assert (A != 0 and A != N), client.send('Are you kidding me?! :P' + '\n')
```

But wait, what if we could send A=2N?

Well, this wasn't thought about, and this is how we solved this challenge.

The only nontrivial part is this:

```python
A = 2*N
K_client = 43388321209941149759420236104888244958223766953174235657296806338137402595305  # hardcoded K_client assuming that S_s = 0
s.send(email + ', ' + str(A) + '\n')
s.send(str(K_client) + '\n')
```

The rest is just basic mathematical operations on numbers given to us by challenge:

```python
def proof_of_work(s):
    data = recvuntil(s, ["Enter X:"])
    x_suffix, hash_prefix = re.findall("X \+ \"(.*)\"\)\.hexdigest\(\) = \"(.*)\.\.\.\"", data)[0]
    len = int(re.findall("\|X\| = (.*)", data)[0])
    print(data)
    print(x_suffix, hash_prefix, len)
    for x in itertools.product(string.ascii_letters + string.digits, repeat=len):
        c = "".join(list(x))
        h = hashlib.sha512(c + x_suffix).hexdigest()
        if h.startswith(hash_prefix):
            return c

print s.recv(9999)

proof = proof_of_work(s)
print proof
s.send(proof)

kot = recvuntil(s, ["public random"])
print kot

email = 'admin@asis-ctf.ir'
ls = kot.split('\n')
for l in ls:
    if 'params' in l:
        data = l[21:]
        N, g, k = eval(data)
        print N, g, k

A = 2*N
K_client = 43388321209941149759420236104888244958223766953174235657296806338137402595305
s.send(email + ', ' + str(A) + '\n')
s.send(str(K_client) + '\n')

# almost done, just need to calculate POC

kot = recvuntil(s, ['session key'])
print kot
ls = kot.split('\n')
for l in ls:
    if 'salt' in l:
        data = l[28:]
        salt, B = re.findall("\((.*),(.*)\)", data)[0]
        salt = salt.decode('base64')
        B = B.strip()
        print salt, B

poc = Hash(Hash(N) ^ Hash(g), Hash(email), salt, A, B, K_client)

print poc
s.send(str(poc))

print s.recv(999)
```

And that's it.


###PL version

Dostajemy całkiem skomplikowany plik, ale po uproszczeniu, jedyna skomplikowana część to to:

```python
params = getParams(nbit)
N, g, k = params
email = 'admin@asis-ctf.ir'
client.send('params = (N, g, k) = ' + str(params) + '\n')
salt = urandom(32)
N, g, _ = params
x = Hash(salt, email, password)
verifier = pow(g, x, N)

client.send('Send the email address and the public random positive value A seperated by "," as "email, A": ' + '\n')
ans = client.recv(_bufsize).strip()
print ans
email, A = ans.split(',')
A = int(A)
assert (A != 0 and A != N), client.send('Are you kidding me?! :P' + '\n')
assert email == 'admin@asis-ctf.ir', client.send('You should login as admin@asis-ctf.ir' + '\n')
b = getRandomRange(1, N)
B = (k * verifier + pow(g, b, N)) % N

client.send('(salt,  public_ephemeral) = (%s, %d) \n' % (salt.encode('base64')[:-1], B))

u = Hash(A, B)

client.send('Send the session key: ' + '\n')
K_client = client.recv(_bufsize).strip()
assert K_client.isdigit(), client.send('Please send a valid positive integer as session key.' + '\n')
K_client = int(K_client)

S_s = pow(A * pow(verifier, u, N), b, N)
print 'S_s', S_s
K_server = Hash(S_s)
print 'K_server', K_server

client.send('Send a POC of session key: ' + '\n')
M_client = client.recv(_bufsize).strip()

assert M_client.isdigit(), client.send('Please send valid positive integer as POC.' + '\n')
M_client = int(M_client)

assert (K_server == K_client), client.send('The session key is not correct!' + '\n')
assert (M_client == Hash(Hash(N) ^ Hash(g), Hash(email), salt, A, B, K_client)), client.send('The POC is not correct!' + '\n')

M_server = Hash(A, M_client, K_server) # TODO: check server POC in clinet side

client.send('Great, you got the flag: ' + flag + '\n')
client.close()
```

Wygląda na skomplikowane i trudne do złamania. Ale w sumie, są tylko dwa testy które musimy przejść:

```python
assert (K_server == K_client), client.send('The session key is not correct!' + '\n')
assert (M_client == Hash(Hash(N) ^ Hash(g), Hash(email), salt, A, B, K_client)), client.send('The POC is not correct!' + '\n')
```

I drugi z nich to żaden problem (bo każda zmienna użyta w assercie jest wysyłana do nas przez serwer zadania) - więc musimy tylko obliczyć `K_client`.
Jak zamierzamy to zrobić? Cóż, wygląda to na niemożliwe - algorytm jest prawie że kuloodporny. Prawie że - ma jeden drobny problem...

```python
S_s = pow(A * pow(verifier, u, N), b, N)
```

A tutaj jest kontrolowane przez nas. Co jeśli wysłalibyśmy A=0? Odzyskanie `S_s` byłoby trywialne (`0*cokolwiek = 0`). Albo moglibyśmy wysłać A=N. Niestety, twórcy zadania pomyśleli o tym:

```python
assert (A != 0 and A != N), client.send('Are you kidding me?! :P' + '\n')
```

Hmm, ale co jeśli wyślemy A=2N?

Cóż, nikt o tym widać nie pomyślał, i w ten sposób rozwiązaliśmy to zadanie.

Jedyna nietrywialna część naszego kodu to to:

```python
A = 2*N
K_client = 43388321209941149759420236104888244958223766953174235657296806338137402595305  # hardcoded K_client assuming that S_s = 0
s.send(email + ', ' + str(A) + '\n')
s.send(str(K_client) + '\n')
```

Reszta to podstawowe operacje matematyczne na liczbach które dostajemy od zadania:

```python
def proof_of_work(s):
    data = recvuntil(s, ["Enter X:"])
    x_suffix, hash_prefix = re.findall("X \+ \"(.*)\"\)\.hexdigest\(\) = \"(.*)\.\.\.\"", data)[0]
    len = int(re.findall("\|X\| = (.*)", data)[0])
    print(data)
    print(x_suffix, hash_prefix, len)
    for x in itertools.product(string.ascii_letters + string.digits, repeat=len):
        c = "".join(list(x))
        h = hashlib.sha512(c + x_suffix).hexdigest()
        if h.startswith(hash_prefix):
            return c

print s.recv(9999)

proof = proof_of_work(s)
print proof
s.send(proof)

kot = recvuntil(s, ["public random"])
print kot

email = 'admin@asis-ctf.ir'
ls = kot.split('\n')
for l in ls:
    if 'params' in l:
        data = l[21:]
        N, g, k = eval(data)
        print N, g, k

A = 2*N
K_client = 43388321209941149759420236104888244958223766953174235657296806338137402595305
s.send(email + ', ' + str(A) + '\n')
s.send(str(K_client) + '\n')

# almost done, just need to calculate POC

kot = recvuntil(s, ['session key'])
print kot
ls = kot.split('\n')
for l in ls:
    if 'salt' in l:
        data = l[28:]
        salt, B = re.findall("\((.*),(.*)\)", data)[0]
        salt = salt.decode('base64')
        B = B.strip()
        print salt, B

poc = Hash(Hash(N) ^ Hash(g), Hash(email), salt, A, B, K_client)

print poc
s.send(str(poc))

print s.recv(999)
```

I to w sumie tyle, wystarczyło to do zdobycia flagi.
