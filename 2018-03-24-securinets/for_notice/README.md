# Notice me (forensics/stegano)

In the task we get some image drive (heavy one, so we won't upload it here), and hint that someone had secret data they removed.
Binwalk says there is a PNG file and strings analysis shows that this PNG is close to `trash` strings.

We extract the image:

![](0.png)

Then we checked with stegsolve is maybe there is something hidden in the picture, and it turns out that LSB of the last data lines hides a link, to another image.
They look identical, but the next image hides a different link.
We assume this might be a long chain, so we've wrote a script to download the whole chain:

```python
import codecs
import requests
from crypto_commons.generic import chunk


def extract_link(data):
    bits = []
    for b, g, r, a in data:
        lsb = b & 1
        bits.append(lsb)
    chunked_bytes = chunk(bits, 8)
    integers = map(lambda x: int("".join(map(str, x)), 2), chunked_bytes)
    full = "".join(map(chr, integers))
    print(full[-100:])
    return full[-23:]


def main():
    from PIL import Image
    index = 0
    filename = "pngs/" + str(index) + ".png"
    while True:
        im = Image.open(filename)
        data = im.getdata()
        index += 1
        new_link = extract_link(data)
        print(new_link)
        r = requests.get("http://" + new_link)
        filename = "pngs/" + str(index) + ".png"
        with codecs.open(filename, "wb") as output_file:
            output_file.write(r.content)


main()
```

It turns out it didn't take that long, already the 6th image is:

![](6.png)

And hides: `Flag{M1nD_4wAk3_b0DY_4sl33P}`
