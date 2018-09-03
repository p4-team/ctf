# SCS7 (crypto, 112p, 134 solved)

In the challenge we get access to a blackbox encryption service.

```
$ nc crypto.chal.ctf.westerns.tokyo 14791
encrypted flag: LY7Gj9deCPzsXNpp0SQcyp9XmtvqUn0ddkWNGFX1AHTbT3mn5uYcu7RbAZ10Tuxp
You can encrypt up to 100 messages.
message: aa
ciphertext: wg9
```

The service gives us ciphertext of the flag in base64-like encoding, and we can encrypt 100 messages per single connection.
The approach here is pretty simple - we brute-force the flag, checking how much of the ciphertext matches the encrypted flag, and use this to guess the "next character".

Judginig by the length of the ciphertext the flag should be 47 characters long, because only such input length gives us ciphertext with correct size.
We also know the flag prefix `TWCTF{`, so now we only need to guess the next characters.
Sending just `TWCTF{` with some random characters as padding gives us `9` matching ciphertext characters.
If we now test all characters on the next position, we hit score `10` for character `6`, which means it's the next character.

In some cases there are multiple characters giving the same result, and in such case we need to test all of them in the next step.
There is a useful property here -> it seems the encryption is somehow monotonic, so if we test characters in ascii order, once the score goes "down" we can break, because we already passed all viable options.

There is a special case when no character actaully raises the score, but in such case we just take all the values with highest score for the next round.
After a moment we realised that charset seems to be only lowercase hex, so we stick to this to speed things up.

```python
import re
import string
import sys

from crypto_commons.netcat.netcat_commons import nc, send, receive_until_match


def count_matching(enc_flag, param):
    counter = 0
    for i in range(len(param)):
        if enc_flag[i] == param[i]:
            counter += 1
        else:
            return counter
    return counter


def find_max_for_prefix(flag_len, flag_prefix, port, url):
    s = nc(url, port)
    initial = receive_until_match(s, "message: ")
    enc_flag = re.findall("encrypted flag: (.*)", initial)[0]
    print(initial)
    max_score = 0
    maxes = []
    for c in string.digits + "abcdef":  # charset
        data = flag_prefix + c + ('0' * (flag_len - len(flag_prefix) - 2)) + '}'
        send(s, data)
        result = receive_until_match(s, "ciphertext: .*\n")
        result = re.findall("ciphertext: (.*)\n", result)[0]
        matched = count_matching(enc_flag, result)
        print(matched, flag_prefix + c)
        if matched == len(enc_flag):
            print("Found", data)
            sys.exit(0)
        if matched > max_score:
            max_score = matched
            maxes = [c]
        elif matched == max_score:
            maxes.append(c)
        elif matched < max_score:
            break  # won't get better anymore
        receive_until_match(s, "message:")
    s.close()
    return max_score, maxes


def main():
    flag_len = 47
    flag_prefix = "TWCTF"
    maxes = ['{']
    current_score = 8
    url = "crypto.chal.ctf.westerns.tokyo"
    port = 14791
    while True:
        for c in maxes:
            flag_prefix_test = flag_prefix + c
            max_score, new_maxes = find_max_for_prefix(flag_len, flag_prefix_test, port, url)
            if (max_score > current_score) or ((max_score == current_score) and len(new_maxes) < 16):
                current_score = max_score
                maxes = new_maxes
                flag_prefix += c
                print(flag_prefix)
                break


main()
```

After a while this will return the flag: `TWCTF{67ced5346146c105075443add26fd7efd72763dd}`
