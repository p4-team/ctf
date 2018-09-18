# Ocean of sockets (forensics, 200p)

In the task we get a binary which I think was packed with UPX, but with renamed sections.
Once you fix those, you can unpack it via UPX and get [binary](OceanOfSockets.exe).
This is actually pyinstaller executable, so we can unpack this using https://github.com/countercept/python-exe-unpacker and we finally get the [real code](oceanOfSockets.py).

This code doesn't seem very interesting, it just sends GET requests to host we provide.
The only interesting part is the cookie: `%|r%uL5bbA0F?5bC0E9b0_4b2?N`

If we XOR this cookie with known flag format `TMCTF{` we get back `713131713337` when hexencode the data.
This doesn't seem very random, but XOR was a wrong approach here.
If we try to see how much the characters in the cookie differ from the flag format: 

```python
    s = '%|r%uL5bbA0F?5bC0E9b0_4b2?N'
    for c in zip(s, "TMCTF{"):
        print(ord(c[0]) - ord(c[1]))
```

We get either 47 or -47.
This means we've got a Caesar with shift of 47.
It's wrapping around at ` ` so we can just do:

```python
    for character in cookie:
        number = ord(character)
        if number - 47 < ord(' '):
            number += 47
        else:
            number -= 47
        result += chr(number)
    print(result)
```

And we get `TMCTF{d33p_und3r_th3_0c3an}`
