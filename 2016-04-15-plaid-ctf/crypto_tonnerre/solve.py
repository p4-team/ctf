from pwn import *
import hashlib

def H(P):
    return hashlib.sha256(P).hexdigest()

def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError
    return x % m
def tostr(A):
    return hex(A)[2:].strip('L')

v=0xebedd14b5bf7d5fd88eebb057af43803b6f88e42f7ce2a4445fdbbe69a9ad7e7a76b7df4a4e79cefd61ea0c4f426c0261acf5becb5f79cdf916d684667b6b0940b4ac2f885590648fbf2d107707acb38382a95bea9a89fb943a5c1ef6e6d064084f8225eb323f668e2c3174ab7b1dbfce831507b33e413b56a41528b1c850e59
N=168875487862812718103814022843977235420637243601057780595044400667893046269140421123766817420546087076238158376401194506102667350322281734359552897112157094231977097740554793824701009850244904160300597684567190792283984299743604213533036681794114720417437224509607536413793425411636411563321303444740798477587L
g=9797766621314684873895700802803279209044463565243731922466831101232640732633100491228823617617764419367505179450247842283955649007454149170085442756585554871624752266571753841250508572690789992495054848L

# g=2**671
#
# Given pS, N, v
# Knowing pS=g**r % N
# Find (pC*v)**r % N for pC chosen by you.
#
# Observation:
# If g**2=pC*v (mod N), then constraints are fulfilled.
# Then pC=(g**2 * modinv(v, N)) % N

pC=(g**2 * modinv(v,N))%N

context.log_level="DEBUG"

r=remote("tonnerre.pwning.xxx", 8561)
r.sendline("get_flag") # Username known from SQLi
r.sendline(tostr(pC))

r.recvline() # Welcome.
r.recvline() # Salt.
res=int(r.recvline(),16) # Residue=(pS+v)%N
pS=(res-v+N)%N

key=H(tostr(pow(pS, 2, N)))
r.sendline(H(tostr(res)+key))

r.recvall()
