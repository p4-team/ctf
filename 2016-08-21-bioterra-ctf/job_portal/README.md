# Job Portal (200, Web/Exploit)

> They pretend to check your letter of application. 
> I want to proof that they are doing nothing to help you. Get me access to the filesystem!

In this task we were given access to service allowing to upload tar files. When uploaded, we could check the
tarball contents (file names only) on separate page. The URL extension was `.cgi`, which hinted at possible
shell injection. Indeed, when we submitted tar with one file called `name; cat /etc/passwd`, we could read directory 
contents listed on the website. Getting the flag from there was just a matter of `cat`ting it.
