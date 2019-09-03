import random
import struct
import sys
from typing import List


# for (j = 0LL; j != 64; j += 8LL)
# {
#     v736[j + 0] = (((((((v735[j] * pubkey_part[128] % 0xFFFFFFFB + v735[j + 1] * pubkey_part[136]) % 0xFFFFFFFB + v735[j + 2] * pubkey_part[144]) % 0xFFFFFFFB + v735[j + 3] * pubkey_part[152]) % 0xFFFFFFFB + v735[j + 4] * pubkey_part[160]) % 0xFFFFFFFB + v735[j + 5] * pubkey_part[168]) % 0xFFFFFFFB + v735[j + 6] * pubkey_part[176]) % 0xFFFFFFFB + v735[j + 7] * pubkey_part[184]) % 0xFFFFFFFB;
#     v736[j + 1] = (((((((v735[j] * pubkey_part[129] % 0xFFFFFFFB + v735[j + 1] * pubkey_part[137]) % 0xFFFFFFFB + v735[j + 2] * pubkey_part[145]) % 0xFFFFFFFB + v735[j + 3] * pubkey_part[153]) % 0xFFFFFFFB + v735[j + 4] * pubkey_part[161]) % 0xFFFFFFFB + v735[j + 5] * pubkey_part[169]) % 0xFFFFFFFB + v735[j + 6] * pubkey_part[177]) % 0xFFFFFFFB + v735[j + 7] * pubkey_part[185]) % 0xFFFFFFFB;
#     v736[j + 2] = (((((((v735[j] * pubkey_part[130] % 0xFFFFFFFB + v735[j + 1] * pubkey_part[138]) % 0xFFFFFFFB + v735[j + 2] * pubkey_part[146]) % 0xFFFFFFFB + v735[j + 3] * pubkey_part[154]) % 0xFFFFFFFB + v735[j + 4] * pubkey_part[162]) % 0xFFFFFFFB + v735[j + 5] * pubkey_part[170]) % 0xFFFFFFFB + v735[j + 6] * pubkey_part[178]) % 0xFFFFFFFB + v735[j + 7] * pubkey_part[186]) % 0xFFFFFFFB;
#     v736[j + 3] = (((((((v735[j] * pubkey_part[131] % 0xFFFFFFFB + v735[j + 1] * pubkey_part[139]) % 0xFFFFFFFB + v735[j + 2] * pubkey_part[147]) % 0xFFFFFFFB + v735[j + 3] * pubkey_part[155]) % 0xFFFFFFFB + v735[j + 4] * pubkey_part[163]) % 0xFFFFFFFB + v735[j + 5] * pubkey_part[171]) % 0xFFFFFFFB + v735[j + 6] * pubkey_part[179]) % 0xFFFFFFFB + v735[j + 7] * pubkey_part[187]) % 0xFFFFFFFB;
#     v736[j + 4] = (((((((v735[j] * pubkey_part[132] % 0xFFFFFFFB + v735[j + 1] * pubkey_part[140]) % 0xFFFFFFFB + v735[j + 2] * pubkey_part[148]) % 0xFFFFFFFB + v735[j + 3] * pubkey_part[156]) % 0xFFFFFFFB + v735[j + 4] * pubkey_part[164]) % 0xFFFFFFFB + v735[j + 5] * pubkey_part[172]) % 0xFFFFFFFB + v735[j + 6] * pubkey_part[180]) % 0xFFFFFFFB + v735[j + 7] * pubkey_part[188]) % 0xFFFFFFFB;
#     v736[j + 5] = (((((((v735[j] * pubkey_part[133] % 0xFFFFFFFB + v735[j + 1] * pubkey_part[141]) % 0xFFFFFFFB + v735[j + 2] * pubkey_part[149]) % 0xFFFFFFFB + v735[j + 3] * pubkey_part[157]) % 0xFFFFFFFB + v735[j + 4] * pubkey_part[165]) % 0xFFFFFFFB + v735[j + 5] * pubkey_part[173]) % 0xFFFFFFFB + v735[j + 6] * pubkey_part[181]) % 0xFFFFFFFB + v735[j + 7] * pubkey_part[189]) % 0xFFFFFFFB;
#     v736[j + 6] = (((((((v735[j] * pubkey_part[134] % 0xFFFFFFFB + v735[j + 1] * pubkey_part[142]) % 0xFFFFFFFB + v735[j + 2] * pubkey_part[150]) % 0xFFFFFFFB + v735[j + 3] * pubkey_part[158]) % 0xFFFFFFFB + v735[j + 4] * pubkey_part[166]) % 0xFFFFFFFB + v735[j + 5] * pubkey_part[174]) % 0xFFFFFFFB + v735[j + 6] * pubkey_part[182]) % 0xFFFFFFFB + v735[j + 7] * pubkey_part[190]) % 0xFFFFFFFB;
#     v736[j + 7] = (((((((v735[j] * pubkey_part[135] % 0xFFFFFFFB + v735[j + 1] * pubkey_part[143]) % 0xFFFFFFFB + v735[j + 2] * pubkey_part[151]) % 0xFFFFFFFB + v735[j + 3] * pubkey_part[159]) % 0xFFFFFFFB + v735[j + 4] * pubkey_part[167]) % 0xFFFFFFFB + v735[j + 5] * pubkey_part[175]) % 0xFFFFFFFB + v735[j + 6] * pubkey_part[183]) % 0xFFFFFFFB + v735[j + 7] * pubkey_part[191]) % 0xFFFFFFFB;
# }
def matrix_mult(data: List[int], key: List[int]) -> List[int]:
    result = []
    for j in range(8):
        for i in range(8):
            val = 0
            for k in range(8):
                val = (val + (data[j * 8 + k] * key[k * 8 + i])) % 0xFFFFFFFB
            result.append(val)
    return result


