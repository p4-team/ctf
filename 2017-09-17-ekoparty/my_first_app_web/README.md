# My First App (Web, 399p, 62 solved)

Honestly we're not exactly sure what was the idea behind this task.
We get a link to a webapplication which says:

```
After much research, I've found on stackoverflow.com how to protect my framework app.
```

And there is a link to `/getflag`, but there is a password prompt when we try to go there.
It seems the authentication is based on some regex rather than on directory structure since going to `/getflags` also gives us authentication prompt and not 404 error.
Additionally we can see that going to `/index.php` and `/index.php/` gives us the same results.

This all suggests some mod_rewrite magic underneath.
We simply tried to see what will happen if we do `/index.php/getflag`, which would depend on the regex rules order, and we got the flag:

`EKO{fucking_m0d_r3wr1t3}`
