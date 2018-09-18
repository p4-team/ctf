# ACME (crypto, 400p)

In the challenge we get a [protocol specs](ACME_Protocol.docx), a [simple client](refClient.py), an [example reference server](refServer.py), and also a [real server binary](server) alongside [runner script](challengeServer.py).

So technically in fact the flag is in the binary we have, but it seems to be packed and protected againts reversing.

We've got here some statelss crypto protocol, which challenges us in order to login and execute commands.
There is `getflag` command, so we just need to properly authenticate.

The idea is that we send login to the server, and the server returns to us `nonce` and encypted challenge cookie, which contains the nonce again, our login and timesatmp.
In order to authenticate we need to send back SHA256 of nonce+password and the cookie again (since protocol is statelss).

The server checks if password is correct, and if it is, we get a ticket, which contains encrypted user identity info (json with some data) plus a timestamp.

Since we have all the data, we could try to somehow modify them.
It's AES-CBC encrypted so we could theoretically to some bitflipping to modify the plaintext.
However, if we notice that the challenge cookie is very similar to the authentication ticket we can skip even this.

The challenge cookie is: `8 bytes nonce + user login + timestamp` and authentication ticket is `json data + timestamp`.
In AES-CBC we can easily just remove first block (the IV) and the cipher will treat the next block as IV, which means effectively we just removed the first block of the plaintext.

So if we send to the server login: `'X' * 8 + '{"user":"x","groups":["admin"]}'`, and remove the first encrypted block, the ciphertext we get decrypts to a perfect ticket.

So we simply run the server, run the client exploit:

```python
def main():
    host = "localhost"
    port = 9999
    username = 'X' * 8 + '{"user":"x","groups":["admin"]}'
    client = Client(host, port)
    client.sendMessage_LogonRequest(username)
    (nonce, challengeCookie) = client.expectMessage_LogonChallenge()
    ticket = b64encode(b64decode(challengeCookie)[16:])
    print(client.execute(ticket, 'getflag'))
```

And recover the flag: `TMCTF{90F41EF71ED5}`
