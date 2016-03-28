import sys
from itertools import product
import ssl, socket


def multiply(matr_a, matr_b):
    """Return product of an MxP matrix A with an PxN matrix B."""
    cols, rows = len(matr_b[0]), len(matr_b)
    resRows = xrange(len(matr_a))
    rMatrix = [[0] * cols for _ in resRows]
    for idx in resRows:
        for j, k in product(xrange(cols), xrange(rows)):
            rMatrix[idx][j] += matr_a[idx][k] * matr_b[k][j]
            rMatrix[idx][j] %= 10**9
    return rMatrix

def fastPow(x, n):
	if(n == 0):
		return [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
	if(n % 2 == 1):
		return multiply(fastPow(x, n-1), x)
	else:
		a = fastPow(x, n/2)
		b = multiply(a,  a)

		return b

class Connect(object):
    def __init__(self, host, port):
        self.context = ssl.create_default_context()
        self.conn = self.context.wrap_socket(
            socket.socket(socket.AF_INET),
            server_hostname=host)
        self.conn.connect((host, port))
        self.f = self.conn.makefile('r+b', 0)
    def __enter__(self):
        return self.f
    def __exit__(self, type, value, traceback):
        self.f.close()

init = [[1, 1, 1, 1],[1, 1, 1, 0],[1, 1, 0, 0],[1, 0, 0, 0]]
begin = [[4, 1, 0, 0], [3, 0, 1, 0], [2, 0, 0, 1], [1, 0, 0, 0]]

def getN(n):
	ans = fastPow(begin, n)
	ans = multiply(init, ans)
	return ans[0][0]

def suma(n):
	a = getN(n+4)
	b = 3*getN(n+3)
	c = 6*getN(n+2)
	d = 8*getN(n+1)

	return (a-b-c-d+16 +20*(10**9)) * 888888889


with Connect('programming.pwn2win.party', 9001) as f:
	for line in f:
		line = line.strip()
		print('received: %s' % line)

		n = int(line)
		#n = 6412110170302000
		n-=4

		if line.startswith('CTF-BR{') or line == 'WRONG ANSWER':
			break

		f.write('%09d %09d\n' % (getN(n)%(10**9), (suma(n))%(10**9)))
		print('sent: %d %d \n' % (getN(n)%(10**9), (suma(n))%(10**9)))



	