# for (k = 0LL; k != 64; k += 8LL)
# {
#     v735[k + 128] = (v735[k + 192] + v736[k + 0]) % 0xFFFFFFFB;
#     v735[k + 129] = (v735[k + 193] + v736[k + 1]) % 0xFFFFFFFB;
#     v735[k + 130] = (v735[k + 194] + v736[k + 2]) % 0xFFFFFFFB;
#     v735[k + 131] = (v735[k + 195] + v736[k + 3]) % 0xFFFFFFFB;
#     v735[k + 132] = (v735[k + 196] + v736[k + 4]) % 0xFFFFFFFB;
#     v735[k + 133] = (v735[k + 197] + v736[k + 5]) % 0xFFFFFFFB;
#     v735[k + 134] = (v735[k + 198] + v736[k + 6]) % 0xFFFFFFFB;
#     v735[k + 135] = (v735[k + 199] + v736[k + 7]) % 0xFFFFFFFB;
# }
def add_rows(fst: List[int], snd: List[int]) -> List[int]:
    result = []
    for i in range(64):
        result.append((fst[i] + snd[i]) % 0xFFFFFFFB)
    return result


def sub_rows(fst: List[int], snd: List[int]) -> List[int]:
    result = []
    for i in range(64):
        result.append((fst[i] - snd[i]) % 0xFFFFFFFB)
    return result


# for (m = 0LL; m != 64; m += 8LL)
# {
#     v737[m + 0] = v736[((m + 0) & 7) + 8LL * ((m + 0) >> 3)];
#     v737[m + 1] = v736[((m + 1) & 7) + 8LL * ((m + 1) >> 3)];
#     v737[m + 2] = v736[((m + 2) & 7) + 8LL * ((m + 2) >> 3)];
#     v737[m + 3] = v736[((m + 3) & 7) + 8LL * ((m + 3) >> 3)];
#     v737[m + 4] = v736[((m + 4) & 7) + 8LL * ((m + 4) >> 3)];
#     v737[m + 5] = v736[((m + 5) & 7) + 8LL * ((m + 5) >> 3)];
#     v737[m + 6] = v736[((m + 6) & 7) + 8LL * ((m + 6) >> 3)];
#     v737[m + 7] = v736[((m + 7) & 7) + 8LL * ((m + 7) >> 3)];
# }
def transpose(data: List[int]) -> List[int]:
    result = []
    for i in range(64):
        result.append(data[(i & 7) + 8 * (i >> 3)])
    return result


