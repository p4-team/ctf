# Advertisement (web, 96 solved, 66p)

```
This platform is under protection. DO NOT hack it.
```

This was supposed to be a `sanity flag`, but it actually took us more time to get this one, than some `real` challenges.
Fun part is that we noticed the `vulnerability` very fast, but we didn't realise it's the `attack vector`.

Once you log-in to the scoreboard you get an interesting cookie `uid` with value set to your `login`.
You can change it to something else, and it will be displayed on the page.

The goal of the challenge was to change it to something malicious - for example `xss` or `sqli` and in such case the page would display the flag:

`rwctf{SafeLine_1s_watch1ng_uuu}`
