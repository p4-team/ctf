```
Find the private key and decrypt the secret inside the picture
material.grandprix.whitehatvn.com/misc02
MD5: 2cad267bb17d5f31551c0d8713e41a77

Hint:
saintgiong.jpg.pgp
outguess
```

After mounting the ISO file `Hacker.iso`, we can start looking for interesting files.
Let's try to find the file from first hint.
```
$ grep -ri "saintgiong" .
./maildir/cur/15334499.com:Content-Type: application/octet-stream; name="SaintGiong.jpg.pgp"
./maildir/cur/15334499.com:Content-Disposition: attachment; filename="SaintGiong.jpg.pgp"
```
File is base64-encoded. After decoding it, we can see that the `pgp` extension isn't lying:
```
$ gpg --decrypt ./SaintGiong.jpg.pgp
gpg: encrypted with 512-bit ELG key, ID D332E256F0EE4293, created 2018-08-05
      "whitehat <whitehat@bkav.vn>"
gpg: decryption failed: No secret key
```
We're looking for the key with fingerprint `D332E256F0EE4293`

Next step is to find a private key for decryption:
```
$ grep -r -e "PGP" -e "PRIVATE"
[...]
etc/mail/private.asc:-----BEGIN PGP PRIVATE KEY BLOCK-----
etc/mail/private.asc:-----END PGP PRIVATE KEY BLOCK-----
[...]
```

We can check, if it's the correct key:
```
$ gpg --keyid-format 0xlong private.asc
pub   dsa2048/0x1C15C0A34BA9AFA0 2018-08-05 [SCA]
      99B0DC8EB1942ACC4F5306561C15C0A34BA9AFA0
uid                             whitehat <whitehat@bkav.vn>
sub   elg512/0xD332E256F0EE4293 2018-08-05 [E]
```

Unfortunately, the key is encrypted so we cannot use it directly, however in the same directory (`etc/mail`) there's another file: `encrypt.pyc`. Let's try to decompile it:
```
$ uncompyle6 /media/Hacker.iso/etc/mail/encrypt.pyc
import struct, sys, base64
password_enc = 'JTd1XyoIbmc3PWhpOjhfVhsIbmcAAAAA'
if len(sys.argv) != 2:
    print 'Usage: %s data' % sys.argv[0]
    exit(0)
data = sys.argv[1]
padding = 4 - len(data) % 4
if padding != 0:
    data = data + '\x00' * padding
result = []
blocks = struct.unpack('I' * (len(data) / 4), data)
for block in blocks:
    result += [block ^ block >> 16]

output = ''
for block in result:
    output += struct.pack('I', block)

print base64.b64encode(output)
```
To decrypt the password, the only thing we have to change one variable: `data = base64.b64decode(password_enc)` and print the result without encoding it with base64:
```
$ decrypt.py
Phu_Dong_Thien_Vuong
```

Now we can import the key and decrypt the picture:

![SaintGiong.jpg](SaintGiong.jpg)

It's time to use the second hint: `outguess` - steganography tool.

```$ outguess -r SaintGiong.jpg h4x```

```
While the sixth Hung Vuong Dynasty, our country, then called Van Lang was under the menace of the An , situated in the North of Vietnam’s borders.
Hung Vuong King was very worried and assembled his court to prepare a plan of defense for the country. A mandarin of the civil service reminded the King that the original founding King of the country, Lac Long Quan  had instructed that if the country were ever to face danger, it should pray for his help.
In that situation, the King then invoked the spirit of the founding King.
Three days later, a very old man appeared in the midst of a storm and said that he was Lac Long Quan himself. He prophesied that in three years the An from the North would try to invade the country; he advised that the King should send messengers all over the country to seek help from talented people, and that thereafter a general sent from heaven would come to save the country.
Event though three years later, indeed came the tempestuous foreign armies trying to take over the Southern Kingdom. At the capital city of Phong Chau, King Hung Vuong still remembered the instruction from Lac Long Quan.
However Even earlier than, at the village of Phu Dong, County of Vo Ninh, Province of Bac Ninh, a woman in her sixties reported she had seen footprints of a giant in the field.
Amazed, she tried to fit her feet in the footprints and suddenly felt that she was overcome by an unusual feeling.
Thereafter she became pregnant and delivered a boy whom she named Giong. Even at the age of three, Giong was not able to crawl, to roll over, or to say a single word.
Surprisingly, at the news of the messenger from the King, Giong suddenly sat up and spoke to his mother, asking her to invite the messenger over to their home.
He then instructed the messenger to request the King to build a horse and a sword of iron for him so that he could go and chase the invaders away.
When the horse and sword were eventually brought to his home, Giong stood up on his feet, stretched his shoulders, became a giant of colossal proportions, and asked his mother for food and new clothing.
She cooked many pots of rice for him but it was not enough for his appetite. The whole village brought over their whole supply of fabric and it was still not enough for his size.
Giong put his helmet on, carried his sword, jumped on the back of his horse and rode away, as fast as a hurricane. The iron horse suddenly spit fire, and brought Giong to the front line at the speed of lightning. The invaders saw Giong like a punishing angel overwhelming them.
Their armies were incinerated by the flame thrown from the horse's mouth. Their generals were decapitated by Giong’s sword. When it finally broke because of so much use, Giong used the bamboo trees that he pulled up from the sides of the road and wiped away the enemies.
Afterwards, he left his armor on the mountain Soc (Soc Son) and both man and horse flew into the sky.
Legend holds that lakes in the area of mountain Soc were created from the footprints of Giong’s horse. At the site of the forest where he incinerated the enemy armies is now the Chay Village ("Chay" meaning burned).
In recognition of Giong's achievement, King Hung Vuong proclaimed him Phu Dong Thien Vuong (The Heaven Sent King of Phu Dong Village). For the people of his country, he is better known as Thanh Giong ("Saint" Giong)
```

The last thing is to notice that first letters of each line form the flag:
```
$ cut -c 1 h4x | tr -d "\n"
WHITEHATSHWSGTALI
```
