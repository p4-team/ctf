## Image Archeology (Admin, 350)

> We have found the file, which contains a part of gai. But where is it?
> Hints
> You don't need any special reverse skills to solve this. It will be enough to use strings
> to reveal how the flag can be found.

In this task, we received an image of a small disk. After mounting it, we found an usual Unix folder (/bin and so on).
Even without the hint, we searched for unusual things in it:
```
find . -type f -exec bash -c "strings {} | grep -E volga\|Volga && echo {}" \;
hacker.volga.ctf
./bin/busybox2
hacker.volga.ctf
./core
strings: ./usr/bin/sudo: Permission denied
strings: ./usr/sbin/visudo: Permission denied
```
Well, it's unlikely that untampered system would have such strings, so we quickly looked into `busybox2` executable.
When ran, it didn't do much - it returned into prompt immediately. However, after a couple of seconds, our system 
restarted... After a close look, we noticed the executable contained string `/sbin/reboot`. We patched it, so it will call
`/bin/ls` instead (a crude patch, but it worked). 

The code itself was not very hard - it was:
- xoring stuff
- taking two `rand()`s without any `srand()` before and interpreting the results as a date
- sending something to `hacker.volga.ctf` (host unavailable)
- forking, and rebooting in one child

Well, we did not waste our time reversing the code any further - we simply stepped through the code in debugger
and break when the connection was made to the aforementioned site. It turns out, that the flag was in memory at that
time.
