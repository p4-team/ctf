# White Box Unboxing 

> Here is a binary implementing a cryptographic algorithm. You provide an input and it 
> produces the corresponding output. Can you extract the key?

We were given binary implementing, as it turns out, whitebox implementation of AES. For a while I tried
standard methods of breaking it, but in the end used `deadpool` library implementing various DFA attacks.
I have no idea how they work, but they solved the puzzle. Scripts attached.

-- akrasuski1
