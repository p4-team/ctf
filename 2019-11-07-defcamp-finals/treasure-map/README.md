# Treasure map (forensics/osint, 136p, 12 solved)

A very weird challenge.
We get a [pdf](pdf.pdf) to work with.
We initially spent a lot of time analysing it, looking at the streams, fonts, etc.
In the end someone noticed that the geographical locations names in the content of the pdf, at the very beginning are the same as at very end (they're repeated).
This prompted us to think that there was supposed to be DCTF prefix and suffix, so maybe that's it.
Then we needed even more time, to just by pure chance notice how one of the places `Kruglyy Prud` looks like on the map.
It looked like a letter `D`.
5545 Humboldt Ave S, Minneapolis, MN 55419, USA - i think about `S` or `2` from the post.
3015 E Evergreen Blvd, Vancouver, WA 98661, USA - `T`
Overland Rd, Meridian, ID, USA Towers at Kuhio Park Apartments - `Y`
Libration Systems Management - `L`
M74X+H7 Taastrup,Høje-Taastrup Municipality,Denmark - Maybe `I`
1299-1261 N Kelham Ave Oklahoma City,OK 7311 - maybe `N` or `T`
testing missile capabilities - maybe `A`

When we checked the other places we noticed that you could also associate them with letters/digits, and finally recover the flag.