def chunks(data: bytes, n: int) -> List[bytes]:
    return [data[i * n:(i + 1) * n] for i in range(len(data) // n)]


def uint32(val: bytes) -> int:
    return struct.unpack('<I', val)[0]


def puint32(val: bytes) -> int:
    return struct.pack('<I', val)


def get_random_vectors() -> List[int]:
    return [random.randint(0, 0xFFFFFFFB - 1) for i in range(64)]


def parse_vectors(data: bytes) -> List[int]:
    assert len(data) == 256
    result = []
    for chunk in chunks(data, 4):
        result.append(uint32(chunk))
    return result


def serialise_vectors8(vectors: List[int]) -> bytes:
    assert len(vectors) == 64
    out = b''
    for vec in vectors:
        out += bytes([vec])
    return out


def serialise_vectors32(vectors: List[int]) -> bytes:
    assert len(vectors) == 64
    out = b''
    for vec in vectors:
        out += puint32(vec)
    return out


def deserialise_vectors8(raw_vectors: bytes) -> List[int]:
    assert len(raw_vectors) == 64
    result = []
    for vec in raw_vectors:
        result.append(vec)
    return result


def negate(vectors: List[int]) -> List[int]:
    return [(-v) % 0xFFFFFFFB for v in vectors]


def decrypt(ct_file: str, pk_file: str, result_file: str) -> None:
    with open(ct_file, 'rb') as ctf:
        ct = ctf.read()
        data0 = parse_vectors(ct[0:256])
        data1 = parse_vectors(ct[256:512])
        data2 = parse_vectors(ct[512:768])

    print("stage0", data0)
    print("stage1", data1)
    print("combined", data2)

    with open(pk_file, 'rb') as pkf:
        pk = pkf.read()
        privkey = parse_vectors(pk)

    tarnacja1 = matrix_mult(privkey, privkey)
    tarnacja2 = matrix_mult(data0, tarnacja1)
    tarnacja3 = matrix_mult(data1, privkey)

    tarnacja4 = add_rows(tarnacja2, tarnacja3)
    tarnacja5 = add_rows(data2, tarnacja4)

    result = transpose(tarnacja5)
    rawdata = serialise_vectors8(result)

    with open(result_file, 'wb') as outf:
        outf.write(rawdata)


def encrypt(pt_file: str, pk_file: str, result_file: str) -> None:
    with open(pt_file, 'rb') as ctf:
        pt = ctf.read()
        pt = (pt + b'\x00' * (0x40 - len(pt)))[:0x40]
        pt = deserialise_vectors8(pt)

    with open(pk_file, 'rb') as pkf:
        pk = pkf.read()
        pk0 = parse_vectors(pk[0:256])
        pk1 = parse_vectors(pk[256:512])
        pk2 = parse_vectors(pk[512:768])

    seed = get_random_vectors()
    stage0 = matrix_mult(seed, pk0)
    stage1 = matrix_mult(seed, pk1)
    stage2 = matrix_mult(seed, pk2)
    combined = add_rows(stage2, pt)

    print('pt =', pt)
    print('seed =', seed)
    print('stage0 =', stage0)
    print('pk0 =', pk0)
    print('pk1 =', pk1)
    print('pk2 =', pk2)
    print('stage1 =', stage1)
    print('stage2 =', stage2)
    print('combined =', combined)

    result = b''
    result += serialise_vectors32(stage0)
    result += serialise_vectors32(stage1)
    result += serialise_vectors32(combined)

    with open(result_file, 'wb') as outf:
        outf.write(result)


def gen_keys(pub_file: str, priv_file: str) -> None:
    pk0 = get_random_vectors()  # pubkey_part[0..64]
    pk1 = get_random_vectors()  # pubkey_part[64..128]

    for i in range(4):
        r0 = random.randint(0, 0xFFFFFFFB - 1)
        r1 = random.randint(0, 0xFFFFFFFB - 1)

        for j in range(8):
            pk0[32 + i * 8 + j] = (pk0[32 + i * 8 + j] + r0 * pk0[i * 8 + j]) % 0xFFFFFFFB
            pk1[32 + i * 8 + j] = (pk1[32 + i * 8 + j] + r1 * pk1[i * 8 + j]) % 0xFFFFFFFB

    privkey = get_random_vectors()  # private_key[0..64]
    priv_square = matrix_mult(privkey, privkey)  # v735[0..64]

    pk0_mult2 = matrix_mult(negate(pk0), priv_square)  # v735[192..256]
    pk1_mult = matrix_mult(negate(pk1), privkey)  # v735[192..256]

    pk2 = add_rows(pk0_mult2, pk1_mult)

    with open(pub_file, 'wb') as outf:
        pub_result = b''
        pub_result += serialise_vectors32(pk0)
        pub_result += serialise_vectors32(pk1)
        pub_result += serialise_vectors32(pk2)
        outf.write(pub_result)

    with open(priv_file, 'wb') as outf:
        priv_result = serialise_vectors32(privkey)
        outf.write(priv_result)


def main():
    if sys.argv[1] == 'encrypt':
        encrypt(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == 'decrypt':
        decrypt(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == 'keygen':
        gen_keys(sys.argv[2], sys.argv[3])


if __name__ == '__main__':
    main()


def dump():
    with open("C:\\Users\\PC\\Desktop\\twctf\\m-poly-cipher\\flag.enc", 'rb') as ctf:
        ct = ctf.read()
        data0 = parse_vectors(ct[0:256])
        data1 = parse_vectors(ct[256:512])
        data2 = parse_vectors(ct[512:768])

    print("stage0 = ", data0)
    print("stage1 = ", data1)
    print("combined =", data2)
