# Malbolge (Web, 238p, 153 solved)

We can connect to a service which asks us for a Malbolge code which will print `Welcome to EKOPARTY!`:

```
$ nc6 malbolge.ctf.site 40111
nc6: using stream socket
Send a malbolge code that print: 'Welcome to EKOPARTY!' (without single quotes)
```

A bit of googling and we find http://www.matthias-ernst.eu/malbolge.html where author created [a program](finder.c) for generating Malbolge programs printing out desired output.
We used it and got:

```
bCBA@?>=<;:9876543210/.-,+*)('&%$#"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]\[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9y765432+O/.-,+*)i'&}C{"!~w={zyxwYutsrqponmlkjiha'Hdcba`_^]\[ZYXWVUTSRQPONMLKJIHGFED=a;@?>7[|:981U543s10/.',+*#G'&%$#"!~`|u;yxqvun4rqpRhmf,Mchgfedcba`_^]VzZYXWVUTSRQJnNM/KDIBfFEDCBA#?>=<54X810T4321q/.-,+$H('&%$#"bx>|{tyxwvutsrqponmlkd*Kafedc\"m
```

Which in turn gave us the flag: `EKO{0nly4nother3soteric1anguage}`
