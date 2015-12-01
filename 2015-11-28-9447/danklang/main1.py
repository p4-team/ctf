from math import sqrt


def fail(memes, calcium):
    dank = True
    if calcium < memes:
        if memes % calcium == 0:
            dank = False
        else:
            wew = fail(memes, calcium + 1)
            dank = wew
    return dank


def epicfail(memes):
    if memes > 1:
        if dank(memes, 2):
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


def brotherman(memes):
    hues = 0
    if memes != 0:
        if memes < 3:
            return 1
        else:
            wew = brotherman(memes - 1)
            hues = wew
            wew = brotherman(memes - 2)
            hues += wew
    return hues % 987654321


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
