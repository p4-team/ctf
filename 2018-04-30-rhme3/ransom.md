# ransom, RE, 50pts

> In theory, this firmware mod was supposed to give you 30% extra horsepower and torque. In reality, it's something different.

> UPDATE: In reality... this challenge is easier than it should be. Consider it a bonus!
> See Random 2.0 for the real challenge.

In this task we got a binary to analyze. Upon flashing, the board
says the car was encrypted due to a ransomware:

```
Your car is taken hostage by REVENANTTOAD ransomware version DEBUG_a4fae86c.
To get your car back, send your user ID:
3835320719001400

and $1337 to the following rhme3coin address: 
[CENSORED].

Already paid? Then enter the received unlock code here:
```

We are supposed to type the decryption code. Either through
randomly mashing the keyboard, or analysis of the code, we notice
that only the first character of the password is checked. A quick
bruteforce should suffice:

```python
import serial, sys

s = serial.Serial("/dev/ttyUSB0", 115200, timeout = 2)
s.write("xxx\n")

for c in range("0123456789ABCDEF"):
    print s.read_until("here:")
    s.write(chr(c) + "\n")
```

After typing "2" we get the flag:

```
2
It was a pleasure doing business with you.
Your car is now unlocked.
Here is a bonus:
3f2bf3eb080475048eee8103a52e0ef8
Have a nice day!
```
