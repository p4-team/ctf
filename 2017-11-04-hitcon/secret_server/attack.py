import base64
import hashlib
import re
import string

import itertools

from crypto_commons.netcat.netcat_commons import receive_until_match, nc, send, receive_until
from crypto_commons.symmetrical.symmetrical import set_byte_cbc, set_cbc_payload_for_block


def PoW(suffix, digest):
    for prefix in itertools.product(string.ascii_letters + string.digits, repeat=4):
        p = "".join(prefix)
        if hashlib.sha256(p + suffix).hexdigest() == digest:
            return p


def pad(msg):
    pad_length = 16 - len(msg) % 16
    return msg + chr(pad_length) * pad_length


def generate_payload_from_message(encrypted, plaintext, new_payload):
    raw = encrypted.decode("base64")
    new_payload = pad(new_payload)[:16]
    plaintext = ("\0" * 16) + (pad(plaintext)[:16])
    payload = set_cbc_payload_for_block(raw, plaintext, new_payload, 1)
    return base64.b64encode(payload)


def main():
    s = nc("52.193.157.19", 9999)
    data = receive_until_match(s, "Give me XXXX:")
    inputs = re.findall("SHA256\(XXXX\+(.*)\) == (.*)", data)[0]
    suffix = inputs[0]
    digest = inputs[1]
    result = PoW(suffix, digest)
    print("PoW done")
    send(s, result)
    receive_until_match(s, "Done!\n")
    welcome = receive_until(s, "\n")[:-1]
    get_flag_payload = generate_payload_from_message(welcome, "Welcome!", "get-flag")
    send(s, get_flag_payload)
    encrypted_flag = receive_until(s, "\n")[:-1]
    raw_enc_flag = encrypted_flag.decode("base64")
    current = "hitcon{"
    print('encrypted flag', encrypted_flag, encrypted_flag.decode("base64"), len(encrypted_flag.decode("base64")))
    for block_to_recover in range(3):
        malleable_block = base64.b64encode(raw_enc_flag[block_to_recover * 16:])
        missing = 16 - len(current)
        for spaces in range(missing):
            for c in string.printable:
                test_flag_block_prefix = current + c + ("\0" * (missing - spaces))
                expected_command = (" " * spaces) + "get-flag"
                payload = generate_payload_from_message(malleable_block, test_flag_block_prefix, expected_command)
                send(s, payload)
                result = receive_until(s, "\n")[:-1]
                if result == encrypted_flag:
                    current += c
                    print('found matching flag char:', current)
                    break
        print(current)
        known_blocks = raw_enc_flag[16 * block_to_recover:16 * block_to_recover + 32]
        expanded_flag = raw_enc_flag[16 * block_to_recover:] + known_blocks  # appending IV and "Welcome!!" at the end
        next_block_known = ""
        for i in range(8):
            get_md5 = set_cbc_payload_for_block(expanded_flag, "\0" * 16 + current, (" " * 9) + "get-md5", 1) # first block is get-md5
            get_md5 = set_byte_cbc(get_md5, ("\0" * (5 - block_to_recover) * 16) + current,
                                   (6 - block_to_recover) * 16 - 1, chr((4 - block_to_recover) * 16 - i - 1)) # last character to cut padding
            send(s, base64.b64encode(get_md5))
            real_md5_result = receive_until(s, "\n")[:-1]
            for c in string.printable:
                test_md5_payload = set_cbc_payload_for_block(expanded_flag, "\0" * 16 + current,
                                                             (" " * (8 - i - 1)) + "get-md5" + next_block_known + c, 1)
                test_md5_payload = set_byte_cbc(test_md5_payload, ("\0" * (5 - block_to_recover) * 16) + current,
                                                (6 - block_to_recover) * 16 - 1,
                                                chr((4 - block_to_recover) * 16 + 1))
                send(s, base64.b64encode(test_md5_payload))
                test_md5_result = receive_until(s, "\n")[:-1]
                if real_md5_result == test_md5_result:
                    next_block_known += c
                    print('found matching flag char:', next_block_known)
                    break
        print(next_block_known)
        current = next_block_known[:-1]


main()
