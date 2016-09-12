## Dsa (Crypto, 333p)

###ENG
[PL](#pl-version)

We are given following python code - it is supposed to sign messages:
```python
#!/usr/bin/python

from hashlib import *
from Crypto.Util.number import *
from gmpy import *
import os

def param_gen():
    q = getPrime(1024)
    while True:
        t = 2*getRandomRange(1, 2**256)
        p = t*q + 1
        if is_prime(p):
            break
    while True:
        h = getRandomRange(1, p-1)
        g = pow(h, (p-1)/q, p)
        if g != 1:
            break
    return (p, q, g)

def key_gen(params):
    p, q, g = params
    x = getRandomRange(1, q)
    y = pow(g, x, p)
    pubkey, privkey = y, x
    return pubkey, privkey

def sign(msg, privkey, params):
    p, q, g = params
    while True:
        k = getRandomRange(1, 1024) * pow(pubkey, privkey, p) % q
        r = pow(g, k, p) % q
        s = invert(k, q) * ( int(sha512(msg).hexdigest(), 16) + privkey * r) % q
        if r*s != 0 :
            break
    return (int(r), int(s))

def verify(msg, signature, pubkey, params):
    p, q, g = params
    r, s = signature
    if (0 < r < q) and  (0 < s < q) :
        w = invert(s, q)
        u1 = (int(sha512(msg).hexdigest(), 16) * w) % q
        u2 = (r * w) % q
        v = ((pow(g, u1, p) * pow(pubkey, u2, p)) % p) % q
        if v == r:
            return True
    return False

params = param_gen()
p, q, g = params
print params
pubkey, privkey = key_gen(params)

for i in range(0, 40):
    msg = 'ASIS{' + os.urandom(16).encode('hex') + '}'
    signature = sign(msg, privkey, params)
    r, s = signature
    print str((msg, r, s))

```

This challenge asks us to recover private key (x) given only a handful (around 40) signatures, public key, and public parameters given (attached to this solution in github).

After a while, we find a vulnerability in this challenge - 
```python
k = getRandomRange(1, 1024) * pow(pubkey, privkey, p) % q
```

This is obviously insecure, as only 1024 ks can possibly be generated. If only we could recover k, this challenge would be trivial - given k we can calculate privkey from linear equation:

```python
s = invert(k, q) * ( int(sha512(msg).hexdigest(), 16) + privkey * r) % q
<=>
s * k - int(sha512(msg).hexdigest(), 16) * invert(r, q) % q = privkey
```

But we don't know k... yet.

After another while, we noticed that if we could find two messages encrypted with the same k, challenge would be easy again. We could solve system of linear equations:

```
s = invert(k, q) * ( int(sha512(msg0).hexdigest(), 16) + privkey * r) % q
s = invert(k, q) * ( int(sha512(msg1).hexdigest(), 16) + privkey * r) % q
```

...where k and privkey are unknowns. But again, this wasn't the case in this challenge.

And finally, when we began to fall into the pit od despair, we noticed that we could create another system of linear equations. Because k = (1..1024) * MAGIC (where `MAGIC = pow(publickey, privkey)`, but it's not important), we can write above equations as:

```
s = invert(k1 * MAGIC, q) * (int(sha512(msg0).hexdigest(), 16) + privkey * r) % q
s = invert(k2 * MAGIC, q) * (int(sha512(msg1).hexdigest(), 16) + privkey * r) % q
```

In more mathematical terms, we can solve this system of equations as follows:

```
s1 = (c1 + priv*r1) / (k1*magic)
s2 = (c2 + priv*r2) / (k2*magic)

1 = (c1 + priv*r1) / (k1*magic*s1)
1 = (c2 + priv*r2) / (k2*magic*s2)

(c1 + priv*r1) / (k1*magic*s1) = (c2 + priv*r2) / (k2*magic*s2)
(c1 + priv*r1) * (k2*magic*s2) = (c2 + priv*r2) * (k1*magic*s1)
c1*k2*magic*s2 + priv*r1*k2*magic*s2 = c2*k1*magic*s1 + priv*r2*k1*magic*s1
c1*k2*s2 + priv*r1*k2*s2 = c2*k1*s1 + priv*r2*k1*s1
priv*r1*k2*s2 - priv*r2*k1*s1 = c2*k1*s1 - c1*k2*s2 
priv*(r1*k2*s2 - r2*k1*s1) = c2*k1*s1 - c1*k2*s2 
priv = (c2*k1*s1 - c1*k2*s2) / (r1*k2*s2 - r2*k1*s1)
```

Great, we have private key! But we have to bruteforce 1024 possible values of k1 and k2. It's easy enough in python:

```python
from hashlib import *
from Crypto.Util.number import *
from gmpy import *
import os

def hash(msg):
    return int(sha512(msg).hexdigest(), 16)

def solve_for(params, set1, set2):
    p, q, g = params
    msg1, r1, s1 = set1
    msg2, r2, s2 = set2
    c1, c2 = hash(msg1), hash(msg2)
    for k1 in range(1, 1024):
        print k1
        for k2 in range(1, 1024):
            priv = (c2*k1*s1 - c1*k2*s2) * invert(r1*k2*s2 - r2*k1*s1, q) % q
            if pubkey == pow(g, priv, p):
                print priv
            
params = (
19990043472646209601994864878783430356973105946195950979159251182377121897576105462833887676561348770957108482823143337701724893247634876231133001112659622843245186144815694000013210989382541478073551247763586093331215996260234193847013210807939190828438263706901950228866893621933887960930392778176297205331569773161563794018138992335091883899396920586572927792555042350138728812073331L, 91629484598379105033512409529628860433949558415030791938154302542936417405614272511539966765257644706180090102931421315331051281240103609205686784098900471134711603588304765157414857991689054932897002635007537146809343047302801243835776634361209432398032301656027511721047704054332653738042312201931970395721L, 13622145302845273763875935516952425125176393702394844695432724066597834898277677169908234619701079219174550050531086255052810547971127992364106395259623997686454799745423099095097056224348731737512112568608406081844751809559052204755863089238863185755017905098158596830866362329243334855589147537151782745634416243769180780246626300677625340613515232605024658651528787608437872606367959L)
set1 = ('ASIS{f178fcdecf80695744078436c8443d21}', 90237121958952251064976624492762150213417521896687572941345633764310618911601030617031373795520024583293535375710106225552196376797438589929204291257545448726331743603280815369427093966770848920593554708454565838054224752549404158493278464435213107237527453340811242850765181020853492694252650516970176641788L, 45699965566033911695982803604354032305058506238185457115666900773211243249439993822400900118887663777494151014067272471514622506941212402877792085312967213090334714190020080393819021065260516916603206309212756987461405393121419856054170230373811099272880018713486783939408418428725471847346917597357388173871L)
set2 = ('ASIS{13d82a52a86b3f60d1d5d0a9a8fbd38c}', 82549501691566010240713957921730895287132128726058380260123211081436703044836270709304732846086147549660502736557189123678902405383474467404416541210982435469292602012427497998459504126706153698217704534579606635614323510632001857553260216879546038347723055837869594047336385462982125121614977106061534077159L, 14100015776662279808055950447194278668824709578034279558537621662053558677298084425976090376958899238099311275299915689425374231782256233762239739696534102757257328540054634833325260578944419955606514868448883176935887227050496260234118031035188783965371809668020726016057511098782430965590465392354859239207L)
pubkey = 5120206348411789470161536127663499609309512038887109068976130122757582186109731229884381538683899917243667766639035225751229538595906667027298668257572271684995053081914448593696545954848592131805237134557157103971058735552127997038702518466039596176245969237004179261427946425137677159565508198606851760199742107673019486271187331752618149416170682584515782866631954825392784384052948

solve_for(params, set1, set2)
```

And we finally get our flag: ASIS{1e58445616cd5178632ae15bef51c4a3}

###PL version

to be done?
