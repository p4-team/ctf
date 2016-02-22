## The hidden message (Misc, 50p)

	My friend really can't remember passwords. So he uses some kind of obfuscation. Can you
	restore the plaintext?
	
###ENG
[PL](#pl-version)

This was a really trivial task. Given text consisted of base-8 numbers, which interpreted as
ASCII yielded base64-encoded string. Reversing the encoding, we get the flag.

###PL version

Proste zadanie, polegające na zinterpretowaniu liczb w systemie ósemkowym jako kody znaków ASCII,
a następnie odkodowanie powstałego tekstu za pomocą base64.
