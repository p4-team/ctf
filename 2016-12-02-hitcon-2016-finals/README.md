# Writeup HITCON CTF 2016 Finals

Team: msm, akrasuski1, rev, shalom

### Remarks

HITCON Finals are Attack-Defense, so there are no tasks suitable for a writeup.
Nevertheless, when preparing for this event we were looking for some information about what to expect, and sadly there was little to be found.
So for some future generations:

* Event took 2 days, about 8h each, with a break for the night in between.
* There were pwn and web tasks.
* Initially everyone started with 1 pwn and 1 web, and then tasks were being added. Pwn services were stacking, so in the end there were 3 services to work with. Web services were removed after some time.
* There were significant bonus points for first blood.
* Pcap files from our network gateway were available on ftp after ~15 minutes.
* We did not have root access to the game servers, and the privileges we had allowed only for deploying the applications and in case of pwn also to patch it. In case of web you have to exploit the application to be able to patch it (or in some cases just drop a shell to directory where it's going to deploy).
