import codecs
import os
from Crypto.Util.number import long_to_bytes


def asm(code):
    code = code.replace("end", "")
    payload = """(module
  (func $dupa (result i32)
%s
  )
  (export "dupa" (func $dupa)))

""" % code
    with codecs.open("code.wat", "w") as out_file:
        out_file.write(payload)
    os.system("~/ctf/hitcon/wabt/bin/wat2wasm code.wat")
    with codecs.open("code.wasm", "rb") as in_file:
        data = in_file.read()
        res = data[0x22:]
        os.system("rm code.wat")
        os.system("rm code.wasm")
        return res


def dis(code):
    size = long_to_bytes(len(code)+1).encode("hex")
    size2 = long_to_bytes(len(code)+3).encode("hex")
    prefix = ('0061736d010000000105016000017f03020100070801046475706100000a'+size2+'01'+size+'00').decode(
        "hex")
    with codecs.open("code.wasm", "wb") as out_file:
        out_file.write(prefix + code)
    os.system("~/ctf/hitcon/wabt/bin/wasm2wat code.wasm > code.wat")
    with codecs.open("code.wat", "r") as in_file:
        data = in_file.read()[79:-30] + "\nend"
        data = data.replace("    ", "")
        return data


def eval(code):
    code = code.replace("end", "")
    payload = """(module
      (func $dupa (result i32)
    %s                                                                                                                                  
      )
      (export "dupa" (func $dupa)))
    """ % code
    with codecs.open("code.wat", "w") as out_file:
        out_file.write(payload)
    os.system("~/ctf/hitcon/wabt/bin/wat2wasm code.wat")
    os.system("~/ctf/hitcon/wabt/bin/wasm-interp code.wasm --run-all-exports > res.txt")
    with codecs.open('res.txt', 'r') as result_file:
        res = result_file.read()
        os.system("rm code.wasm")
        result = int(res[14:])
        if result >= 2**31:
            return result-2**32
        else:
            return result


def main():
    code = """i32.const 62537
i32.const 17488
i32.mul
i32.const 5345
i32.const 12820
i32.const 7342
i32.mul
i32.sub
i32.const 18
i32.const 40931
i32.sub
i32.const 36779
i32.add
i32.and
i32.const 19653
i32.xor
i32.const 18762
i32.const 61387
i32.sub
i32.const 28802
i32.and
i32.const 10760
i32.and
i32.const 64150
i32.const 31717
i32.add
i32.and
i32.xor
i32.or
i32.const 15746
i32.const 34874
i32.add
i32.const 60927
i32.sub
i32.const 12311
i32.xor
i32.or
i32.const 42983
i32.or
return
end
"""
    # s = asm(code)
    # print(s.encode("hex"))
    # print(dis(s))
    data = "41f3800141fe87036a41a52a41ce8d0241fe98036c41eac1006c6a7341d9f801734180f30241becc026b724183f900419294036b41cf8d016a41ddce0041d2ac0341a4e3036c6a41aac40241a8d0016c6a41e585037173720f0b".decode(
        "hex")
    print(dis(data))
    print(eval(dis(data)))

# main()
