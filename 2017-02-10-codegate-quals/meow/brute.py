import hashlib
import string

charset = string.printable
sought = '9F46A92422658F61A80DDEE78E7DB914'.decode('hex')

for o1 in map(ord, charset):
    o3 = o1 ^ (0xa7 ^ 0xc3)
    o8 = o1 ^ (0x89 ^ 0xf5)
    o2 = o3 ^ (0x48 ^ 0x48)
    o5 = o2 ^ (0x55 ^ 0x0d)
    o9 = o3 ^ (0xe5 ^ 0xaf)
    o0 = o3 ^ o5 ^ o9 ^ (0x48 ^ 0x4d)
    
    v0 = chr(o0)
    v1 = chr(o1)
    v2 = chr(o2)
    v3 = chr(o3)
    v5 = chr(o5)
    v8 = chr(o8)
    v9 = chr(o9)

    for v4 in charset:
        for v6 in charset:
            for v7 in charset:
                passw = v0 + v1 + v2 + v3 + v4 + v5 + v6 + v7 + v8 + v9
                if hashlib.md5(passw).digest() == sought:
                    print passw
