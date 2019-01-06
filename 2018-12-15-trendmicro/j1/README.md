# Brewery hack J1 (forensics/osint/reverse/crypto)

This was an interesting multi-stage challenge.
It starts with a 80MB pcap for analysis.
For simplicity we're include only the [relevant part](attack.pcap) with the actual attack.

From this pcap part we can see that the user downloads some `.doc` file with [obfuscated macro](macro_obfuscated.txt) inside.
After cleaning up the code we end-up with some pretty clear [malware code](macro.txt)

After this file is downloaded the attacker sends some commands to the victim:

- get_information
- get_process_list
- exe

The last one is particularly interesting because it seems to be some kind of dropper command, which transfers binary payload to the target:

```
case "exe":
    start_and_load_exe();
    request("exe", "info=OK", 1);
    break;
```

It took us a couple of tries to properly extract the [payload](binary.exe), because it contained some HTTP requests and wireshark split it strangely.

The binary searches for `.XLS` files, and once such file is found, its contents are encrypted and sent to the server.

In the pcap we can see one such payload being transferred, and our goal is to recover the original file.

The encryption itself doesn't look very scary, because it uses only `xor` and `addition` with a `key` embedded in the binary itself:

```c
void encrypt(char* dest, unsigned char* src, int seedx, int sz) {
	unsigned int* destptri = (unsigned int*)dest;
	unsigned int* srcptri = (unsigned int*)src;
	unsigned int* keyptri = (unsigned int*)key;
	for (int i = 0; i < sz; i+=8) {
		*destptri = *srcptri ^ *keyptri;
		destptri++;
		keyptri++;
		srcptri++;
		*destptri = *srcptri + *keyptri;
		destptri++;
		keyptri++;
		srcptri++;
		if (keyptri >= (unsigned int*)(key + 40)) {
			keyptri = (unsigned int*) key;
		}
	}
	seed = seedx;
	short tab[10000];
	for (int i = 0; i < sz; i++) {
		printf("%02x\n", (unsigned int)dest[i]&0xff);
		tab[i] = weird_base(dest[i]);
	}
	char* asd = (char*)tab;
	for (int i=0; i<sz; i+=1) {
		dest[2*i] = asd[2*i+1];
		dest[2*i+1] = asd[2*i];
	}
}
```

What is also interesting, is that the encryption process duplicates the data via `weird_base` function.
The tricky part to break was the `weird_base` function.
Its output looks a bit like base64, but in reality the function was doing some strange encoding using random values all the time.
At first we thought it will be necessary to brute-force the seed (doable, it's 32 bits) using the known XLS file header, but it turned out to easier than that.
Also this idea didn't work anyway, because the file turned out to be XLSX and not XLS, so the header was different.

After some analysis of the `weird_base` function, we realised that:

- Every byte is encoded on 2 bytes
- Each of the resulting bytes contains information about 4 bits of the input "clear" of the random data

Basically by doing:

```c
for (int i=0; i<sz; i++) {
    dst[i] = (src[2*i+1] & 0xf) | ((src[2*i] & 0xf) << 4);
}
```

We can recover the original data sent to `weird_base` function, without worrying about the random values mixed into the ciphertext.

From this point the decryption is trivial, because it's just xor and subtraction:

```c
void decrypt(char* dst, unsigned char* src, int sz) {
	for (int i=0; i<sz; i++) {
		dst[i] = (src[2*i+1] & 0xf) | ((src[2*i] & 0xf) << 4);
	}
	unsigned int* dstptri = (unsigned int*)dst;
	unsigned int* keyptri = (unsigned int*)key;
	for (int i = 0; i < sz; i+=8) {
		*dstptri = *dstptri ^ *keyptri;
		dstptri++;
		keyptri++;
		*dstptri = *dstptri - *keyptri;
		dstptri++;
		keyptri++;
		if (keyptri >= (unsigned int*)(key + 40)) {
			keyptri = (unsigned int*) key;
		}
	}
}
```

Whole code available in [decryptor](decryptor.c).

Once we run this, we can recover the original [XLS file](stolen_file.xls) stolen during the attack.
From this file we can get the information to get the flag for the challenge.

Last piece of the puzzle was to provide the name of the group which presumably performed the attack, and we can recover this information by looking into the IP address of the attackers -> `185.17.121.200`, and we get the name `BATELEUR`.
