# We got paged out, mr president! (forensic, misc, 973p)

> We got some important data paged out.
> Can you recover it?

> pagefile.sys.gz

> Hints:

> The first key is named 'ct', the second one - 'fz'. Find out the remaining keys.

This was an exercise in good Linux-fu. The file we had was 1GB large, so impossible to search by hand. 
Given the hint, we could deduce though that there should be `ct` and `fz` strings somewhere.
Since `ct` is pretty common digraph (`action`, `direct`, and others), we decided to look for far rarer `fz`. Since this
was a Windows dump, we searched for UTF-16 strings. And... done:
```bash
λ strings -e l pagefile.sys | grep fz
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\ct\fz\one\{\r3g_\h4x\0r}
```

The flag is `ctfzone{r3g_h4x0r}`
