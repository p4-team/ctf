import requests

from crypto_commons.generic import xor_string

s = requests.Session()


def get_state():
    return requests.utils.unquote(s.cookies['Encrypted_Game_Session']).decode('base64')


def main():
    s.get('http://hacktactoe.dctf-f1nals-2017.def.camp/action.php?action=init')
    original_state = get_state()
    pt = 'a' * 100
    s.get('http://hacktactoe.dctf-f1nals-2017.def.camp/action.php?name=' + pt)
    state_with_long_name = get_state()
    matching_block = state_with_long_name[112:112 + len(pt)]
    keystream = xor_string(matching_block, pt)
    print(xor_string(original_state[112:], keystream))
    print(keystream.encode("hex"))
    print(xor_string(original_state, keystream[:32] * 10))


main()
