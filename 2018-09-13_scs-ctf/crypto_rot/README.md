# Rot (Crypto)

Another ciphertext-only challenge. This time, ciphertext is even shorter:

```
5?5?6B0a_`gL:d=6a!|vBc<<A=q>YA8|#A=Urr6t{"N
```

We immediately can infer *something* about the encryption, because we know that `scsctf_2017{` encrypts to ```5?5?6B0a_`gL```. The same input characters encode to the same output characters, so this is a substitution cipher.

The challenge title and description suggested `rot` operation. Alas, there are no obvious patterns in:

```python
mapping = {
    '5': 's',
    '?': 'c',
    '6': 't',
    'B': 'f',
    '0': '_',
    'a': '2',
    '_': '0',
    '`': '1',
    'g': '8',
    'L': '{',
    'N': '}',
}
```

But we compute differences between ASCII values of various characters:

```python
for k, v in mapping.iteritems():
    print v, ord(v) - ord(k)
```

The result is quite regular:

```
f 36
{ 47
} 47
0 -47
2 -47
1 -47
8 -47
_ 47
s 62
t 62
c 36
```

Now, as I've said, we hate guessing. So we decided to approach this problem
methodically, instead of getting into the task author's head.

One of my teammates noticed that there are only a few possible differences for
ASCII values. So he tried subtracting `[36, 47, -47, 62]` from every ciphertext
character, and written down all printable results at every position:

```
scsctf_2018{i5at2EMGf4kkeaBb*egMGea&CCtELF}
            x l  P    zzpl m}pv Rply     Q
                                a
```

According to that, for example, there are only two candidates for the character
after `{`, etc.

My other teammate deduced that since this is a substitution cipher and there is
clearly a lot of structure in the transformation, it should be possible to
guess the blanks in the sbox. His proposition was:

```python
rot = '5?5?6B0a_`gL:d=6a!|vBc<<A=q>YA8|#A=Urr6t{"N'

out = ''' !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~'''
inn = '''OPQRSTUVWXYZ[\]^_`pqrstuvwxyzabcdefghijklmno{|}~!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMN '''

from string import maketrans
m = maketrans(out, inn)
print rot.translate(m)
```

This prints `scsctf_2018{x5at2PMGf4zzeaBb*evMRea&CCtELQ}` and both solutions agree that this should be the correct flag. But it was not accepted by the system.

The last breakthrough was by me. First I noticed that the top and bottom parts
are almost a rotation - but not quite. I fixed this with a new proposition:

```
out = ''' !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}'''
inn = '''OPQRSTUVWXYZ[\]^_`pqrstuvwxyzabcdefghijklmno{|} !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMN'''
```

Finally, I noticed that the lowercase alphabet is rotated but uppercase characters are not. I fixed that too:

```python
out = ''' !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}'''
inn = '''DEFGHIJKLMNO[\]^_`pqrstuvwxyzabcdefghijklmno{|} !"#$%&'()*+,-./0123456789:;<=>?@PQRSTUVWXYZABC'''
```

And that was it - the resulting flag was accepted by the system:

```
scsctf_2018{x5at2EBVf4zzeaQb*evBGea&RRtTAF}
```