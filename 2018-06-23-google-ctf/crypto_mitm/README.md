# MITM (crypto, 243p, 34 sovled)

In the task we get [server code](challenge.py) and endpoint to connect to.

The task is a classic Man-In-The-Middle setup between client and server, which are connecting via ECDH protocol using curve25519.
Both parties have pre-shared private secret value, which they use to authenticate.

We can connect to either of them and try to initiate communication, but since we don't know the secret, we will fail authentication.
The most important part of the code is the handshake:

```python
def Handshake(password, reader, writer):
  myPrivateKey = Private()
  myNonce = os.urandom(32)

  WriteBin(writer, myPrivateKey.get_public().serialize())
  WriteBin(writer, myNonce)

  theirPublicKey = ReadBin(reader)
  theirNonce = ReadBin(reader)

  if myNonce == theirNonce:
    return None
  if theirPublicKey in (b'\x00'*32, b'\x01' + (b'\x00' * 31)):
    return None

  theirPublicKey = Public(theirPublicKey)

  sharedKey = myPrivateKey.get_shared_key(theirPublicKey)
  myProof = ComputeProof(sharedKey, theirNonce + password)

  WriteBin(writer, myProof)
  theirProof = ReadBin(reader)

  if not VerifyProof(sharedKey, myNonce + password, theirProof):
    return None

  return sharedKey
```

Both parties send and receive:

- public key
- random 32 bytes nonce
- hmac proof calculated from shared key, pre-shared secret and nonce


We can negotiate a shared key with the other party but we can't calculate the proof since we lack the pre-shared secret.
During the handshake client and server first send their nonce, and then read nonce from the other side, so we could send the same nonce they provided, and therefore our proof would be identical to their proof, so we could re-send this one too.
But the code prevents this:
```python
  if myNonce == theirNonce:
    return None
```

We could forward the parameters between client and server, and it would pass authentication, but we won't know the shared secret value, so we won't be able to encrypt/decrypt communication.
If we could negotiate a shared secret with both sides, but somehow force the shared secret to be identical in both cases, we could forward nonces and proofs between client and server, and get authenticated, while actually having access to the shared secret.
The question is if this is even possible?
Shared secret is based on the private key of the other side, and public key we provide.
Mathematically it is possible to provide such public key curve points, for which the private keys of server and client would give identical vlaues, however it would be hard to do, not knowing private keys.
However, there might be some special points for that.
The code proves it is by:
```python
  if theirPublicKey in (b'\x00'*32, b'\x01' + (b'\x00' * 31)):
    return None
```

If we check what happens for those two public keys we can see that code:
```python
def zeroSecret():
    import hashlib
    from curve25519 import Private, Public

    myPrivateKey = Private()
    public_test = ['\1'+('\0'*31),
                   '\0'+('\0'*31)]
    for key in public_test:
        pub = Public(key)
        print(myPrivateKey.get_shared_key(pub, hashlib.sha256)).hexdigest()
```

Prints out identical shared secret value - `66687aadf862bd776c8fc18b8e9f8e20089714856ee233b3902a591d0d5f2925`
If we read a bit about curve25519 we can find https://cr.yp.to/ecdh.html and there:

```
There are some unusual non-Diffie-Hellman elliptic-curve protocols that need to ensure ``contributory'' behavior. In those protocols, you should reject the 32-byte strings that, in little-endian form, represent 0, 1, 325606250916557431795983626356110631294008115727848805560023387167927233504 (which has order 8), 39382357235489614581723060781553021112529911719440698176882885853963445705823 (which also has order 8), 2^255 - 19 - 1, 2^255 - 19, 2^255 - 19 + 1, 2^255 - 19 + 325606250916557431795983626356110631294008115727848805560023387167927233504, 2^255 - 19 + 39382357235489614581723060781553021112529911719440698176882885853963445705823, 2(2^255 - 19) - 1, 2(2^255 - 19), and 2(2^255 - 19) + 1
```

If we now test other values presented here, for example `long_to_bytes(39382357235489614581723060781553021112529911719440698176882885853963445705823)[::-1]` we get the same shared secret value!

This means we can send this public key point to both client and server, and shared secret for both channels will be the same.
We can therefore simply forward nonces and proofs between them, and authenticate.

The modified handshake for us is:
```python
from curve25519 import Private, Public
from crypto_commons.generic import long_to_bytes

def riggedHandshake(server, client):
    zeroPublicKey = long_to_bytes(39382357235489614581723060781553021112529911719440698176882885853963445705823)[::-1]

    print("Rigging handshake")
    clientPublicKey = Public(readBin(client))
    print("Client key = "+str(clientPublicKey))
    clientNonce = readBin(client)
    print("Client nonce = " + clientNonce.encode("hex"))

    serverPublicKey = Public(readBin(server))
    print("Server key = " + str(serverPublicKey))
    serverNonce = readBin(server)
    print("Server nonce = " + serverNonce.encode("hex"))

    print("Sending to server")
    writeBin(server, zeroPublicKey)
    writeBin(server, clientNonce)

    print("Sending to client")
    writeBin(client, zeroPublicKey)
    writeBin(client, serverNonce)

    serverProof = readBin(server)
    clientProof = readBin(client)
    print("Server proof = "+serverProof.encode("hex"))
    print("Client proof = "+clientProof.encode("hex"))

    print("Forwarding proofs")
    writeBin(server, clientProof)
    writeBin(client, serverProof)

    return Private().get_shared_key(Public(zeroPublicKey))
```

And it gives us authenticated channels for client and server, and shared secret.

Combined with the code:
```python

from binascii import hexlify
from binascii import unhexlify

import nacl.secret
from crypto_commons.netcat.netcat_commons import nc, receive_until, send

def readBin(socket):
    try:
        data = receive_until(socket, "\n")[:-1]
        return unhexlify(data)
    except:
        print('error', data)


def writeBin(socket, data):
    send(socket, hexlify(data))


def main():
    url = "mitm.ctfcompetition.com"
    port = 1337
    server = nc(url, port)
    client = nc(url, port)
    send(server, "sS")
    send(client, "cC")
    sharedKey = riggedHandshake(server, client)
    mySecretBox = nacl.secret.SecretBox(sharedKey)

    print(mySecretBox.decrypt(readBin(server)))
    writeBin(server, mySecretBox.encrypt("getflag"))
    print(mySecretBox.decrypt(readBin(server)))

main()
```

We get:

```
Rigging handshake
Client key = <curve25519.keys.Public instance at 0x7f9a019ecea8>
Client nonce = bfaf0c97e8030e0bc59f6371438ea348bd51ad60127302d5ccd9a08add8190d3
Server key = <curve25519.keys.Public instance at 0x7f9a019f42d8>
Server nonce = 1b50d096795799effc8e1dbdf5a45e71a612aa0f3ccb60d5d09e94639c128f73
Sending to server
Sending to client
Server proof = 30e2f5990849450ca851bd99cc7b15569167e04c7068fa4383d25469e32916ef
Client proof = 3ae7e589e04fec309f5c6a235c35d70ff2cd031d4bc9e1104a3fdbc13e0bd567
Forwarding proofs
AUTHENTICATED
CTF{kae3eebav8Ac7Mi0RKgh6eeLisuut9oP}
```
