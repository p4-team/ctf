# COBOL (RE, 485p, 10 solved)

In the task we get an old [IBM SAVF file](EKO.SAVF).
Unlike last year, where we could just load it to some online tools, this time the file was corrupted.

We quickly had a look around at the file contents, decoded from ebcdic string encoding, but the flag string seemed permutated, so we guessed we actually have to recover the binary and reverse it.
This was a huge mistake.
We wasted quite some time trying to fix this file, which had some checksum failures.

After a while we tried one more time to look at the strings:

```python
import codecs
import ebcdic

def decode():
    with codecs.open("EKO.SAVF", 'rb') as input_file:
        print(input_file.read().decode('cp1148'))
```

We can see there a nice section:

```
YOU ARE RIGHTWE}m_A4rREg0_RrpUN+0NI04NGsa_O+7UT3313F_+rGO3hODt0_In4DE{OASKE  NOPE], YOUR SECRET IS WRONG]
```

And from this we guess that the part:

```
}m_A4rREg0_RrpUN+0NI04NGsa_O+7UT3313F_+rGO3hODt0_In4DE{OASKE
```

Is the mangled flag.
It's clear it's inverted, so we invert it back:

```
EKSAO{ED4nI_0tDOh3OGr+_F3133TU7+O_asGN40IN0+NUprR_0gERr4A_m}
```

We know that the flag starts with `EKO{` so we need to take 2 characters, remove next 2, and again take 2.
We guessed we will check what happens if we proceed like this:

```
EKO{4n0th3r+31TUO_GNINNUR_ERA_EW
```

And inverted:

```
WE_ARE_RUNNING_OUT13+r3ht0n4{OKE
```

So we're on a good track, and we have first half of the flag.
Since the second half is also not random, we decided to do our take-2-leave-2, but with offset of 2:

```
SAEDI_DOOG_F337+as400+pr0gr4m}
}m4rg0rp+004sa+733F_GOOD_IDEAS
```

This way we get a second half of the flag and rest of the message blended in:

```
EKO{4n0th3r+31337+as400+pr0gr4m}
WE_ARE_RUNNING_OUTF_GOOD_IDEAS
```

As can is noticable now, we could have just removed all uppercase and `_` characters from the initial string to get the flag as well.
