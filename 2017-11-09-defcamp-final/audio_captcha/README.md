# Audio captcha (Misc/PPC)

This was a funny challenge, since we've done 2-3 of those some years ago.

We get a link to a webpage where we are supposed to listen to a [voice captcha](captcha.wav) and solve it.
We need to solve a number of them without failure to get a flag.
Sounds are distorted and actually it's pretty hard to solve those even manually, and things like Google Speech API are useless here.


However, we had a pretty good idea how to work with this.
The audio data we got was wav, which means basically a raw sound stream.
The upside of this is that we can simply cut this stream into pieces and play them or work with them separately.

It was also pretty clear to us, that the sounds, although distorted, are actually always "the same".
It looked like the captcha was basically glued from the same inputs every time, without any random distortions.

This means we could do a simple pattern matching on the bytes!
The approach was simple:

1. Download some captchas and solve them by hand.
2. Split the captcha into 10 pieces (there were always 10 symbols)
3. Cut a bunch of bytes from the piece and place it in our patterns list, alongside the symbol we take it for

Now that we have the list of patterns we can simply start solving the task:

1. Download a captcha
2. Cut into pieces
3. For each piece go through the patterns list and try to get matchings
4. If more than one pattern fits skip this captcha
5. If only a single pattern matches the sample then add this symbol to the list
6. If all symbols were found send the answer to the server.

Complete solver can be found [here](captcha.py)
