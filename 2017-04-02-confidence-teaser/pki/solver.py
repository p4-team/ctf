import base64
import codecs
import hashlib
from time import sleep

from crypto_commons.generic import long_to_bytes
from crypto_commons.netcat.netcat_commons import nc, send
from crypto_commons.rsa.rsa_commons import modinv, get_fi_distinct_primes, rsa

G = 0xe6a5905121b0fd7661e2eb06db9a4d96799165478a0b2baf09836c59ccf4f086bc2a55191ee4bf8b2324f6f53294da244342aba000f7b915861ba2167d09c5569910ae80990c3c79040879d8e16e48219127718d9ff05f71a905041564e9bcb55417b39cdb0b7afc6863ccd10b90ee42f856840e0dd5f8602e49592b58a22d39
P = 0xf2a4ca87978e05b112ef4a16b547c5036cd51fadac0cf967c152e56378c792a45e76e0ebfd62b2b23e94ca3727fbe1ebb308211cf8938c8a735db2de4cd26f0beb53b51fc2a5474bd0d466fc54fce13a4ec2b9840800ecdf337c55105c9b7d702b7f2d20bb3cba16a5948a208f8886ab2eddd1284a5b8ec457bf696be4bbb51b
Q = 0x9821a36da85bf3bcfb379d7cc39f5b6db7a553d5


def h(x):
    return int(hashlib.md5(x).hexdigest(), 16)


def makeMsg(name, n):
    return 'MSG = {n: ' + n + ', name: ' + name + '}'


def simple_sign(name, n, priv):
    k = 5  # dice roll, I swear!
    r = pow(G, k, P) % Q
    s = (modinv(k, Q) * (h(makeMsg(name, n)) + priv * r)) % Q
    return r * Q + s


def read_collision_n(name):
    with codecs.open(name, "rb") as input_file:
        return input_file.read()[8:]


def get_sig(col):
    name = base64.b64encode("test")
    url = "pki.hackable.software"
    port = 1337
    s = nc(url, port)
    send(s, "register:" + name + "," + col)
    sleep(5)
    signature = s.recv(9999)
    return int(signature.strip())


def decode_rsa_signature(n, factors, ct):
    n = int(n.encode("hex"), 16)
    d = modinv(65537, get_fi_distinct_primes(factors))
    return rsa(ct, d, n)


def main():
    n1 = read_collision_n("col1")
    factors1 = [234616432627,
                705869477985961204313551643916777744071330628233585786045998984992545254851001542557142933879996265894077678757754161926225017823868556053452942288402098017612976595081470669501660030315795007199720049960329731910224810022789423585714786440228952065540955255662140767866791612922576360776884260619L]
    # col1 = base64.b64encode(n1)
    # sig1 = get_sig(col1)
    # value cached below
    sig1 = 45254147107316604985838940723873087065648716656505719897465763752188344559259982909946582387581238630810505111702280156530580024162354320922165321462910808027195861156154913029659141369366731116256144166513466262820414101619676170670462164924122480441158287460305618685897536866567703872210447139212329752485

    n2 = read_collision_n("col2")
    factors2 = [119851, 236017,
                5854608817710130372948444562294396040006311067115965740712711205981029362712183315259168783815905208719000197236691607700100836391807927746833977891792631066541406816904680111217125634549418611669208807316369565620310660295144628581977856740654199823679135895590513942858128229967305158632385155587L]
    # col2 = base64.b64encode(n2)
    # sig2 = get_sig(col2)
    # value cached below
    sig2 = 75192947990007542085188766184539371284719071358445557426300109324739891690549237742257214192631557978881958688601121333533557280909118797353696869434142069884160391258848066603116809532123308968051639065681186651011928077675380204482405509591787282691679920144780885427200808239335447140493957969342214523565

    real_signature1 = decode_rsa_signature(n1, factors1, sig1)
    real_signature2 = decode_rsa_signature(n2, factors2, sig2)
    print(real_signature1)
    print(real_signature2)

    k = (h(makeMsg("test", n1)) - h(makeMsg("test", n2))) * modinv(real_signature1 - real_signature2, Q) % Q
    print(k)

    r = real_signature1 / Q
    s = real_signature1 % Q
    private_key = ((s * k) - h(makeMsg("test", n1))) * modinv(r, Q)
    print(private_key)

    admin_sig = simple_sign("admin", "1", private_key)
    name = base64.b64encode("admin")
    n = base64.b64encode("1")
    sig = base64.b64encode(long_to_bytes(admin_sig))
    url = "pki.hackable.software"
    port = 1337
    s = nc(url, port)
    send(s, "login:" + name + "," + n + "," + sig)
    sleep(5)
    flag = s.recv(9999)
    print(flag)
    # DrgnS{ThisFlagIsNotInterestingJustPasteItIntoTheScoreboard}


main()
