# A7 ~ Gee cue elle (misc, 283p)

> We installed a fancy automatic attack protection system to be more secure against automated attacks from robots and hackers so it can be fully A7 compliant!

> Hint: .yaml~

> start.html

In this task we are given a small HTML file. Its whole content is here:
```html
<script>
location.replace('http://'+parseInt(Math.random()*1e15)+'-abuse.web.ctfcompetition.com/login');
</script>
```

It's a simple redirect to randomly generated host. What we see next, is a simple login site. 
There is a login and password
field, along with a `~Login~` button. Trying to type anything into the fields and clicking the
button shows a popup saying `Please match the requested format`. OK, we may be able to craft a
request anyway (the check is client-side), but let's not do this yet. Instead, we'll peek
into the source of the website. Honestly, not much is here, just the regex for checking the 
fields: `admin` for the login field, and `CTF[{]qu0t45[a-z0-9_]{16}www-[0-9A-Za-z_-]{64}[}]` for
the password.

When we type the login and password matching the formats, we receive a popup saying 
`Wrong password`. Nothing unexpected. However, if we check for SQL injection by forging a 
request with apostrophe character in password field, we receive a redirect to a subpage
showing popup 
`Parse Error: Identifier is a reserved keyword at symbol ANCESTOR`.
Hmmm. Googling the error shows it's an error of GQL (Google Query Language, alternative to SQL).
Now we can make sense of the challenge title: "Gee cue elle" is the phonetic form of GQL.

GQL is known for being difficult to inject to. We were stuck at this point for a while, but 
then a hint arrived: `.yaml~`.

As one of the first steps, we checked `robots.txt` file. It showed:
```
User-agent: *
Disallow: /app.yaml
Disallow: qa!
```
We obviously tried to fetch the `app.yaml`, but the request was blocked (maybe permissions 
issue). Anyway, after the hint, we thought to append a tilde character to the filename, as 
though someone left editor temporary files on the server. And it worked! Here are the contents
of the file:
```
service: anon2-lmuwucba5we9gi5a
runtime: python27
api_version: 1
threadsafe: true

handlers:
- url: /login
  script: main.app

- url: /
  static_files: index.html
  upload: index.html

- url: /(.+)
  static_files: \1
  upload: .*[.](?!py$).*

libraries:
- name: webapp2
  version: latest
- name: jinja2
  version: latest

skip_files:
- ^(.*/)?\.bak$
```

Looks like it's App Engine's configuration file 
(`https://cloud.google.com/appengine/docs/standard/python/config/appref`).
After looking at some of sample projects using this platform, we noticed a lot of them contains
`main.py` file. We checked for its presence on the server, and we managed to download it
when we appended a tilde (so, temporary file again).

Now we have full application source code. It appears it's a pretty basic login checker,
but just as we noticed earlier, there is an GQL injection:
```python
  def post(self):
    sql = "SELECT password FROM UserModel WHERE ANCESTOR IS :1 AND user = '%s'"
    query = ndb.gql(sql % self.request.get("user"), self.quota.key)
    result = query.fetch(1)
    if not result:
      self.redirect("/index.html?e=%s" % urllib.quote("Wrong username"))
    elif result[0].password != self.request.get("password"):
      raise Exception("Wrong password")
    else:
      self.response.write(self.request.get("password"))
```
The query should have used `:2` placeholder for username, instead of formatting the query
using `%s`. 

Well, it seems we can't really get password directly sent to us, because the only result
we can have is that we either have `Wrong username` error, or `Wrong password` one (or
correct password, but we won't get it by accident ;]). Wrong username will be returned only
if the query doesn't return any rows - and we know `admin` user exists. So, if we set
username to `admin' AND some_check`, we might have error-based injection, and be able to 
dump the password bit by bit. In fact, we used the following username:
```
admin` AND password > 'checked_password
```
The full query then looks like:
```
SELECT password FROM UserModel WHERE ANCESTOR IS :1 AND user = 'admin' AND password > 'checked_password'
```
Now we can binary searched the password.


... or so we thought. I haven't mentioned that, but the application implements a simple
abuse detection. When too many password checks have been done, or too many errors have 
been made, it bans us for 90s. In addition, it bans us permamently after 2240s. It even 
writes that in the response if we get banned:
```
<h1>Abuse detection system triggered!</h1>
<h3>You have been banned for 90 seconds.</h3>
<p>
  <b>
    If you believe this is a mistake, contact your system administrator.
  </b>
  Possible reasons include:
  <ul>
    <li>Generating too many errors too quickly
      <!--DEBUG: 2 queries / 30 seconds--></li>
    <li>Making too many requests too quickly
      <!--DEBUG: 13 queries / 30 seconds--></li>
    <li>Spending too much time without authenticating
      <!--DEBUG: 2240 seconds--></li>
  </ul>
</p>
```

When I first implemented the binary search, I just got throttled so much, that I eventually
hit the 2240s limit while getting less than half of the password. I retried a couple of times,
but the results were the same.

Hmmm. Let's make some calculations.

The password follows a certain regex. From the Python source, we know all the characters,
except for 64 pseudo-random base64 characters. Since each base64 character has 6 bits of
entropy, that means we have a total of `64*6 == 384` bits and we need that many queries.
On average, half of them counts as errors (`Wrong password` is signalled through raising
an exception, while `Wrong username` directly redirects). If we don't throttle requests
on our side, we will get banned for 90s after around 4 requests, so reading all bits will
take approximately `384/4*90 == 8640` seconds. That's way too much. We can reduce it
threefold if we throttle the requests locally - in other words, when we got 2 errors within
the last 30 seconds, we wait until this condition is no longer true. That algorithm
will give password after, very approximately, `384/4*30 == 2880` seconds. That's much
closer to the limit of 2240s, but still, when we tried it a couple of times, we were
getting banned too soon. 

What else can we do? Well, let's assume for a moment only error requests are counted towards
the limit, and otherwise we can do them as much as we can. Then, we would be able to check
consecutive letters: `A`, `B`, `C`, and so on, each time getting free `Wrong username`,
until we finally hit the correct letter with `Wrong password`. This would take only one
error per letter, so one timeout per 4 letters or `64/4*30 == 480` seconds (not
counting latency for checking all the small characters). 

Unfortunately, the non-error requests are limited too (up to 13 requests per 30 seconds),
so we cannot directly apply that strategy. Instead, we biased our binary search algorithm
to divide the search space not in the middle, but at around 90%. The value is pretty arbitrary,
it should probably be close to `allowed_hits/(allowed_hits+allowed_errs)`, but the truly
optimal strategy would also take into account how many of the errors are already used up.
We decided not to bother with such hard optimizations and just opened 20 instances of the
biased binary search, and after 2240s we found two of them actually managed to squeeze
through and calculated the whole flag.

CTF-quality code for solving is available in `doit2.py` file. 
