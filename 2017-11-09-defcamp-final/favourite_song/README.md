# Caesar's favourite song (Misc/Crypto/Stegano)

In the task we get a [song](killthegauls.mp3).
We also know that the flag format is `DCTFXXXDCTF`.

We start off by translating the song into [notes](killthegauls.xml) by some free software.
One we have the transcription we parse this and store in a single list.
Initially we didn't take octave into consideration and we couldn't get this to work, but fortunately at some point we remembered that there were sounds in a different octave. We marked this different octave sounds as lowercase, to keep track of them.

We noticed that if we combine pairs of sounds next to one another we get identical sequence of length 4 at the start and end, which would fit the flag format:

`['AA', 'AG', 'BA', 'Ac', 'GD', 'GD', 'GD', 'AB', 'AF', 'Ge', 'Gc', 'AB', 'GD', 'GD', 'GA', 'GB', 'GB', 'AA', 'AE', 'GD', 'AG', 'GF', 'GA', 'AB', 'GA', 'GG', 'AB', 'GG', 'Ge', 'Ac', 'AA', 'GE', 'AG', 'GE', 'AA', 'GD', 'Gf', 'Gd', 'Ge', 'Gd', 'AA', 'AG', 'BA', 'Ac']`

Now we need to somehow "decrypt" rest of the flag.
We knew that `AA` should become `D`, `AG` should be `C`, `BA` should be `T` and `Ac` should be `F`.

Looking at bits of the expected symbol we noticed that bit sequences of the `A` are the same, but in case of `BA` they're shifted by 4.
We guessed that there is a simple arithmetic encoding here -> first character in the pair is translated into some number and shifter by 4 bits to the left, and then added to the translated second character.
From the flag format we could devise that `A` has to translate to `4`, `G` translate to `3`, `B` translate to `5` and `c` translate to `6`.

We expected that those are not just some random values, since otherwise we could not decrypt this in an unique way.
Since this was all about music, we thought that maybe it's an actual music scale, we looked at some and finally we found one that fit -> `D major`.
We applied the whole scale and decrypted the flag.

Whole solver [here](caesar.py)
