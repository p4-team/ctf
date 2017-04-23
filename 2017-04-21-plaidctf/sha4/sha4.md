#Sha4 (web, 300pts, 16 solves)

> tl;dr
> local file read, race condition, hash collision, template injection

![scr1](scr1.png)


Start off by noticing that we have a local file read via the second form:

![scr2](scr2.png)

Lets find out where the application root is: `etc/apache2/sites-enabled/000-default.conf`

```
<VirtualHost *:80>
	ServerName sha4

	WSGIDaemonProcess sha4 user=www-data group=www-data threads=8 request-timeout=10
	WSGIScriptAlias / /var/www/sha4/sha4.wsgi

	
    <directory /var/www/sha4>
		WSGIProcessGroup sha4
		WSGIApplicationGroup %{GLOBAL}
		WSGIScriptReloading On
		Order deny,allow
		Allow from all
	</directory>

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined


</VirtualHost>
```

Great!


[file:////var/www/sha4/server.py](server.py)

[file:////var/www/sha4/sha4.py](sha4.py)



``` python
  out_text = str(decode(ber))
  open(f, "w").write(out_text)

  if is_unsafe(out_text):
    return render_template_string(unsafe)

  commentt = comment % open(f).read()
  return render_template_string(commentt, comment=out_text.replace("\n","<br/>"))
```

Is vulnerable to race condition and template injection.
We can first send a valid input that passes the `is_unsafe` and a malicious input that injects the template while `is_unsafe` is running with the valid input.

But in order to do that we need 2 different inputs that produce the same `hash`:

``` python
def hash(x):
  h0 = "SHA4_IS_"
  h1 = "DA_BEST!"
  keys = unpad(x)
  for key in keys:
    h0 = DES.new(key).encrypt(h0)
    h1 = DES.new(key).encrypt(h1)
  return h0+h1
```


`unpad` function works as expected, it takes 7 8-bit bytes and output 8 7-bit bytes, pic rel:

![scr3](scr3.png)

DES.encrypt was the problem, as it ignores the lsb. So we could perform bitflips to bypass the whitelist.


After generating a valid input pair we simply smash them agains the server and hope to get the flag via a usuall template injection.

[full script](script.py)