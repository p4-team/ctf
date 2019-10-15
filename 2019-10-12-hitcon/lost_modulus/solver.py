import gmpy2

from crypto_commons.generic import long_to_bytes


def find_phi(e, d):
    kfi = e * d - 1
    k = kfi / (int(d * 3))
    print('start k', k)
    while True:
        fi = kfi / k
        try:
            d0 = gmpy2.invert(e, fi)
            if d == d0:
                yield fi
        except:
            pass
        finally:
            k += 1


def solve_for_phi(ipmq, iqmp, possible_phi):
    a = iqmp - 1
    b = ipmq + iqmp - 2 - possible_phi
    c = ipmq * possible_phi - possible_phi
    delta = b ** 2 - 4 * a * c
    if delta > 0:
        r, correct = gmpy2.iroot(delta, 2)
        if correct:
            x1 = (-b - r) / (2 * a)
            x2 = (-b + r) / (2 * a)
            if gmpy2.is_prime(x1 + 1):
                q = x1 + 1
                p = possible_phi / x1 + 1
                return p, q
            elif gmpy2.is_prime(x2 + 1):
                q = x2 + 1
                p = possible_phi / x2 + 1
                return p, q


def main():
    e = 1048583
    d = 20899585599499852848600179189763086698516108548228367107221738096450499101070075492197700491683249172909869748620431162381087017866603003080844372390109407618883775889949113518883655204495367156356586733638609604914325927159037673858380872827051492954190012228501796895529660404878822550757780926433386946425164501187561418082866346427628551763297010068329425460680225523270632454412376673863754258135691783420342075219153761633410012733450586771838248239221434791288928709490210661095249658730871114233033907339401132548352479119599592161475582267434069666373923164546185334225821332964035123667137917080001159691927
    ipmq = 22886390627173202444468626406642274959028635116543626995297684671305848436910064602418012808595951325519844918478912090039470530649857775854959462500919029371215000179065185673136642143061689849338228110909931445119687113803523924040922470616407096745128917352037282612768345609735657018628096338779732460743
    iqmp = 138356012157150927033117814862941924437637775040379746970778376921933744927520585574595823734209547857047013402623714044512594300691782086053475259157899010363944831564630625623351267412232071416191142966170634950729938561841853176635423819365023039470901382901261884795304947251115006930995163847675576699331
    ct = 0x32074de818f2feeb788e36d7d3ee09f0000381584a72b2fba0dcc9a2ebe5fd79cf2d6fd40c4dbfea27d3489704f2c1a30b17a783baa67229d02043c5bc9bdb995ae984d80a96bd79370ea2c356f39f85a12d16983598c1fb772f9183441fea5dfeb5b26455df75de18ce70a6a9e9dbc0a4ca434ba94cf4d1e5347395cf7aafa756c8a5bd6fd166bc30245a4bded28f5baac38d024042a166369f7515e8b0c479a1965b5988b350064648738f6585c0a0d1463bd536d11a105bb926b44236593b5c6c71ef5b132cd9c211e8ad9131aa53ffde88f5b0df18e7c45bcdb6244edcaa8d386196d25297c259fca3be37f0f2015f40cb5423a918c51383390dfd5a8703
    for potential_phi in find_phi(e, d):
        res = solve_for_phi(ipmq, iqmp, potential_phi)
        if res:
            p, q = res
            n = p * q
            print(long_to_bytes(pow(ct, d, n)))
            break


main()


def sanity():
    from Crypto.Util.number import getPrime
    e = 65537
    bits = 1024
    p = getPrime(bits)
    q = getPrime(bits)
    ipmq = gmpy2.invert(p, q)
    iqmp = gmpy2.invert(q, p)
    phi = (p - 1) * (q - 1)
    d = gmpy2.invert(e, phi)
    n = p * q

    X = p - 1
    Y = q - 1
    assert (phi == X * Y)
    assert (phi == ipmq * X + ipmq + iqmp * Y + iqmp - 1 - (X + 1 + Y))
    assert (phi == ipmq * (phi / Y) + ipmq + iqmp * Y + iqmp - 1 - ((phi / Y) + 1 + Y))
    assert (phi * Y == ipmq * phi + ipmq * Y + iqmp * Y ** 2 + iqmp * Y - Y - (phi + Y + Y ** 2))
    assert (phi * Y == Y ** 2 * (iqmp - 1) + Y * (ipmq + iqmp - 1 - 1) + ipmq * phi - phi)
    assert (Y ** 2 * (iqmp - 1) + Y * (ipmq + iqmp - 2 - phi) + ipmq * phi - phi == 0)
    assert ((p, q) == solve_for_phi(ipmq, iqmp, phi))

    for potential_phi in find_phi(e, d):
        res = solve_for_phi(ipmq, iqmp, potential_phi)
        if res:
            assert ((p, q) == res)
            break

# sanity()
