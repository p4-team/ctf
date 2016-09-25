## Broken Box (Crypto, 300p)

We are given web service signing data for us, and we are told that it is somehow "broken".

Indeed, this service looks suspicious - for example, it sometimes give different signature for the same data.

We guessed that somewhere, somehow bit is flipped, because this is common trope with RSA on CTFs (so called RSA fault attacks). So we hacked simple script, to get more data:

```python
    import socket

    s = socket.socket()
    s.connect(('crypto.chal.csaw.io', 8002))

    import time
    result = open('responses_' + str(int(time.time())), 'w')
    print s.recv(9999)
    while True:
        s.send('2')
        response = s.recv(9999)
        print 'response', response
        result.write(response + '\n')
        s.send('yes')
        s.recv(9999)
        s.recv(9999)
```

I promise that someday I will learn pwnlib and stop this socket madness. Nevertheless, this script gave us all the data we needed. It is attached as responses.txt file.

N is the same everywhere, so is was not very interesting. So we used this script, to extract only signatures:

```python
import argparse

parser = argparse.ArgumentParser(description='Merge signatures')
parser.add_argument('signatures', nargs='+', help='signatures')

args = parser.parse_args()

signatures = set()
for sigfile in args.signatures:
    with open(sigfile, 'r') as sigdata:
        sigdata = sigdata.read()
        for line in sigdata.split('\n'):
            if len(line) < 3:
                continue
            signatures.add(line.split(':')[1][:-3])

for sig in signatures:
    print sig
```

So what can we do with this information?

We know that `pow(sig,e,n) == data` (where sig is correct signature). RSA signature is computed as follows:

```
pow(data, d, n) = sig
```

When we are given invalid signature, we can assume that it is computed for good data, but some bit in `d` was flipped. In other words:
* If k'th bit in d was 1 and, and turned to 0, then `d = d - 2^k`. So `pow(data, d') === pow(data, d - 2^k) === pow(data, d) / pow(data, 2^k)  (mod k)`
* If k'th bit in d was 0 and, and turned to 1, then `d = d + 2^k`. So `pow(data, d') === pow(data, d + 2^k) === pow(data, d) * pow(data, 2^k)  (mod k)`

And we can just check all possibilites here (because there is only 1024 possible values of k!).

If `badsig == good_signature * pow(2, pow(2, k, n), n)`, than we know that k-th bit was 0 and turned to 1. Similarly we can determine that bit was 1 and turned to 0.

So every bitflip allows us to recover one bit in private key. We scripted it as follows:

```python
import argparse

parser = argparse.ArgumentParser(description='Solve')
parser.add_argument('signatures', help='signatures')
args = parser.parse_args()

ls = open(args.signatures, 'rb').read().split('\n')
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def invmod(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
    return pow(a, n-2, n)

mod = 123541066875660402939610015253549618669091153006444623444081648798612931426804474097249983622908131771026653322601466480170685973651622700515979315988600405563682920330486664845273165214922371767569956347920192959023447480720231820595590003596802409832935911909527048717061219934819426128006895966231433690709
good = 22611972523744021864587913335128267927131958989869436027132656215690137049354670157725347739806657939727131080334523442608301044203758495053729468914668456929675330095440863887793747492226635650004672037267053895026217814873840360359669071507380945368109861731705751166864109227011643600107409036145468092331
ls = filter(bool, ls)
ls = map(int, ls)
ls = list(set(ls))
bad_sigs = ls

print 'precomputing +...'
good_plus = [(good * pow(2, pow(2, bit, mod), mod)) % mod for bit in range(1024)]
print 'precomputing -...'
good_minus = [(good * invmod(pow(2, pow(2, bit, mod), mod), mod)) % mod for bit in range(1024)]

bits = {}
for bad in bad_sigs:
    for bit in range(1024):
        # bad == g' == g^d' == g^(d+2**k) == good * g^2**k
        if bad == good_plus[bit]:
            bits[bit] = 0
        # bad == g' == g^d' == g^(d-2**k) == good / g^2**k
        if bad == good_minus[bit]:
            bits[bit] = 1

import sys
for i in range(1024):
    if i in bits:
        sys.stdout.write(str(bits[i]))
    else:
        sys.stdout.write('?')
print
```

And after few seconds, we had completed flag:


```
1010010010000001011011011001100100100110100111111010000111100101111000100111101101111111001001011001001101101010000100111010111110111100100100111110000011001010110101110001011010000010000100001000101001110101100110000101010001000110011101100001001110111001100110001000110100100100010010010001011100111010000101101100011100000111011010011010000010010011101001111110111101011001111011111111110100110001101100101001000110100111111011000010110001111111010000101111001101010001110101111010001011000010000100111010011011100101101111001000011101110111011001111111111101111101110100111010011100001111110000110110011101000000010111101110000100010000110110000000011100011110110111010110111110010010110000000010101000101011000011001101011000110001010111100101011101001100101110111010110001110000001000101100100011011011101110100010001100100001001100100111000000100000000000001010100101100011011101011010101111010100001100010011000110000001111011000000111011110111100111100110110101010011011011001110111011111100000101010010110111011101
```

And finally, the flag is ours:

```
In [192]: long_to_bytes(s)
Out[192]: 'flag{br0k3n_h4rdw4r3_l34d5_70_b17_fl1pp1n6}'
```
