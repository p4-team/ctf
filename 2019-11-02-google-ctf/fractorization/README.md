# Fractorization (crypto, 300p, 5 solved)

In the challenge we get [encryption code](enc.py), [encrypted flag](flag.enc), [encrypted private key](priv.der.enc) and [public key](pub.der).

The code is quite short and simple:

1. RSA keypair is generated in some secret way
2. Private RSA key is encrypted via AES-ECB
3. Flag is encrypted using public RSA key

The goal seems clear - we need to somehow recover the private key from the public key and the AES-encrypted version of the private key.

If we look closely at the private key, we can notice a very strange `pattern` at a certain point:

```
96 e7 52 3f 9a 7b 17 0a 19 2f 94 66 17 bd cc 0d
0c 0e 7c 7e c8 a2 4c 4e 6d e3 9c 6d 1b c2 68 30
96 e7 52 3f 9a 7b 17 0a 19 2f 94 66 17 bd cc 0d
0c 0e 7c 7e c8 a2 4c 4e 6d e3 9c 6d 1b c2 68 30
96 e7 52 3f 9a 7b 17 0a 19 2f 94 66 17 bd cc 0d
0c 0e 7c 7e c8 a2 4c 4e 6d e3 9c 6d 1b c2 68 30
96 e7 52 3f 9a 7b 17 0a 19 2f 94 66 17 bd cc 0d
0c 0e 7c 7e c8 a2 4c 4e 6d e3 9c 6d 1b c2 68 30
96 e7 52 3f 9a 7b 17 0a 19 2f 94 66 17 bd cc 0d
0c 0e 7c 7e c8 a2 4c 4e 6d e3 9c 6d 1b c2 68 30
96 e7 52 3f 9a 7b 17 0a 19 2f 94 66 17 bd cc 0d
0c 0e 7c 7e c8 a2 4c 4e 6d e3 9c 6d 1b c2 68 30
96 e7 52 3f 9a 7b 17 0a 19 2f 94 66 17 bd cc 0d
0c 0e 7c 7e c8 a2 4c 4e 6d e3 9c 6d 1b c2 68 30
96 e7 52 3f 9a 7b 17 0a 19 2f 94 66 17 bd cc 0d
```

This is a classic ECB encryption artifact - identical plaintext blocks encrypted into identical ciphertext blocks.

Now if we generate our own key with similar parameters (we can use the same public key and generate primes of the same size), we can notice that this particular piece of data falls into the place where first prime factor should be, plus-minus few bytes in the block before and block after.

This means that the prime factor has to have such repeating pattern spanning over 2 blocks (32 bytes), at leats in the middle.
So the prime has to be something like `X ABCD ABCD ABCD ... Y`.

We could also write this down as `ABCD * 0x10001000... + S` where `S` is the unknown part located in the non-repeating blocks, and `0x10001000...` has far more zeros.

It took us a while to come up with a reasonable solution, because initially we were thinking about looking for roots of bivariate equation with `ABCD` and `S` as our unknowns.

Eventually we came up with a far simpler formulation of the problem:

```
N = p*q
p = k*pattern+S
```

