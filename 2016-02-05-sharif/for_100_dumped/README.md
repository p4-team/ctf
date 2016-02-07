## Dumped (Forensics, 100p)

    In Windows Task Manager, I right clicked a process and selected "Create dump file". I'll give you the dump, but in return, give me the flag!

    Download RunMe.DMP.xz

###ENG
[PL](#pl-version)

Running `strings RunMe.DMP | grep Sharif` against this file gives us flag.

###PL version

Wystarczy użyć `strings RunMe.DMP | grep Sharif`.
