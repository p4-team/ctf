# Treasure map (forensics/osint, 136p, 12 solved)

A very weird challenge.
We get a [pdf](pdf.pdf) to work with.
We initially spent a lot of time analysing it, looking at the streams, fonts, etc.
In the end someone noticed that the geographical locations names in the content of the pdf, at the very beginning are the same as at very end (they're repeated).
This prompted us to think that there was supposed to be DCTF prefix and suffix, so maybe that's it.
Then we needed even more time, to just by pure chance notice how one of the places `Kruglyy Prud` looks like on the map.
It looked like a letter `D`.
Humboldt Ave looked like I (or 1)
When we checked the other places we noticed that you could also associate them with letters/digits, and finally recover the flag.

