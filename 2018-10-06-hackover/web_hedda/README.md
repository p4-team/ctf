# Ez web (web, 100p, 97 solved)

A second trivial web task.
As previously we check for `robots.txt` and again there is:

```
User-agent: *
Disallow: /flag/
```

And in the directory there is `flag.txt`.
The link is actually broken, but we can fix the name by hand.

Once we get there it says: `You are using the wrong browser, 'Builder browser 1.0.1' is required`.

If we set User-agent to this string we get: `You are refered from the wrong location hackover.18 would be the correct place to come from.`

And if we set Referer to this string we get: `aGFja292ZXIxOHs0bmdyeVczYlMzcnYzclM0eXNOMH0=` which decoded as base64 string gives `hackover18{4ngryW3bS3rv3rS4ysN0}`
