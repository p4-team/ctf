#Carder (web, 150 points, solved by 119)

The objective of this challange was to enter valid card numbers with known prefix and suffix.

[This](https://en.wikipedia.org/wiki/Luhn_algorithm) wikipedia describes the method used to validate a card number

A python script that does the job for us:

``` python

import itertools
import requests
import json
import string

#verifyCard

def digits_of(number):
    return [int(i) for i in str(number)]

def luhn_checksum(card_number):
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    total = sum(odd_digits)
    for digit in even_digits:
        total += sum(digits_of(2 * digit))
    return total % 10

def is_luhn_valid(card_number):
    return luhn_checksum(card_number) == 0

#request
url = "http://86dc35f7013f13cdb5a4e845a3d74937f2700c7b.ctf.site:20000/api.php"
data = {
	"action":"start"
}
headers = {
	"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
	"Content-Length":"18",
	"Content-Type":"application/json",
	"Host":"86dc35f7013f13cdb5a4e845a3d74937f2700c7b.ctf.site:20000",
	"Origin":"http://86dc35f7013f13cdb5a4e845a3d74937f2700c7b.ctf.site:20000",
	"Referer":"http://86dc35f7013f13cdb5a4e845a3d74937f2700c7b.ctf.site:20000/"
}

r = requests.get(url)
cookies = r.cookies

r = requests.post(url, data=json.dumps(data), cookies=cookies, headers=headers)

response = r.json()
cards = ['amex','visa','mcard']
lengths = [7, 5, 8]


responseData = {}

for i in range(3):
	start = response["p"+cards[i]]
	ending = response["s"+cards[i]]

	for s in itertools.product(string.digits, repeat=lengths[i]):
		if(is_luhn_valid(start+''.join(s)+ending)):
			print(cards[i])
			print(len(start+''.join(s)+ending))

			responseData["n"+cards[i]] = "".join(s)
			break;



responseData["action"]="validate"
print(json.dumps(responseData))
r = requests.post(url, data=json.dumps(responseData), cookies=cookies, headers=headers)
print(r.text)

```