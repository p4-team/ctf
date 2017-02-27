# slow (cloud 450)

> Maybe if you run this on a big enough, strong enough computer for long enough,
> you'll get it to print the flag!

> The NSA might have a computer suitable for this :)

This task, although it was in the `cloud` category, was more of an reverse engineering one.

The main function was very simple, just `printf("FLAG{%lu}\n", real_main());`. So we had to find out what that function
returns. Note that we couldn't simply run the binary - it throws `std::bad_alloc` immediately.

Reverse engineering of the biggest function of the binary shows it is very sequential and repetitive code.
First, it allocates two vectors of complex numbers - their size was 1LL<<48 though, far too much too allocate,
let alone initialize.

After initialization (0+0i everywhere, and 1+0i in the very first cell), there was a couple of calls to a certain function -
I called it `split`. It took one parameter, and what it did was adding, subtracting, and multiplying some numbers in the 
vector. After reading some quantum mechanics articles (and solving the other quantum challenge), I believe it applied 
Hadamard gate to the system - not that it was important to the solution... One thing I noticed after reimplementation 
of the function in C++, is that the number of non-zero cells doubles after each call to `split`. This property will be
important later on.

After around 20 or so `split`s, the only remaining repeating patterns were of one of two types: `swap`,
taking two arguments (say `a` and `b`), and swapping each index of array with `a`th bit set, with its corresponding cell,
with bit `b` flipped. I believe this is controlled swap gate.

The other repeating function was `rotate`, which multiplied each cell with certain bit set by (0+1i), or simply shift phase
by 90 degrees.

Finally, the code calculated a kind of checksum of the vector and returned the result to be printed as flag.

Unfortunately, some of the calls to the functions I mentioned were inlined, which made it much more difficult to see what
is going on. In the end, I wrote a dirty Python script to scrape the called functions, with heuristics to find the inlined
ones too (and their parameters).

Still, we had to somehow run the code. I remind that there was a huge vector with 1LL<<48 cells. However, we can notice
both `swap` and `rotate` do not change the number of non-zero cells: the `swap` just swaps them, and `rotate` multiplies.
That means after all 22 of the `split`s, we had only 1<<22 non-zero cells - the vector was extremely sparse. For this reason,
we did not have to waste computing power to iterate over all the cells - just the ones that had effect on the state (the
non-zero ones). We implemented it in C++ using `unordered_map`s, being careful to remove cells with zero in them after
each transformation - otherwise, the whole map would quickly fill up and slow down. See `map.cpp` for the source code.

Running it took around 10-15 minutes, and printed the correct flag.
