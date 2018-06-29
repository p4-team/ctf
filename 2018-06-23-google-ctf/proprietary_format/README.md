# Proprietary format, re, 326p

> The villains are communicating with their own proprietary file format. Figure out what it is.

> proprietary.ctfcompetition.com 1337

We were given an encoded binary file of unknown format, and service to connect to. Sending some data there,
we were getting some errors like `P6 expected` or `width` expected. It looks like it expected image in
simple P6 format. Indeed, when we sent that, we got some data that has similar structure as the `flag.ctf` file.

After a header, there were raw pixel data (in reversed, BGR order) preceeded often by some small (<0x10) bytes.
Sending `/dev/urandom` as pixels, we received file that was about 1/3 larger than what we sent. On the other hand,
sending `"A" * 256` we got very short file - so there must be some kind of compression.

After some experimentation, we found what the format was - it was preorder representation of quad tree.
The recursive description of a node is:

- if the next byte was `0xf`, what follows is recursive representations of four children nodes
- if the next byte `b` was < 0xf, what follows is three bytes of pixel color, followed by some children nodes.
  For each of the four bits of `b`, if it is 0, make the node fully colored in that saved color and don't parse it,
  otherwise, we have to parse recursive representation of children node.
  
We wrote a parser and tested it on a few simple inputs, then ran it on `flag.ctf` to get `lol.png` and the flag.
