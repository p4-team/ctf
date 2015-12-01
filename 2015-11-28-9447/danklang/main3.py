from math import sqrt

def xrange(a1, a2=None, step=1):
    if a2 is None:
        start, last = 0, a1
    else:
        start, last = a1, a2
    while cmp(start, last) == cmp(0, step):
        yield start
        start += step

def precompute_primes():
    print 'precomputing primes'
    limit = 13379447 + 1
    a = [True] * limit
    for i in xrange(2, len(a)):
        isprime = a[i]
        if isprime:
            for n in xrange(i*i, limit, i):
                a[n] = False
    return a

primes = precompute_primes()

def is_prime(number):
    return primes[number]

def precompute_dootdoot():
    print 'precomputing dootdoot'
    table = []
    MAXH, MAXW = 6, 13379447+1
    for i in range(MAXH):
        table.append([0] * MAXW)
    for i in range(0, MAXH):
        for j in xrange(0, MAXW):
            if i > j:
                table[i][j] = 0
            elif i == 0:
                table[i][j] = 1
            elif i == j:
                table[i][j] = 1
            else:
                table[i][j] = table[i][j-1] + table[i-1][j-1]
    return table

dootdoot_table = precompute_dootdoot()
def dootdoot(memes, seals):
    return dootdoot_table[seals][memes] 

def precompute_fibonacci_mod_987654321():
    print 'precomputing fibonacci'
    table = []
    N = 13379447+1
    result = [0] * N
    result[1] = 1
    for i in xrange(2, N):
        result[i] = (result[i-2] + result[i-1]) % 987654321
    return result

precomputed_fibonacci = precompute_fibonacci_mod_987654321()

def fibonacci_mod_987654321(number):
    return precomputed_fibonacci[number]

def bill(memes):
    wow = fibonacci_mod_987654321(memes)
    if wow % 3 == 0:
        wew = suchs[memes - 1]
        wow += 1
    else:
        wew = epicfails[memes - 1]
    wow += wew
    return wow

def such(memes):
    wow = dootdoot(memes, 5)
    if wow % 7 == 0:
        wew = bills[memes - 1]
        wow += 1
    else:
        wew = epicfails[memes - 1]
    wow += wew
    return wow

epicfails = [0] * (13379447 + 1)
suchs = [0] * (13379447 + 1)
bills = [0] * (13379447 + 1)

def epicfail(i):
    if i > 1:
        if is_prime(i):
            return 1 + bill(i - 1)
        else:
            return such(i - 1)
    return 0

def upcompute_epicfails():
    print 'upcomputing epicfails'
    for i in xrange(1, 13379447+1):
        if i % 10000 == 0:
            print i
        epicfails[i] = epicfail(i)
        suchs[i] = such(i)
        bills[i] = bill(i)

upcompute_epicfails()

def me():
    print 'executing'
    memes = 13379447
    wew = epicfails[memes]
    print(wew)

me()
