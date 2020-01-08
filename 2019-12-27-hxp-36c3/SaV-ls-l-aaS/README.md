## SaV-ls-l-aaS
SaV-ls-l-aaS (aka. Sign and Verify ls -l as a service) is a task that consists of two independent services.
First one is "frontend" written in go. Frontend exposes api for user to interact with, proxying only correct requests to the backend.
Backend is a single php file that implements Sign and Verify actions using md5 with RSA. It is accesible only from localhost, in this case, only by frontend application.
This prevents signing custom messages by calling php service directly.

Go frontend exposes following API endpoints:
- `/ip` - returning ip of the caller
- `/sign` - allows for signing of commands, although the only command that you are allowed to sign is `ls -l`
- `/exec` - verifies signed command, if this succeeds, command is executed on the server side

Executing `ls -l` command through API gives us a listing with one file called `flag.txt`.

We can easily see that our goal is to sign `cat flag.txt` command in order to read the flag.

### Signing scheme
Signing goes as follows:
- Make a POST request to `/sign` in the format of `ip=192.168.1.1&cmd=ls -l`, where `192.168.1.1` can be any ip that is accepted by the `net.ParseIP` function from go and must be equal to ip of the caller (represenatations may be different but they have to resolve to the same address - this is important later on).  As far as `cmd` goes, there is no way to bypass the whitelist check in any way. Verification code for both parameters below:

```go
ip = r.PostFormValue("ip")
signIP := net.ParseIP(ip)
if signIP == nil || !signIP.Equal(remoteAddr) {
    fmt.Fprintln(w, "lol, not ip :>")
    return
}

cmd := r.PostFormValue("cmd")
if cmd != "ls -l" {
    fmt.Fprintln(w, "lol, nope :>")
    return
}
```
- Message to be signed is hashed with sha1 and converted to json, format of the signed message is `ip|cmd`
```go
msg := ip + "|" + cmd
digest := sha1.Sum([]byte(msg))

b := new(bytes.Buffer)
err = json.NewEncoder(b).Encode(string(digest[:]))
```
- Hashed message is sent to the backend to be signed with secret private RSA key
```go
resp, err := http.Post("http://127.0.0.1/index.php?action=sign", "application/json; charset=utf-8", b)
```
- Backend uses md5 with RSA algorithm to sign the message
```php
define('ALGO', 'md5WithRSAEncryption');
$d = json_decode(file_get_contents('php://input'), JSON_THROW_ON_ERROR);

error_log(print_r($d, TRUE)); 
if ($_GET['action'] === 'sign'){
    $pkeyid = openssl_pkey_get_private("file:///var/www/private_key.pem");
    openssl_sign($d, $signature, $pkeyid, ALGO);
	echo json_encode(base64_encode($signature));
    openssl_free_key($pkeyid);
}
```
- Signature is then prepended to the message that was signed and returned through frontend to the caller

We can summarize the signing scheme by `RSA(md5(sha1("ip|cmd")), priv_key)ip|cmd`

### Verify scheme
Verification is implemented exactly as one would expect.
First 172 bytes of the message are used as a signature, rest is used as message. 
Split on `|` determines what is the value of ip and what cmd was signed.

### The bug
The bug wasn't easy to spot. Especially if someone is not working with go on the daily basis.
Bug was placed in the second step of signing scheme presented earlier.

```go
msg := ip + "|" + cmd
digest := sha1.Sum([]byte(msg))

b := new(bytes.Buffer)
err = json.NewEncoder(b).Encode(string(digest[:]))
```
First observation is that `sha1.Sum` function returns `[20]byte` array.
So `string(digest[:])` has to convert type from bytes in `digest` to string. By default this is done using `utf8` encoding.
The question is how does decoder behave when incorrect utf8 sequence is encountered. It turns out that no error is thrown. 
In place of bytes that couldn't be decoded - **REPLACEMENT CHARACTER `\xfffd` is inserted**. 
This behaviour is equivalent to the python `replace` option 
```python
b"something".decode("utf-8", "replace")
```
We can see exactly which bytes can't be decoded by looking at `utf8.Valid` function https://golang.org/src/unicode/utf8/utf8.go?s=12830:12855#L439.

Good approximation can be determined by looking at the array found in the same file.

```go
// first is information about the first byte in a UTF-8 sequence.
var first = [256]uint8{
	//   1   2   3   4   5   6   7   8   9   A   B   C   D   E   F
	as, as, as, as, as, as, as, as, as, as, as, as, as, as, as, as, // 0x00-0x0F
	as, as, as, as, as, as, as, as, as, as, as, as, as, as, as, as, // 0x10-0x1F
	as, as, as, as, as, as, as, as, as, as, as, as, as, as, as, as, // 0x20-0x2F
	as, as, as, as, as, as, as, as, as, as, as, as, as, as, as, as, // 0x30-0x3F
	as, as, as, as, as, as, as, as, as, as, as, as, as, as, as, as, // 0x40-0x4F
	as, as, as, as, as, as, as, as, as, as, as, as, as, as, as, as, // 0x50-0x5F
	as, as, as, as, as, as, as, as, as, as, as, as, as, as, as, as, // 0x60-0x6F
	as, as, as, as, as, as, as, as, as, as, as, as, as, as, as, as, // 0x70-0x7F
	//   1   2   3   4   5   6   7   8   9   A   B   C   D   E   F
	xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, // 0x80-0x8F
	xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, // 0x90-0x9F
	xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, // 0xA0-0xAF
	xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, // 0xB0-0xBF
	xx, xx, s1, s1, s1, s1, s1, s1, s1, s1, s1, s1, s1, s1, s1, s1, // 0xC0-0xCF
	s1, s1, s1, s1, s1, s1, s1, s1, s1, s1, s1, s1, s1, s1, s1, s1, // 0xD0-0xDF
	s2, s3, s3, s3, s3, s3, s3, s3, s3, s3, s3, s3, s3, s4, s3, s3, // 0xE0-0xEF
	s5, s6, s6, s6, s7, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, xx, // 0xF0-0xFF
}
```
If first byte is any of the position where `xx` is present, decoding will fail.
We can observe that this is around 1/4-1/3 of all values. In reality this is a bit bigger number due to existence of wrong sequences following correct first byte.

All of this means that bytes of the resulting sha1 hash which are invalid utf8 sequences, are gonna be converted to REPLACEMENT CHARACTER `\xfffd`.

### Exploit
The bug gives some collision potential, finding two different messages(ideally one with `ls -l` and one with `cat flag.txt`) that hash to 20*`\xfffd` would result in the same signature.

To find a collision we have to generate a lot of messages. This can be done thanks to many represenations of single IP address, especially with use of ipv6(although with ipv4 it works fine as well). 

IP `192.168.1.1` can be represented as `::0:0:0:0:ffff:192.168.1.1`, `::0:0:0:00:ffff:192.168.1.1`, `::0:0:0:000:ffff:192.168.1.1`...

This allows us to create as many messages as we want.
So our goal is to find such `ipX` and `ipY` which both resolve to our ip and `ipX|ls -l`, `ipY|cat flag.txt` hash to 20*`\xfffd`.

This allows us to then send a first message, get the signature, prepend to the latter one and `/exec` it.
For that purpose we wrote [go program](main.go).
