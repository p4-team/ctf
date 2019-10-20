import struct
import pyflate
from io import BytesIO

import os
import pickle

if not os.path.isfile("./disasm.pickle"):
    f = open("./q.png", "rb")
    header = f.read(8)
    while True:
        length = f.read(4)
        length = struct.unpack(">I", length)[0]
        typ = f.read(4)
        data = f.read(length)
        crc = f.read(4)
        if b"IDAT" == typ:
            break

    #78 9C - Default Compression / last 4 bytes == CRC
    f = BytesIO(data[2:-4])
    (out, cmds) = pyflate.gzip_main(f)

    with open("./disasm.pickle", "wb") as f:
        pickle.dump(cmds, f)
    #print("Commands written")
else:
    with open("./disasm.pickle", "rb") as f:
        cmds = pickle.load(f)
    #print("Commands loaded from file")


bytes_written = 0
row_size = 0xffffffff + 1 + 1
for entry in cmds:
    (count, cmd) = entry
    opcode = cmd[0]


    print("{: 8} {}".format( count, ' '.join(map(str, cmd))))

    # ADDB byte
    if opcode == "ADDB":
        bytes_written += count * 1
    # ADDL len
    elif opcode == "ADDL":
        bytes_written += count * cmd[1]
    # ADDL distance length
    elif opcode == "ADDO":
        bytes_written += count * cmd[2]

print("Total bytes: {0} /  {0:x}".format(bytes_written))
print("Total size: {:.1f}MiB".format(bytes_written/1024/1024))
print("Total size: {:.1f}Mb".format(bytes_written * 8 / 1024 / 1024))

