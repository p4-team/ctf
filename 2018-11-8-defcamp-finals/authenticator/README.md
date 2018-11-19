# authenticator (pwn, 2 solves) 

This task was categoried as pwn, but in fact it was RE and simple crypto.
The hardest part of this task was to reverse engineer the binary.

main calls following functions:

`000000000406950` is sha1 function from boost library. The proof is the string `/usr/include/boost/uuid/sha1.hpp`.


`0000000000406410` is also a cryptography function. 
Let's call it `crypto_function` now, we will look at it closely later.

The pseudocode of main() function is below:

```C
int main()
{
	sha = boost_sha1(); //buffer of 16 bytes
	
	if (strcmp(user_input(),"HELLO")) return 0;
	
	bytes = read("/dev/urandom",16); //buffer of 16 bytes
	print_bytes_hex(bytes);
	bytes2 = read("/dev/urandom",16); //buffer of 16 bytes
	print_bytes_hex(bytes2);
	
	print_some_strange_data(); //idk what is this, it's not needed anyway :)
	
	if(crypto_function(bytes2, user_input(), 16, some_bytes) == bytes1)
	  print crypto_function(bytes2, flag, 16, some_bytes);
}
```

`user_input` is a function which reads data from the user.

Now let's investigate `crypto_function`. 
I was sure that this isnt any new crypto but just from some library.
We can see that it calls various virtual methods from vtable.
After navigating to the memory of them we can gain more information.

For example above offset `73F500` is located the following string:

```
.data.rel.ro:000000000073F4F8                 dq offset _ZTIN8CryptoPP14CTR_ModePolicyE ; `typeinfo for'CryptoPP::CTR_ModePolicy
.data.rel.ro:000000000073F500 unk_73F500      db    0  
```

also this one is interesting:

```
.data.rel.ro:0000000000741BC8                 dq offset _ZTIN8CryptoPP8Rijndael4BaseE ; `typeinfo for'CryptoPP::Rijndael::Base
.data.rel.ro:0000000000741BD0 unk_741BD0      db    0                 ; DATA XREF: sub_406410+3CD↑o
``` 


So I just concluded that this is AES-128 encryption in CTR mode.
I've set a breakpoint at this function and printed their arguments:

- 1: random data, different at every time.
- 2: user input
- 3: int 16
- 4: 0x0d00000f0d0a0af7, 0x0d00000f0d0a0a0b
- 5: where encrypted data will be stored

I came to the conclusion that the first argument is ctr, 4 is the key.
I checked if my theory about this cipher function is correct - I copied arguments and output abd wrote the following python script:

```python
from pwn import *
from crypto_commons.symmetrical import aes
        
def aes_encode(input):
	global key
	global ctr
	AES = aes.AES()
	AES.init(key)
	w = AES.encrypt(ctr)
	w = xor(input, w)
	return w

def aes_decode(input):
	global key
	global ctr
	AES = aes.AES()
	AES.init(key)
	w = AES.encrypt(ctr)
	w = xor(input, w)
	return w	
	
key = "f70a0a0d0f00000d0b0a0a0d0f00000d" #wytestowac nowe kombinacje
ctr = "f3 e9 cf 98 bb 8d 94 58 43 61 21 f4 f8 e3 19 ad"
input = "a"*16

ctr = ctr.replace(" ","").decode("hex")
key = key.replace(" ","").decode("hex")
	
x = aes_encode(input)
print "encrypted user input: "+x.encode("hex")
print "the output from binary: 9bcefda8b86570db6d8330986472ac5e"
```

output:

```
a@x:~/Desktop/Authenticator$ python test.py 
encrypted user input: 9bcefda8b86570db6d8330986472ac5e
the output from binary: 9bcefda8b86570db6d8330986472ac5e
```

It proves that my predictions were correct.

if we want to pass `if(crypto_function(bytes2, user_input(), 16, some_bytes) == bytes1)` in `main` function, it's obvious, that user input needs to be equal the output of the decryption function AES-128 CTR mode with `bytes1` as data to decrypt 
 

The key to `crypto_function` was the same at every run when ASLR was switched off.
When ASLR was switched on, the first byte of the key was different at every run.
I also checked this on different linux systems and it was the same.
So I wrote the exploit that connects to the server and tries to brute-force all possibilities of the first byte of the key:

```
from pwn import *
from crypto_commons.symmetrical import aes

def recvall(r):
    d = ""
    n = "a"
    
    while n:
        n = r.recv(timeout = 0.2)
        d += n
        
    return d 
	
def aes_decode_(key,input,ctr):
	print ctr
	ctr = hex(ctr)[2:]
	ctr = ctr.rjust(32,"0")
	ctr = ctr.decode("hex")
	
	AES = aes.AES()
	AES.init(key)
	
	w = AES.encrypt(ctr)
	w = xor(input, w)
	return w	

def split_string(string, split_string):
    return [string[i:i+split_string] for i in range(0, len(string), split_string)]

def aes_decode(key,input,ctr):
	ctr = ctr.encode("hex")
	ctr = int(ctr,16)
	input = split_string(input, 16)
	decrypted = ""
	for i in input:
		decrypted += aes_decode_(key, i, ctr)
		ctr += 1
	return decrypted

def try_key(key):
	r = remote("46.101.180.78", 13031)
	r.sendline("HELLO")

	data = recvall(r)
	print data
	random1 = data.split("\n")[0]
	random2 = data.split("\n")[1]
	print "-----------"
	print random1
	print random2

	random1 = random1.replace(" ","").decode("hex")
	random2 = random2.replace(" ","").decode("hex")

	key = key.decode("hex")

	inp = aes_decode(key, random1, random2)
	print inp.encode("hex") 

	r.send("1"+inp+"\n")

	print "encrypted flag:"

	encrypted_flag = r.recv()
	print len(encrypted_flag)
	print encrypted_flag
	print "###"
	decrypted = aes_decode(key,encrypted_flag,random2)
	print decrypted
	if "DCTF" in decrypted:
		exit()
	r.close()

for brut_byte in range(0x00,0x100):
	gg = hex(brut_byte)[2:]
	gg=gg.rjust(2,"0")
	print gg
	try_key(gg+"0a0a0d0f00000d0b0a0a0d0f00000d")
```


and the flag is:

```
DCTF{a1fee34f2a3e6e010d786f02865dc39896faa6b589d1f57f565bac9bd1d85cae}
```

Summing up, the task was very easy if you reversed the binary properly.
The task was categoried wrongly and this could mislead people, maybe this is why this task hadn't many solves.
