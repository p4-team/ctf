import time

def long_to_bytes(data):
    data = str(hex(long(data)))[2:-1]
    return "".join([chr(int(data[i:i + 2], 16)) for i in range(0, len(data), 2)])
	
def main():
	import codecs
   	with codecs.open("data.txt", "r") as input_file:
		data = [int(c) for c in input_file.readlines()]
		a = [data[i * 4] for i in range(5)]
		b = [data[i * 4+1] for i in range(5)]
		c = [data[i * 4+2] for i in range(5)]
		ns = [data[i * 4 + 3] for i in range(5)]
		t = []
		for n in ns:
			other_moduli = [x for x in ns if x != n]
			t.append(crt([1,0,0,0,0],[n]+other_moduli))
		N = reduce(lambda x,y: x*y, ns)
		e = 5
		P.<x> = PolynomialRing(Zmod(N), implementation='NTL');
		pol = 0
		for i in range(5):
			pol += t[i]*((a[i]*x+b[i])^e - c[i])
		dd = pol.degree()
		if not pol.is_monic():
			leading = pol.coefficients(sparse=False)[-1]
			inverse = inverse_mod(int(leading), int(N))
			pol *= inverse
		beta = 1
		epsilon = beta / 7
		mm = ceil(beta**2 / (dd * epsilon))
		tt = floor(dd * mm * ((1/beta) - 1))
		XX = ceil(N**((beta**2/dd) - epsilon))
		roots = pol.small_roots()
		for root in roots:
			print(long_to_bytes(root))
	
main()
