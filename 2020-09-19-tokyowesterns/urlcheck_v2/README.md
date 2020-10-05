# urlcheck v2
Just like in previous prolem here we have a simple form that makes the http request for us and returns the response. Quick glance at the code:
```python
import os, re, time, ipaddress, socket, requests, flask
from urllib.parse import urlparse

app = flask.Flask(__name__)
app.flag = '***CENSORED***'

def valid_ip(ip):
    try:
        result = ipaddress.ip_address(ip)
        # Stay out of my private!
        return result.is_global
    except:
        return False

def valid_fqdn(fqdn):
    return valid_ip(socket.gethostbyname(fqdn))

def get(url, recursive_count=0):
    r = requests.get(url, allow_redirects=False)
    if 'location' in r.headers:
        if recursive_count > 2:
            return '&#x1f914;'
        url = r.headers.get('location')
        if valid_fqdn(urlparse(url).netloc) == False:
            return '&#x1f914;'
        return get(url, recursive_count + 1)
    return r.text

@app.route('/admin-status')
def admin_status():
    if flask.request.remote_addr != '127.0.0.1':
        return '&#x1f97a;'
    return app.flag

@app.route('/check-status')
def check_status():
    url = flask.request.args.get('url', '')
    if valid_fqdn(urlparse(url).netloc) == False:
        return '&#x1f97a;'
    return get(url)
```
so we need to make an SSRF to http://localhost/admin-status

The problem it that first it checks if the domain resolves to 127.0.0.1 and fails if so.

Whole operation, however, is not atomic. One needs to notice that the domain is resolved twice - first in `valid_ip` function for checking if the ip is not local, then while making the final request in `get` function. That means we can make us of the technique called *DS Rebinding*. If we can make our DNS server respond with global IP address for the first requests and with 127.0.0.1 for the second - we'll get a flag :)

Luckily there are open services working just like we want, so we don't have to configure the server ourselves. One of them is https://lock.cmpxchg8b.com/rebinder.html. We generate the URL, try a couple of times, and... here it is!
```
$ curl 'http://urlcheck2.chal.ctf.westerns.tokyo/check-status?url=http://4d37d938.7f000001.rbndr.us/admin-status'
TWCTF{17_15_h4rd_70_55rf_m17164710n_47_4pp_l4y3r:(}
```