## hsab (misc, 200)

In this task, we were given only an IP and port to connect to. After sending a simple proof of work,
we are immediately dropped into bash shell. Trying a couple of standard commands, such as `ls` or
`cat /etc/passwd` doesn't work - it said `ls: command not found`. Playing with it some more time, we
noticed `echo` actually did work, `echo xxx` actually printed `xxx`. Using `echo *`, `echo */*` and so on,
we could list all the files on the server. I did not save the output, but it was mostly normal Linux
stuff, `/etc` and similar. However, two things stood out. First, the only binaries in `/bin` were `bash`
itself and `server` - presumably the program managing the connection. Second, there was a file called
`/home/ctf/flag.ray`, probably containing the flag. However, without `cat` we could not easily read it.

Thankfully, most of the bash builtin commands were working. After quick look into `man bash`, we thought
`read` should work - `read xxx < flag.ray; echo $xxx` was the command we tried. Although it worked locally,
on the server it was syntax error - probably they disabled redirection, as `echo < /etc/passwd` errored too.

One more thing we tried, was running `bash flag.ray`. Trying it on local system with dummy flag, it outputed:
```
$ bash flag.ray 
flag.ray: line 1: DUMMY_FLAG: command not found
```
On the server, there was no output though. That meant it was probably a correct bash script. Finally, the
thing that worked was running `bash -v flag.ray` - or running bash in verbose mode. It turned out, that
the file contents were `#BCTF{ipreferzshtobash}` - commented flag.
