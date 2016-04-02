## Invest (Forensics, 50points)
	tl;dr dump http objects, use scheme to get the key, decode the encrypted file using aes-256-cbc

We're given a [pcap file](invest.pcapng) that contains some internet traffic, there are lots of downloaded files so we decided to export the using `Export Objects -> HTTP`.

There are 2 folders: `chall` and `key`. Chall contains a lot of base64 encoded files which turn out to be a split encrypted message. We can concact them simply using `cat * > out` 

Key folder has some 'funny' pictures but what interests us is `12767348_10208095326368148_1014857467_n.jpeg`: (my annotations)

![alt](scheme.png)

And `key.txt`:

```
010001110101111001100011011011100100100100111001010111100100011101000111001110010100011100111001010001110011100101000111001110010101111001100011011011100100100101101110010010010011100100110101010111100110001100111001001101010110111001001001011011100100100101000111010111100011100100110101011011100100100101011110011000110100011101011110001110010011010101011110011000110101111001100011010111100110001101000111010111100101111001100011011011100100100101000111010111100011100100110101010001110101111001101110010010010101111001100011010111100110001101101110010010010101111001100011010111100110001100111001001101010100011101011110010111100110001101011110011000110101111001100011010001110101111001000111010111100101111001100011011011100100100101101110010010010101111001100011
```

We cannot use the key as the password (as well as decrypted binary). Let's try to run it through the graph byte by byte.

[decode.py](decode.py) does the job for us, we get `001101000101010101101011011110100011100100110101010001100011001001011001011100010101000001101001` or `4Ukz95F2YqPi` back, pretty good so far.

Looking up the message header (`Salted__`) we come across [this](http://justsolve.archiveteam.org/wiki/OpenSSL_salted_format) website. So we probably have to use openssl to decrypt the flag, okay but which encryption algorithm?... 

Let's brute it!

```bash
code=(aes-128-cbc aes-128-ecb aes-192-cbc aes-192-ecb aes-256-cbc aes-256-ecb base64 bf bf-cbc bf-cfb bf-ecb bf-ofb camellia-128-cbc camellia-128-ecb camellia-192-cbc camellia-192-ecb camellia-256-cbc camellia-256-ecb cast cast-cbc cast5-cbc cast5-cfb cast5-ecb cast5-ofb des des-cbc des-cfb des-ecb des-ede des-ede-cbc des-ede-cfb des-ede-ofb des-ede3 des-ede3-cbc des-ede3-cfb des-ede3-ofb des-ofb des3 desx rc2 rc2-40-cbc rc2-64-cbc rc2-cbc rc2-cfb rc2-ecb rc2-ofb rc4 rc4-40 seed seed-cbc seed-cfb seed-ecb seed-ofb)

for c in ${code[@]};
do
	echo $c;
	openssl $c -d -in out.bin -pass file:pass.txt -out decoded/$c;
	echo $c;
done;
```

It turns out that aes-256-cbc runs without any problems, it creates a Microsoft Word 2007+ document. Since I don't have Microsoft Office(lol) let's just treat it as a zip and see what's inside.

![alt](bingo.png)

Bingo!
