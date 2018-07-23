# Federation Workflow System (crypto, 40 solved, 119p)

```
The source code for the Federation Workflow System has been leaked online this night. 
Our goal is to inspect it and gain access to their Top Secret documents.
nc crypto-04.v7frkwrfyhsjtbpfcppnu.ctfz.one 7331
```

In the task we get [client](client.py) and [server](server.py) sources.

Using the client we can connect to the server and:

- list files on the server
- get AES-ECB encrypted file contents
- login as admin and receive the flag, if we can provide a proper one-time-password

Once we examine the server code we can see that file list is hardcoded, so not very useful.
We can also see that what we get is not exactly encrypted file contents but in fact:

```python
content = self.read_file(file)
response = '{0}: {1}'.format(file, content)
encrypted_response = self.encrypt(response)
```

So file contents, but prefixed by filename we provide!
File names are `sanitized` but in a strange way:

```python
def sanitize(self, file):
    try:
        if file.find('\x00') == -1:
            file_name = file
        else:
            file_name = file[:file.find('\x00')]

        file_path = os.path.realpath('files/{0}'.format(file_name))

        if file_path.startswith(os.getcwd()):
            return file_path
        else:
            return None
```

This simply removes anything after first nullbyte from the filename.
So if we request files `XXX\0` and `XXX\0\0\0` we would get identical result.

We can also see that we could in fact request any file from CWD by sending `../somefilename`and jumping out of `files` directory.

If we look at config files the server uses we can see:

```
self.log_path = '../top_secret/server.log'
self.real_flag = '../top_secret/real.flag'
self.aes_key = '../top_secret/aes.key'
self.totp_key = 'totp.secret'
```

So the flag, aes key and logs are out of our reach, but `totp.secret` file is not!
We could request this file from the server.

Now let's examine the `admin` command.
It's pretty straightforward - it checks the OTP and if it matches we get the flag.
OTP seems solid:

```
def totp(self, secret):
    counter = pack('>Q', int(time()) // 30)
    totp_hmac = hmac.new(secret.encode('UTF-8'), counter, sha1).digest()
    offset = ord(totp_hmac[19]) & 15
    totp_pin = str((unpack('>I', totp_hmac[offset:offset + 4])[0] & 0x7fffffff) % 1000000)
    return totp_pin.zfill(6)
```

It's time based, but we actually get the time from the server right after we login.
So the only unknown value is actually the `secret`, which is collected from the `totp.secret` file.
If we can get contents of this file, we can calculate OTP and login as admin.

We mentioned earlier that what we get is not only the content of the file, but also the filename, and that we could add as many nullbytes as we want to the filename, and still get the right file.

We could utilize those properties to recover decrypted contents of the file!
This is because we can decrypt any AES-ECB ciphertext suffix, as long as we control the prefix.
The idea is pretty simple:

- We send payload which fills the first block, leaving only a single byte available in this block.
- The first byte of suffix falls into this last byte, so we have something like `XXXXXXXXXXXXXXXS | UFFIXSUFFIXSUFFI`, where `|` is the block boundary.
- Now we encrypt 256 payloads, each one with the same prefix but the last byte of the block is changing, so we have `XXXXXXXXXXXXXXXA`, `XXXXXXXXXXXXXXXB`, `XXXXXXXXXXXXXXXC`...
- Last step is to compare the first ciphertext we got, with the last byte set by suffix, with the ciphertexts generated each with different last byte. One of those have to match, and thus we learn what is the first byte of suffix.
- We can repeat this process for the second byte, by simply shifting to the left by 1 byte. We can also extend this to recover more blocks, simply by sending more padding bytes to fill more blocks.

The code to achieve this is:

```python
def brute_ecb_suffix(encrypt_function, block_size=16, expected_suffix_len=32, pad_char='A'):
    suffix = ""
    recovery_block = expected_suffix_len / block_size - 1
    for i in range(expected_suffix_len - len(suffix) - 1, -1, -1):
        data = pad_char * i
        correct = chunk(encrypt_function(data), block_size)[recovery_block]
        for character in range(256):
            c = chr(character)
            test = data + suffix + c
            try:
                encrypted = chunk(encrypt_function(test), block_size)[recovery_block]
                if correct == encrypted:
                    suffix += c
                    print('FOUND', expected_suffix_len - i, c)
                    break
            except:
                pass
    return suffix
```

Available in our crypto-commons as well.

We combine this with function:

```python
def encrypt(pad):
    return send("file ../totp.secret\0\0" + pad).decode("base64")[16:]
```

And we can recover contents of the `totp.secret` file -> `0b25610980900cffe65bfa11c41512e28b0c96881a939a2d`.
Now we can simply connect to the server, calculate OTP and grab flag with `admin` command:

```python
def main():
    # secret = brute_ecb_suffix(encrypt, 16, 64, '\0')[2:]
    secret = '0b25610980900cffe65bfa11c41512e28b0c96881a939a2d'
    result = send('login')
    time = int(result)
    print(send('admin ' + totp(secret, time)))
```

And we get back: `ctfzone{A74D92B6E05F4457375AC152286C6F51}`
