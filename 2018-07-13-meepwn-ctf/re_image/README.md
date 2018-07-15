# Image crackme (re/crypto, 61 solved, 100p)

In the challenge we get a [binary](image_crackme.exe) a [sample input](MeePwn.jpg) and [output](MeePwn.ascii.bak).
The binary performs some kind of encryption of given payload, using privided key.

It was a RE challenge, but code looked horrible, so we decided to try blackboxing this.
Especially that task decription was 

```
Find the key that was used to generate Meepwn.ascii.bak
Sometimes you don't really need to read the code 
```

Once we run the tool a couple of times we noticed that:

1. The payload is always the same len as inputs, so more likely a stream, not block cipher
2. The encryption using key `A` and `AA` is identical, so the provided key  must somehow be expanded. This indicates some kind of repeating XOR. This can be firther verified by encrypting using `AAAAAA` and `AAAAAB`, in which case every 6th byte differs.
3. Since the output charset is very limited, there have to be collisions.

We figured that the easiest way to solve this, will be simply brute-forcing the key byte-by-byte, and comparing it with the expected result.

## Length recovery

First step was to recover the initial key length:

```python
with codecs.open("MeePwn.ascii.bak", "r") as flag_file:
    reference_data = flag_file.read()
        
def recover_key_len(reference_data):
    key = "MeePwn"
    while True:
        key += 'A'
        d = popen("image_crackme.exe", 'w')
        d.write(key)
        d.close()
        with codecs.open("MeePwn.ascii", "r") as new_file:
            data = new_file.read()[2 * len(key):2 * len(key) + 6]
            second = reference_data[2 * len(key):2 * len(key) + 6]
            if data == second:
                print(len(key))
                real_len = len(key)
                break
    return key, real_len
```

What we do, is simply comparing the part of the file encrypted by first "key expansion", so see if it matches.
It should be encrypted using `MeePwn` flag prefix as key if we got the length correctly.

This way we recover the length = 33.

## Key recovery

Now that we know the length, we can proceed to recover the actual flag.
We encrypt the reference picture with key consisting of only `A` but the first character we set to every printable char.
Then we check if the characters in the output file, which should have been encrypted using first key character, are correct.
If so, we got the right char and we can proceed to set another one.
It's important to check not only a single character, but characters from next "key expansions", due to conflicts.

```python
with codecs.open("MeePwn.ascii.bak", "r") as flag_file:
    reference_data = flag_file.read()

def verify(expansion, data, reference_data, real_len, char_index):
    return data[expansion * real_len:expansion * real_len + char_index + 1] == reference_data[expansion * real_len:expansion * real_len + char_index + 1]

def recover_key(real_len, reference_data):
    key = list("A" * real_len)
    for i in range(real_len):
        for c in string.printable:
            key[i] = c
            d = popen("image_crackme.exe", 'w')
            d.write("".join(key))
            d.close()
            with codecs.open("MeePwn.ascii", "r") as new_file:
                data = new_file.read()
                result = True
                for expansion in range(4):
                    result &= verify(expansion, data, reference_data, real_len, i)
                if result:
                    key[i] = c
                    break
        print("current key = ", "".join(key))
    return "".join(key)
```

And after a moment we get: `MeePwn{g0l4ng_Asc11Art_1S84wS0me}`
