--------------------------------------
[Python Exploitation] Secret Accounts - 80 points
--------------------------------------

> Through many months of sniffing, we discovered a server running a software which the Club uses to manage information about secret bank accounts abroad. We even obtained its source code. We need to obtain access to the system in order to discover the real name of the owner of the account possessing the greater amount of money, in which bank it is, and the real amount. As you might expect, it seems that the Club has hunkered down to assert only authorized people, which really know what they are doing, are able to operate this system and to interpret information provided by it. Rumors exist that the Mentor himself manages it, as amazing as it may seem (he is old but not deciduous!).

> You will need good “python-fu” to win this challenge!

> Submit the flag in the following format: CTF-BR{info1_info2_info3}.

> Hint: Who is Fideleeto (Cuba!) in real life? Take this into account. :)

In this task we were given an obfuscated Python script and a server running it. Unfortunately I do no longer have the
original code, because I was deobfuscating it overwriting the file each time. It had a lot of octal numbers, some 
additions and multiplications just to hide the constants and so on.

We had to input password. Connecting the dots, we guessed that `master` (variable name) corresponds to description text's
Fideleeto, and birthyear is 1926, as per Wikipedia. We added some z's because the source code asked us for it.

After a couple of seconds, we were logged in. We were asked for option 1-4, but in reality our input was subtracted,
multiplied and generally messed with, so we simply brute forced the needed numbers. When we chose correct number, we 
were presented with a menu. The most interesting part of it was that our text was inputted via `input()`. Since
Python's `input()` is equivalent to `eval(raw_input())`, we had arbitrary code execution. We used it to write the file
with flag to stdout. Full exploit code is available in `doit.py`.
