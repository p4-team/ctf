v5 = [0] * 32
if 1:
  v5[0] = -25095;
  v5[1] = 1630;
  v5[2] = 15252;
  v5[3] = -1319;
  v5[4] = -15399;
  v5[5] = -494;
  v5[6] = -23173;
  v5[7] = -28535;
  v5[8] = 16303;
  v5[9] = -17615;
  v5[10] = 19629;
  v5[11] = 5141;
  v5[12] = 29901;
  v5[13] = -12534;
  v5[14] = 7393;
  v5[15] = -19110;
  v5[16] = 21702;
  v5[17] = -32129;
  v5[18] = 6045;
  v5[19] = 26329;
  v5[20] = -128;
  v5[21] = -32474;
  v5[22] = 21881;
  v5[23] = 19181;
  v5[24] = 24445;
  v5[25] = 17167;
  v5[26] = 12004;
  v5[27] = 4764;
  v5[28] = -9267;
  v5[29] = -5296;
  v5[30] = -29272;
  v5[31] = -16943;

def ror(x):
    return ((x >> 1) | (x << 15)) & 0xffff

def enc(key):
    r = ""
    for c in v5:
        c += 65536
        c &= 0xffff
        key = ror(key) ^ c
        r += chr(key & 0xff)

    return r

addr = [0] * 32
if 1:
  addr[0] =  0xE0908;
  addr[1] =  0xE0930;
  addr[2] =  0xE0958;
  addr[3] =  0xE0980;
  addr[4] =  0xE09A8;
  addr[5] =  0xE09A8;
  addr[6] =  0xE09A8;
  addr[7] =  0xE09D0;
  addr[8] =  0xE09F8;
  addr[9] =  0xE0A20;
  addr[10] = 0xE0A48;
  addr[11] = 0xE0A70;
  addr[12] = 0xE0A70;
  addr[13] = 0xE0A98;
  addr[14] = 0xE0AC0;
  addr[15] = 0xE0AE8;
  addr[16] = 0xE0B10;
  addr[17] = 0xE0B38;
  addr[18] = 0xE0B60;
  addr[19] = 0xE0B88;
  addr[20] = 0xE0BB0;
  addr[21] = 0xE0BD8;
  addr[22] = 0xE0C00;
  addr[23] = 0xE0C00;
  addr[24] = 0xE0C28;
  addr[25] = 0xE0C50;
  addr[26] = 0xE0C78;
  addr[27] = 0xE0CA0;
  addr[28] = 0xE0CC8;
  addr[29] = 0xE0C78;
  addr[30] = 0xE0CF0;
  addr[31] = 0xE0CF0;

data = open("all2", "rb").read()
result = [0] * 32

for i in range(32):
    exp = data[addr[i]:][:32]
    hi = None
    for key in range(65536):
        buf = enc(key)
        if buf == exp:
            hi = key >> 8
            hik = key
    hik ^= 0x6666
    if i / 8 == 0:
        assert hik % 123 == 0
        hik /= 123
    elif i / 8 == 1:
        hik -= 20384 + i % 8
    elif i / 8 == 2:
        hik ^= 0x73ab
    elif i / 8 == 3:
        hik -= 9981

    a = i / 8
    b = i % 8
    result[4 * b + a] = hik
    print hik, chr(hik), repr("".join(chr(c) for c in result))

