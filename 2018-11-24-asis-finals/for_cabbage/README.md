# Green Cabbage (for, 322p, 7 solved)

A pretty random challenge.
It was very simple "technically", but the hardest part was to guess what's going on there.
We get a [pcap](Green_Cabbage.pcap) to analyse.
The only interesting part is some communication with server `37.139.4.247` on port `31337`.

Some base64 binary-looking payloads are sent back and forth.
The server is up so we can try sending data as well, but without knowing what we're looking at it's a bit hard.

One communication in the pcap is interesting, because it results in:

```
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
BBBBBBBBBBBBBBBBBBBBBBrrrrrrrrrrrrrrroBBBBBBBBBBBBBBBBBBBBB
BBBBBBBBBBBBBBBBtrrrrrrrrrrrrrrrrrrrrrrrrrtBBBBBBBBBBBBBBBB
BBBBBBBBBBBBBrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrBBBBBBBBBBBBB
BBBBBBBBBBBrrrrrrrrrrrrrrrrrrrrrr   rrrrrrrrrrrrBBBBBBBBBBB
BBBBBBBBBrrrrrrrrrrrrrrrrrrrrrr      rrrrrrrrrrrrrBBBBBBBBB
BBBBBBBrrrrrrrrrrrrrrrrrrrrrrr       rrrrrrrrrrrrrrrBBBBBBB
BBBBBBrrrrrrrrrrrrrrrrrrrrrrr        lrrrrrrrrrrrrrrrBBBBBB
BBBBtrrrrrrrrrrrr   rrrrrrrr         rrrrrrrrrrrrrrrrroBBBB
BBBBrrrrrrrrrrrl    rrrrrrr          rrrrrrrrrrrrrrrrrrBBBB
BBBrrrrrrrrrrrr     rrrrrr           rrrrrrrrrrrrrrrrrrrBBB
BBrrrrrrrrrrrr     irrrrrr           rrrrrrrr rrrrrrrrrrrBB
BBrrrrrrrrrrr      rrrrrr           rrrrrrri   rrrrrrrrrrBB
Borrrrrrrrrrr      rrrrri           rrrrrr     rrrrrrrrrroB
Brrrrrrrrrrr      rrrrrr            rrrrrr     rrrrrrrrrrrB
Brrrrrrrrrrr     rrrrrr            rrrrrr      rrrrrrrrrrrB
Borrrrrrrrrr     rrrrrr           irrrrr      rrrrrrrrrrroB
BBrrrrrrrrrr   irrrrrrr           rrrrrr      rrrrrrrrrrrBB
BBrrrrrrrrrrr rrrrrrrr           rrrrrri     rrrrrrrrrrrrBB
BBBrrrrrrrrrrrrrrrrrrr           rrrrrr     rrrrrrrrrrrrBBB
BBBBrrrrrrrrrrrrrrrrrr          rrrrrrr    lrrrrrrrrrrrBBBB
BBBBBrrrrrrrrrrrrrrrrr         rrrrrrrr   rrrrrrrrrrrroBBBB
BBBBBBrrrrrrrrrrrrrrrl        rrrrrrrrrrrrrrrrrrrrrrrBBBBBB
BBBBBBBrrrrrrrrrrrrrrr       rrrrrrrrrrrrrrrrrrrrrrrBBBBBBB
BBBBBBBBBrrrrrrrrrrrrr      rrrrrrrrrrrrrrrrrrrrrrBBBBBBBBB
BBBBBBBBBBBrrrrrrrrrrrr   rrrrrrrrrrrrrrrrrrrrrrBBBBBBBBBBB
BBBBBBBBBBBBBrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrBBBBBBBBBBBBB
BBBBBBBBBBBBBBBBorrrrrrrrrrrrrrrrrrrrrrrrrBBBBBBBBBBBBBBBBB
BBBBBBBBBBBBBBBBBBBBBBrrroootttllliiiBBBBBBBBBBBBBBBBBBBBBB
```

At some point one of our friends googled thr word in the bottom -> `Brrroootttllliii` and we found https://github.com/google/brotli with matching logo.

We did a quick check and yes, the payloads are simply compressed with brotli.
The only thing left was to communicate with the server:

```
hi all, ********************
send the exact time in epoch format please...
```

Once we send the timestamp we get back the logo.
Then:

```
as you found that we are using Brotli compression algorithm for connection
in this task you should find a compressed string inside the given byte stream
are you ready? [Y]es or [N]o ********************
RJYafFyURxsp3r0D6jJVZibafFyURxsp3r0D6jJVZibafFyURxsp3r0D6jJVZibXcV
whats the message?**********
```

Now this was very confusing because we didn't understand what is the goal here.
We tried to do some cryptanalysis on this strange string, but eventually someone suggested that maybe we simply need to send this random string back.
We did and we got the flag: `ASIS{Brotli_iz_the_b35t_lOssl3s5_c0mpr3ss1oN_algOr1thm___Ri9ht??}`

Full solver [here](cabbage.py)
