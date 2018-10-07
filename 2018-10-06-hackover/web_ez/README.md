# Ez web (web, 100p, 185 solved)

A very simple web challenge.
The site says it's under construction and there is not much there, but if we check `robots.txt` we can see:

```
User-agent: *
Disallow: /flag/
```

And in `flag` directory there is `flag.txt` but it says we're not allowed to see it.
However if we look at the network communication, there is a cookie `isAllowed` sent by the webpage, set to `false`.
If we set it to true we can see the flag: `hackover18{W3llD0n3,K1d.Th4tSh0tw4s1InAM1ll10n}`
