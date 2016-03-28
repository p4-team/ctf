## Death Sequence (PPC-M)
	tl;dr use matrixes with fastpow to get the desired results in O(logn) time

In this chall, we're given a series of numbers:

`1 1 1 1 10 46 217 1027 4861 23005 108874 515260 2438533 11540665`

It turns out that each numbers satisfies such formula that: inline equation:

`Fn = F(n-1) * 4 + F(n-2) * 3 + F(n-3) * 2 + F(n-4)`

This looks strangely fimilar to Fibonacii definition and we know, that we can calculate n'th fibonacii number in O(logn) time by using fast matrix exponentiation and [Q-matrix](http://mathworld.wolfram.com/FibonacciQ-Matrix.html) 

After a **lot** of thought, we came up with a solution: 

Declare *init* matrix as: 

|**4**|**1**|**0**|**0**|
|:--:|:--:| :--:| :--:|
|**3**|**0**|**1**|**0**|
|**2**|**0**|**0**|**1**|
|**1**|**0**|**0**|**0**|

And *begin* matrix as:

|**1**|**1**|**1**|**1**|
|:--:|:--:| :--:| :--:|
|**1**|**1**|**1**|**0**|
|**1**|**1**|**0**|**0**|
|**1**|**0**|**0**|**0**|


If we raise the begin matrix to the power of n and then multiply the init matrix with the result we'll get nth (more or less*) desired number in the left top record. 

	* We'll actually get n+4th number so we have to subtract the offset

Of course, if n is more than 10 we'll start getting really big results, so we have to modulo the field during multiplication. 

The sum was a little bit trickier, write down Fn, F(n-1), F(n-2), F(n-3) and F(n-4) then recognise common paterns and you get:

`Sn = (F(n+4)-3F(n+3)-6F(n+2)-8F(n+1)+16)/9`

Wrapping that all up we get [this](solve.py) scripts which allows us to get the flag: `CTF-BR{It-wAs-jUsT-a-ReCURsIVe-SequenCE-to-BE-coded-In-LOGN-XwmIBVyZ5QEC}`


