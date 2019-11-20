import itertools

def long_to_bytes(data):
    data = hex(data)[2:-1]
    if len(data) % 2 == 1:
        data = '0' + data
    return data.decode("hex")
def primorial(p):
    q = 1
    s = 1
    while q < p:
        r = next_prime(q)
        if r <= p:
            s *= r
            q = r
        else:
            break
    return s

def get_divs():
    current_a = 2 ** 6 - 1
    a = []
    while len(bin(current_a)[2:]) <= 9:
        current_a = next_prime(current_a)
        a.append(current_a)
    print(a)
    current_b = 2 ** 1 - 2
    b = []
    while len(bin(current_b)[2:]) <= 5:
        current_b = next_prime(current_b)
        b.append(current_b)
    print(b)
    ps = [primorial(p) for p in a]
    qs = [primorial(q) for q in b]
    divs = []
    for (p, q) in itertools.product(ps, qs):
        divs.append(p / q)
    potential_divs = []
    for d in divs:
        if 475 < len(bin(d)[2:]) < 478:
            potential_divs.append(d)
    return map(int, potential_divs)

def decrypt_flag(N, ct, potential_divs):
    F.<x> = PolynomialRing(Zmod(N), implementation='NTL')
    for d in potential_divs:
        print('testing',d)
        for r in range(10**3, 3*10**3, 2):
            poly = x * d - r
            poly = poly.monic()
            roots = poly.small_roots(beta=0.5,X=2**50)
            if len(roots)>0:
                print(roots)
                p = int(roots[0]*d-r)
                q = int(int(N)/int(p))
                phi = (p-1)*(q-1)
                print(phi)
                d = inverse_mod(65537,phi)
                decrypted = pow(ct,int(d),N)
                print(decrypted)
                return long_to_bytes(int(decrypted))

def main():
    N = 129267954332200676615739227295907855158658739979210900708976549380609989409956408435684374935748935918839455337906315852534764123844258593239440161506513191263699117749750762173637210021984649302676930074737438675523494086114284695245002078910492689149197954131695708624630827382893369282116803593958219295071
    ct = 123828011786345664757585942310038992331055176660679165398920365204623335291878173959876308977115607518900415801962848580747200997185606420410437572095447682798017319498742987210291931673054112968527192210375048958877146513037193636705010232608708929769672565897606711155251354598146987357344810260248226805138
    potential_divs = get_divs()
    print(decrypt_flag(N, ct, potential_divs))

main()

