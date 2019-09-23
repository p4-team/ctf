# Looking glass (web/crypto, 330p, 18 solved)

In the challenge we get access to a go webservice behind some wasm interface.
We can ignore the wasm part and focus solely on the [go part](main.go) and on [protobuf interface](command.proto).

The logic of the application is simple:

1. User can send messages via protobuf
2. The message can be either a tracert or ping request
3. User provides address to query (or not, since there are default values)
4. Address is filtered to make sure there is no malicious payload, especially that the commands are run without any shellescape, so are prone to command injection by simply sending `; your_command`'

The twist is that the application has a cache of know requests.
If request is in the cache, then filtering of address is not performed anymore.
The cache is based on `md5` of the request payload.

The vulnerability is of course hash collision.
If we could create two requests with identical md5, but one with a nice address which will not get rejected, and the second one with malicious shell injection, we will be able to gain RCE and steal the flag.

While md5 is generally considered broken, it's not yet possible to make such strong collision though.
It's easy to make a random collision with hashclash and possible to make collisions with similar prefixes.
We also have to take into consideration protobuf.
It will reject requests padded with some weird bytes, and hash collisions always contain those!

It took us a while to figure out how to bypass the protobuf problem.
While we were going through the documentation we noticed that protobuf praises itself to be backward/future compatible.
You can add new fields to the packet definition, and a server which doesn't expect them (because has old version of the interface definition) will simply ignore them!
This means that we could pretend that all the weird bytes added by hash collision are simply a new `bytes` field, and the server will accept this and ignore them.
If we look into the provided protobuf interface definition we can see that ping and tracert commands have only fields 1,2,3, so if we provide a field of any higher number it will get ignored.

Still, we have to somehow create a payload for the collision.
While looking for the best available options we found UniColl with a very neat feature -> it can create a collision with identical 9 byte prefix, then LSB flip in the 10th byte, then common suffix of 10 bytes and then collision blocks.

The idea was to use this single bitflip in 10th byte to change the protobuf packet in such a way, that our payload would be interpreted differently.

Our final target payload is `\n~"\x00"\x00"\x00"\x00"\n\t;nl /flag"h` with collision bitflip on the last `\x00` flipping to `\x01`.
The shell injection payload is `\t;nl /flag` where `nl` works as `cat`.
The idea behind this payload is:

- `\n` is constant starting byte of the protobuf message
- `~` is the length of the rest of the packet
- `"` is in binary `00100010`. Last 3 bits denote the "type" of the field, and in this case it's `010` so decimal `2` which means string/bytes field. First 5 bits are for the field number, so `00100` in our case it's field number `4`, which doesn't exist in the given protocol definition, so it will be ignored by the server.
- `\x00` is the length of the string payload, in this case 0.
- So the `"\x00` are just "padding" becase we don't care about the 9 bytes before the collision bitflip, but we need to put something there.
- `"h` at the end is simply there to convince protobuf to ignore all bytes after that, again `"` is definition of string field number 4 and `h` is just the number 104 which is the length of the collision bytes added by hash collision.

The key part of the payload is: `"\x00"\n\t;nl /flag`

This `"\x00` is interesting, because the flip happens on `\x00`. 
In the first version the length of the string is `0` in the other case the length is `1`.
Let's consider what happens in both cases:

## Case `\x00`

- We again have `"\x00` so ignored string field of length 0
- Then protobuf reads `"\n\t;nl /flag` which is simply another ignored string field, this time of length 10, which simply means protobuf will ignore this whole part

Such payload will pass all the checks in the application, because we didn't provide address at all and default value will be used.
Protobuf will not complain about this message, because we placed all bytes on ignored string field number 4.

## Case `\x01`

- This time we have `"\x01` so ignored string field of length 1, so it will ignore also the character `"` behind.
- Then protobuf reads `\n\t;nl /flag` and the `\n` is now interpreted as field definition, in binary `\n` is `00001010`, so a string field (`010` -> 2), with number `00001` so 1, which happens to be the id number of `address` field. The `\t` defines the field length of 9.
- This means protobuf will now parse `;nl /flag` as address to use for ping!

## Collision

Now the last thing to do is actually run UniColl to get a collision for payload `\n~"\x00"\x00"\x00"\x00"\n\t;nl /flag"h`:

```
$ base64 collision1.bin 
Cn4iACIAIgAiACIKCTtubCAvZmxhZyJoBOabW+Ucv+N3Z3aeA1fsgd7eMHf0W1fcdyw6Ql+5ta7x
1O05JbT4qrUgkje4ZPcLwFWXta75QjR4KlMy6tIf9+uLcwKEpmUDzQ9YZOABqFoVG+v+7acdj9jc
rr8flHO19HD8v2EhZ6A=

$ base64 collision2.bin 
Cn4iACIAIgAiASIKCTtubCAvZmxhZyJoBOabW+Ucv+N3Z3aeA1fsgd7eMHf0W1fcdyw6Ql+5ta7x
1O05JbT4qrUgkje4ZPcLwFSXta75QjR4KlMy6tIf9+uLcwKEpmUDzQ9YZOABqFoVG+v+7acdj9jc
rr8flHO19HD8v2EhZ6A=
```

Send those two requests to the server and read back the flag: `DrgnS{w00T_Md5_1N_2OI9?}`
