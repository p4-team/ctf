# Whistleblower (crypto)

In the task we get a [pcap](capture_corrupted.pcap) and link do a webpage. 
The pcap contains interaction between the user and the webpage.

The webpage lets you to input some text and then submit this to the server.
Before the data is sent, a random 128bit key is generated on the client side using Web Crypto API, and sent to the server with some randomly assigned ID using `/key` endpoint.
Next the data are encrypted using this key with AES-CBC and data with IV are submitted to the server via `/data` endpoint.

In the PCAP we can find the ciphertex:

```json
{"ciphertext":"680a2f38d93aaf86e562ab01bb6f7ef9eaf50a2e393bb2262d5d0f32541a7543bf6361220aa7cc1ad1a94efd6ed2fa99aa80c26379316199e70b6c7fbb2d9f81272fce8abf1edf8facce85a8dc89a9eb9d16ca22845545e55460d99c8fe98e383c25b9acc108ea88c7f6cf6666ccc4f56db3886ce0524b185c58aea95e59659c","keyid":"e845799dc6bb731000221f5e20587814"}
```

but the key is not there:

```json
{"key":"corrupted_missing_data_not_here!","id":"e845799dc6bb731000221f5e20587814"}
```

We have only ciphertext and the ID of the key.

If we try to use the webpage we can notice that we get HTTP-500 response from the `/key` endpoint with message:

```json
{
  "message": "key store in read-only maintenance mode", 
  "status": "error"
}
```

So it seems we can't store a new key on the server.
But in the pcap we can see the user could do it, so his key is on the server.

Also when sending data we get HTTP-404 error from `/data` endpoint with message:

```json
{
  "message": "key not found", 
  "status": "error"
}
```

So there is some verification of the keyid we pass.

Finally if we try to submit the same data we got from pcap, we get `message stored` response.
But if we try sending random ciphertext with existing keyid, we get `decryption error`.

There is no special signature added to the data, so decryption failure can come only from incorrect padding.
And this means we have a classic `padding oracle` here (we've described the idea multiple times already in our writeups, so won't go into details here), so we can run:

```python
import requests

from crypto_commons.symmetrical.symmetrical import oracle_padding_recovery

s = requests.session()


def oracle(ct):
    url = "http://web.midnightsunctf.se/data"
    data = {"ciphertext": ct, "keyid": "e845799dc6bb731000221f5e20587814"}
    r = s.post(url, json=data)
    return r.status_code == 200 # return True if padding was correct


def main():
    ct = '680a2f38d93aaf86e562ab01bb6f7ef9eaf50a2e393bb2262d5d0f32541a7543bf6361220aa7cc1ad1a94efd6ed2fa99aa80c26379316199e70b6c7fbb2d9f81272fce8abf1edf8facce85a8dc89a9eb9d16ca22845545e55460d99c8fe98e383c25b9acc108ea88c7f6cf6666ccc4f56db3886ce0524b185c58aea95e59659c'
    oracle_padding_recovery(ct, oracle)


main()
```

And recover full plaintext: `I have discovered a secret flag. It is: midnight{p4dding_padd1ngt0n_th3_0r4cl3} Please do not tell anyone`
