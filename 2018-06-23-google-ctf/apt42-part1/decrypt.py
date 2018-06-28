import struct

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def xor_qword(chunk, qword):
    dword = struct.pack("<I", qword >> 32)

    out = ''
    for a, b in zip(map(ord, chunk), map(ord, dword)):
        out += chr(a^b)
    return out


init_data = 0xD806209B3D160872
round_data = 0x5851F42D4C957F2D
data = '49AB407E86FAA237'.decode('hex')

decoded_chunks = []

for chunk in list(chunks(data, 4))[::-1]:
    init_data = (init_data * round_data + 1) & 0xffffffffffffffff
    d = xor_qword(chunk, init_data)
    decoded_chunks.append(d)

decoded_text = ''.join(decoded_chunks[::-1])
print(repr(decoded_text))