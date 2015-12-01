from math import sqrt


def is_prime(number):
    if number % 2 == 0:
        return False
    else:
        for divisor in range(3, int(sqrt(number)) + 1, 2):
            if number % divisor == 0:
                return False
    return True


def epicfail(memes):
    if memes > 1:
        if is_prime(memes):
            return 1 + bill(memes - 1)
        else:
            return such(memes - 1)
    return 0


def dootdoot(memes, seals):
    if seals <= memes:
        if seals == 0:
            return 1
        else:
            if seals == memes:
                return 1
            else:
                return dootdoot(memes - 1, seals - 1) + dootdoot(memes - 1, seals)


def such(memes):
    wow = dootdoot(memes, 5)
    if wow % 7 == 0:
        wew = bill(memes - 1)
        wow += 1
    else:
        wew = epicfail(memes - 1)
    wow += wew
    return wow


def precompute_fibonacci_mod_987654321():
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
        wew = such(memes - 1)
        wow += 1
    else:
        wew = epicfail(memes - 1)
    wow += wew
    return wow


def me():
    memes = 13379447
    wew = epicfail(memes)
    print(wew)

me()
