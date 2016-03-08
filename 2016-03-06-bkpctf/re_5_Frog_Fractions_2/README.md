## Frog Fractions 2(reversing, 5 points, 65 solves)
	Turns out Frog Fractions 2 is not battletoads
We're given a 64bit elf file, let's start by disassembling it and describing important points in the program.

The program uses a library called libgmp to handle big numbers, it makes the debugging less friendly. 

After analysing the binary come we come up with a replacement script in python:

```python
data = [] #scraped data array from binary
primes = [] #init primes somewhere
v11 = 1019
line = "A sample line input" #our input

def factor_print(a1):
	v4 = a1
	for x in range(200):
		c = 0
		while(v4 % primes[x] == 0):
			v4 = v4/primes[x];
			c = c+1
		if(c != 0):
			sys.stdout.write(chr(c))
	print

for i in range(len(line)):
	v11 = v11* pow(primes[i], ord(line[i]))
j =0
while(j < len(data)/2):
	v6 = data[j*2]
	v7 = data[j*2+1]

	v10 = v11*v6
	if(v10 % v7 == 0): 
		v11 = v10/v7
		j = 0
	else:
		j = j+1
factor_print(v11)
```

While searching through the binary we stumble into two big, interesting integers: 62834...(6955 chars) and 50209...(8423 chars).

What's interesting about them is that if we run them through our `factor_print` function we get the 2 messages available:

`Nope!  You need to practice your fractions!`

`Congratulations!  Treat yourself to some durians!`

So we need to find a line that reproduces the second output message, we do that by reversing the function:

```python
def crack(v11):
	j = 0
	while(j < len(data)/2):
		v7 = data[j*2]
		v6 = data[j*2+1]

		v10 = v11*v6
		if(v10 % v7 == 0): 
			v11 = v10/v7
			j = 0
		else:
			j = j+1
	factor_print(v11)
```

Which gives us the desired output: `KEY{(By the way, this challenge would be much easier with a cybernetic frog brain)}`

The full source is available [here](https://gist.github.com/nazywam/0634494b4b1c0ffd46a3)