Here `pattern` is just the 0x10000...10000...1` pattern.

Now we can do:

```
N = p*q = (k*pattern+S)*q = k*pattern*q + S*q
N - S*q = k*pattern*q
(N-S*q)/pattern = k*q
```

Now let's introduce a polynomial `f(x) = (N-x)/pattern`.
From the above equation it's clear that for `x0 = S*q` this polynomial reduces to `0 mod q` because it would be a multiple of `q`.
We also know that `q` is a factor of `N`.

However, we can't directly use Coppersmith method here, because `S*q` is actually very big, it's bigger than one of the factors, so at least `N^1/2` and Coppersmith bound for this case would allow for finding roots about `N^1/4`.

But we can go one step further and make an approximation:

```
(N-S*q)/pattern ~= N/pattern - (S*q/pattern)
```

Now we can re-formulate the polynomial to `f(x) = N/pattern - x`, and since we're now looking for `x0 = (S*q/pattern)` the bound for the root is in fact close to `S*k`, which we can hope is small, but at least it's definitely smaller than previously.

We can look at this via a simple sanity check:

```python
    p = getPrime(2048)
    k = random.randint(2 ** 255, 2 ** 256)
    pattern = 0x10000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001
    q = gmpy2.next_prime(k * pattern + random.randint(0, 2 ** 256))
    S = q - k * pattern
    N = p * q
    print(math.log(N // pattern - k * p, 2))
```

This shows us that with this setup the root we would be looking for is about 512 bits long.

The solver for this problem is as described above:

```python
def solve(N, pattern):
    F.<x> = PolynomialRing(Zmod(N), implementation='NTL')
    poly = x - N//pattern
    roots = poly.small_roots(beta=0.4, X=2**600)
    for root in roots:
        val =  root - N//pattern
        q0 = gcd(N,val)
        if q0 > 1:
            print(int(root).bit_length())
            print('q',q0)
            print('p',int(N)//int(q0))
            print(hex(int(N)//int(q0)))
            return True
```

We can now run another sanity check with this, to verify it works under our assumptions:

```python
def sanity():
def sanity():
    mult = random.randint(2**255, 2**256)
    mult = 2**255
    small = random.randint(0, 2**100)
    pattern = 0x10000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001
    #big_shift = 2**(2048-8*7)
    #big = 0xABCDEFABCDEFAB * big_shift
    big = 0
    p = next_prime(big + mult * pattern + small)
    print(hex(p))
    q = random_prime(2**2048)
    N = p*q
    print(N.nbits())
    print(p)
    print(q)
    solve(N,pattern)

#sanity()
```

The `big` simulates the upper bits we don't know, which are not in the repeating pattern, and `small` lower bits.
Interestingly enough, adding this `big` part could make it unsolvable, since the root would now be very big, but it does still work for some reason.

Anyway, this is not strictly necessary in the task, because the actual root we recovered had 560 bit, so was within the Coppersmith bounds.

There was one more thing to consider - the pattern might be shifted, since the blocks are not perfectly aligned.
We don't really know where is the first `1`, so we check the shifts as well:

```python
    pattern = 0x10000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001
    for i in range(16):
        N = 864548738332874087668503368831766249570260242783591552090675185261065394078050565610543041932800764724587585870383343251100904921187940519593954644380103508613133721893687769245467054781165129931842935345632471221108475282905047577044998272614999900190070356568926673218272825600985299507924236632515852004699265280255459721713289017451417963625732868682233625418249666192969191571123259131334481738959268675197737845268734505452629162251408183665714593194085000765150594131359155637719565709425013854872777561241631196785845113023038532866885477368063060870336357032800949481193136635548507618719395155108369351135560013249407504681745255774980220938402804576145433072855750609892899681227859840020080049417911764687461353619448605061402921180936683590478280857786258094946429659735653016131876268043249607509143045235827923490215048040840605913760167939925178228075589301790633691254996042457599109896534654922831538681455372034279792686064670317873356145126455426581532494485566559734055837974168777530418933444611498167101313802133643307821986306829084673888064633316469645388738526070397530481627815041169108357108172265337488326979522139084457836177137061191877719132682265381042692814726652081549112958388430260682287769002623
        if solve(N,pattern):
            print(hex(pattern))
            return
        pattern >>=8
```

And running this returns `p`, and `q`, which we can then use to decrypt the flag:

```python
    p = 31555720069118467147821203380224688806508163874037062556871239093255339528072891743195624687579532411584859333841089765811499736308991315463091756017090529202299936208689648373141343597991860093978598902926090232992764931582226454250074858177012092591548149291064575730653835010920492247198535167191585166480877445761052166924142883439179965961951576933148558934090755078213363498758285000755039337195455242673921605828911137420067348601000484969826029498761388313806843351409851631342417130602655307496140948184067195777694576593815738040507892091972065716370060935261045921496556097674611235357384656566616433908673
    q = 27397528449333398750266387529399849594682216775605225874849547559945466938581310049056423758294428745281988771459564198153711125673814939447341104464740539016255096946065703781298853877488132070586594115004124442717121218952600553960735334894628874273087986471973958189578919842785742959834288220821152546005560279488312797225964835987590602038239664681987623721916034601354242735359390919706918151677300197346402700017376804125322544083323057603601951652908109780754435619135175157568318298834572584611540505862918372984499337203170925029821230664438885207275220250572467711031742903314341377918564015565214188441151
    e = 65537
    d = modinv(e, (p - 1) * (q - 1))
    data = open("flag.enc", 'rb').read()
    print(long_to_bytes(pow(bytes_to_long(data), d, p * q)))
```

And we finally get `CTF{ju5t-A-cheap3r-w4y-t0-generate-pR1m3s}`
