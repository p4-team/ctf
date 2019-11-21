import itertools

def long_to_bytes(data):
    data = hex(data)
    if len(data) % 2 == 1:
        data = '0' + data
    return data.decode("hex")

def find_factors(N):
    F.<x> = PolynomialRing(Zmod(N), implementation='NTL')   
    i = 0
    while True:
        poly = x*(2**350)+i
        poly = poly.monic()
        roots = poly.small_roots(beta=0.5)
        if roots:
            for root in roots:
                if root != 0:
                    q = int(root)*(2**350)+i
                    p = int(N)/int(q)
                    return p,q
        i=i+1

def cubic_root_prime(c,p):
    F.<x> = PolynomialRing(Zmod(p), implementation='NTL')
    poly = x^3 - c
    return [root for (root,_) in poly.roots()]
        
def cubic_composite_root(c, p, q):
    rootsp, rootsq = cubic_root_prime(c,p), cubic_root_prime(c, q)
    return [CRT([int(rp), int(rq)],[p,q]) for rp, rq in itertools.product(rootsp, rootsq)]

def main():
    N = 420908150499931060459278096327098138187098413066337803068086719915371572799398579907099206882673150969295710355168269114763450250269978036896492091647087033643409285987088104286084134380067603342891743645230429893458468679597440933612118398950431574177624142313058494887351382310900902645184808573011083971351
    p,q = find_factors(N)
    print('primes', p,q)
    c = 78643169701772559588799235367819734778096402374604527417084323620408059019575192358078539818358733737255857476385895538384775148891045101302925145675409962992412316886938945993724412615232830803246511441681246452297825709122570818987869680882524715843237380910432586361889181947636507663665579725822511143923
    for solution in cubic_composite_root(c,p,q):
        flag = long_to_bytes(solution)
        if "ASIS" in flag:
            print(flag)

main()