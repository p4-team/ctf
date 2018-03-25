# Special (Pwn)

A classic restricted shell jailbreak task.
We can ssh to a server and we get access via some kind of restricted shell.
It's all blackbox, so we need to poke around a bit to figure out what we can and can't do.

We get only messages from stderr, which makes things a bit harder.
Sending some random payloads tells us that our commands are executed via `bash -c "cmd"`.
There is also some input filtration applied.

We can send as command `$PWD` which shows error `bash: /home/special: Is a directory`.
This is very useful, because we can send for example `$PWDabcdefg....` and in the error log we get back the string without the filtrated characters.
From this we know that we can use `{}|;:<>$'#^_+-` and all uppercase letters.

Next we proceed with testing bash special variables, and from this we get an interesting result for `$_`:

```
declare -x A="T"
declare -x AB="HI"
declare -x ABC="ISN"
declare -x ABCD="OTTH"
declare -x ABCDE="EFLAG"
declare -x ABCDEF="BUTMAY"
declare -x ABCDEFG="BEITCAN"
declare -x ABCDEFGH="HELPGETT"
declare -x ABCDEFGHI="INGFLAG:D"
declare -x OLDPWD
declare -x PWD="/home/special"
declare -x SHELL=""
declare -x SHLVL="1"
declare -x _="export"
```

Now what we want to do, is to create some meanigful command.
Sadly we don't have `()` so we can't do any `calculations` and therefore create numbers.
The intended solution was to use `${#variable_name}` to get length of the variable, and thus get some numbers, but we didn't know that...

What we can do is to use `${variable:K:N}` which is a substring from index `K` with length `N`.
We have only `$SHLVL` which has value `1` and `$#` with value `0`, and with those we can get:

```
slash -> ${PWD::$SHLVL}
h -> ${-::$SHLVL}
a -> ${PWD:$SHLVL$SHLVL:$SHLVL}
i -> ${PWD:$SHLVL$#:$SHLVL}
e -> ${_:$#:$SHLVL}
x -> ${_:$SHLVL:$SHLVL}
```

Again, the intended solution was to get `s` and `h` and spawn a shell, but we didn't have `s`.
Fortunately we figured out that we can run `ex` command, which spawns `vim`!

From `vim` we can simply run `:!sh` to spawn a shell, and read the flag: `Flag{B4sh_subst1tut1on_is_gud!}`
