# Welcome (re, 96p, 49 solved)

In the challege we get a [virtual machine code](vo-interpreter.c) and a [flag checking program](welcome_task.voprotected.c) implemented on this VM.

We're lazy so before trying to analyse VM or at least translate the challege code to some assembly-like representation, we simply compiled this and run:

```
shalom@ubuntu:~/ctf/asis$ ./welcome 
Usage: program --left <num1> --right <num2>
```

We quickly check and it seems the values passed as parameters have to be 0-9, otherwise we get an error.
So there are only 100 options to check, not too much.
If we pass random values we get:

```
shalom@ubuntu:~/ctf/asis$ ./welcome --left 1 --right 2
flag iS n0t {thankS f0r participating aSiSctf2ol8}
Flag Flag Flag!
```

We simply run this in a loop with all possible parameter:
`python -c "[[__import__('os').system('echo %d %d;./welcome --left %d --right %d'%(left,right,left,right)) for left in range(10)] for right in range(10)]"`

And we get for example:
```
9 9
flag iS {vvelc0me_and_enj0y_aSiSctf20l8}
Flag Flag Flag!
```

And the flag is `ASIS{vvelc0me_and_enj0y_aSiSctf20l8}`
