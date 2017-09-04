# Private Local Comment (ppc)


In this PPC task we have 3 levels of Python challenges where we need to extract some data in unusual way.
There is sandbox around all of the tasks so we can't spawn a shell or do anything like that, we need to use legit python code.

### Private 

Here we have code:

```python
import sys
from restrict import Restrict

r = Restrict()
# r.set_timeout()

class Private:
    def __init__(self):
        pass

    def __flag(self):
        return "TWCTF{CENSORED}"

p = Private()
Private = None

d = sys.stdin.read()
assert d is not None
assert "Private" not in d, "Private found!"
d = d[:24]

r.seccomp()

print eval(d)
```

So we have only instance of the class and we need to call a private method to get the flag.
This is trivial for anyone who knows python at least a little bit, or know how to use `dir()`.
In Python there is no such thing as "private" really, the prefix `__` only causes the interpreter to rewrite the method name to `classname__methodname` so in our case `Private__flag`.
There is still the second check, so we can't use `Private` in our input and we have only 24 character to use, so we can't play around with extracting the class name from object.

As I mentioned, the `dir()` functions is useful here, it returns list of fields and methods of the objects, and in our case `dir(p)[0]` will return the name of method we want.
Now we need some reflection to call the method from the string name, and we can use `getattr` for this.
The solution finally is: `getattr(p,dir(p)[0])()` and we get flag `TWCTF{__private is not private}`

### Local

This time we get:

```python
import sys
from restrict import Restrict

r = Restrict()
# r.set_timeout()

def get_flag(x):
    flag = "TWCTF{CENSORED}"
    return x

d = sys.stdin.read()
assert d is not None
d = d[:30]

r.seccomp()

print eval(d)
```

This time we need to extract value of local variable defined in a function.
People with some experience in refection in python will know that you can actually construct functions in the code just like any objects, and you can also decostruct them, because they are simply objects like any other.
Each function has property `func_code` which contains details about the code of the function.
There we can find `co_const` property, which stores list of constant used in the function, just like our flag.

So we can simply send: `get_flag.func_code.co_consts` to recover the flag ` TWCTF{func_code is useful for metaprogramming}`

### Comment

In the last taks we have code:

```python
import sys
from restrict import Restrict

r = Restrict()
# r.set_timeout()

d = sys.stdin.read()
assert d is not None
d = d[:20]

import comment_flag
r.seccomp()

print eval(d)
```

and the imported `comment_flag` module is:

```python
'''
Welcome to unreadable area!
FLAG is TWCTF{CENSORED}
'''
```

The trick here is that the comment defined at the very top of the module is actually treated by python as module documentation docstring.
As such it can be accessed via `__doc__` property of the module, so by sending `comment_flag.__doc__` we can recover the last flag: `TWCTF{very simple docstring}`
