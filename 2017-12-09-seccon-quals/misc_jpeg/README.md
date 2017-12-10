# JPEG File (Misc, 100p)

```
It will be fixed if you change somewhere by 1 bit.
```

In the task we get a [jpeg file](tktk.jpg) and the description is quite clear - we need a single bitflip to uncover the flag.
We simply generated images with bitflips and the scrolled through thumbnails.
We thought about using tesseract but it would take much time.

Bitflips were generated via:

```python
import codecs


def main():
    start_byte = 0
    stop_byte = 700
    with codecs.open("tktk.jpg", "rb") as input_file:
        data = input_file.read()
    for byte in range(start_byte, stop_byte):
        for bit in range(8):
            modified = chr(ord(data[byte]) ^ (1 << bit))
            output_data = data[:byte] + modified + data[byte + 1:]
            with codecs.open("res/" + str(byte) + "_" + str(bit) + ".jpg", "wb") as output_file:
                output_file.write(output_data)
main()
```

And once we flipped bits in byte 623 we got the flag:

![](623_1.jpg)

The flag was `SECCON{jp3g_study}`
