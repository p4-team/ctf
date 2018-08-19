# Crypto A5/1 (crypto, 380p, 12 solved)

```
./chatclient 43.224.35.245 3425

one of secret key:

id: manh

key: 0x7f6949db22eeada0 Can you get the secret?
```

In the task we get [lots of sources](crypto01.zip) of the server and client applications.
In short, the server is running a chatbot, which responds with a set of predefined responses, based on how close our input to predefined questions.
The communication is encrypted via A5/1, where the symmetrical shared key is derived from secret key and timestamp.

## Overview

The most important part is the chatbot loop:

```c
A51Comm a51Comm(secretKey, COMM_TIMEOUT, fd, fd);
if (DEBUG) {std::cout << "Enter encrypted mode\n";}
while(1) {
    if (!a51Comm.receive(sInput)) {
        // some error occured
        std::cerr << "Some error occured at receive\n";
        return 1;
    }
    l.log("Got: "); l.log(sInput);
    if (DEBUG) {std::cout << "Got: " << sInput << "\n";}
    if (sInput == "quit") {
        l.log("quit");
        if (DEBUG) {std::cout << "quit\n";}
        break;
    } else if (sInput == "super") {
        superMode = true;
        if (!a51Comm.send(std::string("Enter supper mode!"))) {
            // some error occured
            std::cerr << "Some error occured at send\n";
            return (1);
        }
        l.log("Enter super mode");
        getSuperSecretKey(superSecretKey, argv[3]);
        a51Comm = A51Comm(superSecretKey, COMM_TIMEOUT, fd, fd);
    } else if (sInput == "secret") {
        if (!superMode) {
            if (!a51Comm.send(std::string("You have not entered super mode!"))) {
                // some error occured
                std::cerr << "Some error occured at send\n";
                return (1);
            }
            l.log("Have not entered super mode!");
        } else {
            std::string data = "Secret: ";
            data += getSecretData(argv[4]);
            if (!a51Comm.send(data)) {
                // some error occured
                std::cerr << "Some error occured at send\n";
                return (1);
            }
            l.log("Sent secret");
        }
    } else {
        sResponse = getResponse(sInput, records);
        if (!a51Comm.send(sResponse)) {
            // some error occured
            std::cerr << "Some error occured at send\n";
            return (1);
        }
        l.log(sResponse);
    }
}
```

We can see here that the bot creates encrypted channel using the secret key we provide.
Then it's waiting for commands.
There are 2 interesting special command -> `secret` and `super`.
First one sends us the flag, but it can only be invoked after `super`.
The problem is that `super` triggers changing the encrypted channel to use a different secret key, which we don't know.

We need to invoke `super` command, and then issue `secret` command to get back the flag.
However `super` will change the secret key, and from this point the server won't be able to properly decrypt our messages, and we won't be able to decrypt messages from the server.

## A5/1 stream cipher

Without going into much details, the encryption in the task is using a stream-cipher with keystream derived from secret key and timestamp.
However, the timestamp is changed only every 30 seconds, and there is no notion of any counter (like in CTR mode), so for 30 seconds keystream stays constant!

Timestamps are kept independent, and are sent with the encrypted message.
This means the receiving side uses the timestamp we send to decrypt the data.

## Recovering keystream and forging messages

Since the responses from the server are pre-defined, we can easily recover the keystream, by XORing the encrypted payload with the plaintext message.
We can do this easily, because the message contains also the `length`, and most of the plaintexts have different length, only 24 is repeated.
This means that even if the server changes the encryption secret key after we issue `super` command, we can recover the keystream!

With keystream, we can encrypt any message we want (assuming it's not too long) by simply XORing the message with keystream we recovered.
We know the timestamp server used, so we can send the same one, to make sure the server gets identical keystream and decrypts message correctly.
Server will also keep his own timestamp valid for 30 seconds, so every message will be encrypted with the same keystream, and therefore we can easily decrypt them.

## Getting the flag

The idea of the attack is pretty simple now:

1. Connect to the server.
2. Send `super` message.
3. Send some random message, just so we can get back response from server encrypted with secret key. Repeat this if we get message which is too short (like `Hey`) or is ambigious (like length 24). Save the timestamp used by server.
4. XOR the ciphertext with known plaintext message with the same length to recover keystream.
5. Encrypt `secret` using the keystream by XORing and send the encrypted `secret` with the same timestamp server was using.
6. Save the encrypted `flag` we get.
7. Encrypt `How are you?` using the keystream by XORing and send the encrypted value with the same timestamp server was using. Repeat this until we get back the answer with length 56.
8. XOR the last message ciphertext with `I'm a bot, I don't feel much of anything, how about you?` to recover 56 bytes of keystream.
9. XOR keystream with encrypted flag.

We did this by modifying the client a bit, and writing the rest of the attack in python.
We added a function to the crypto communication library, so we could send already encrypted payloads directly, using the same timestamp as server was using:

```c
bool A51Comm::send_raw_hex(const std::string& data)
{
    std::cout<<"========================== SEND RAW START =========================="<<"\n";
    timestamp = partnerTimestamp;
	uint64_t dataLength = data.length()/2;
    std::cout << "timestamp: " << timestamp << "\n";
    std::cout << "data-length: " << dataLength << '\n';
	const char* payload = hex_to_string(data).c_str();
	// send in form: p64(timestamp) + p64(data-length) + encrypted
	write(fdOut, &timestamp, 8);
	write(fdOut, &dataLength, 8);
	write(fdOut, payload, dataLength);
    std::cout<<"========================== SEND RAW END =========================="<<"\n";
	return true;
}
```

We modified the client a bit as well:

```c
   A51Comm a51Comm(key, COMM_TIMEOUT, sockfd, sockfd);
   
   a51Comm.send(std::string("Hi"));
   a51Comm.receive(input);
   puts(input.c_str());

   a51Comm.send(std::string("super"));
   a51Comm.receive(input);
   puts(input.c_str());
   
   a51Comm.send(std::string("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"));
   a51Comm.receive(input);
   puts(input.c_str());
   
  while(true) {
	   fgets(buffer, BUFF_LEN, stdin);
	   buffer[strcspn(buffer, "\n")] = 0;
	   if (!a51Comm.send_raw_hex(std::string(buffer))) {
		// some error occured
		fprintf(stderr, "Some error occured at send\n");
		exit(1);
		}
		if (!a51Comm.receive(input)) {
			// some error occured
			fprintf(stderr, "Some error occured at receive\n");
			exit(1);
		}
		puts(input.c_str());
   }
```

We automatically send greeting, then enter super mode, and then send lots of `aa` hoping to get a reasonably long response.
After that we start sending raw hex payloads to the server.
We also added logging of the raw hex payloads in the client.

The other part of the attack is:

```python
import codecs

from crypto_commons.generic import xor_string


def main():
    responses = {}
    with codecs.open("records.txt") as input_file:
        for line in input_file:
            if "<response>" in line:
                response = line[line.index("<response>") + 11:-1]
                responses[len(response)] = response
    length = raw_input("len: ")
    payload = raw_input("raw payload: ").decode("hex")
    s = responses[int(length)]
    xor_key = xor_string(s, payload)
    print('secret', xor_string("secret", xor_key).encode("hex").upper())
    print('How are you?', xor_string("How are you?", xor_key).encode("hex").upper())
    flag_ct = raw_input("flag payload")
    how_ct = raw_input("'How are you?' payload")
    xor_key = xor_string(how_ct.decode("hex"), responses[56])
    print(xor_string(flag_ct.decode("hex"), xor_key))


main()
```

This code asks for length and raw hex payload of the server message encrypted after entering super mode.
We copy those values from the console client from the logging we added.
Then it provides us with 2 hex payloads encrypted with the same keystream.
We simply copy those 2 messages to the client.
Then we copy back the payloads we got.
We might need to send the last message a few times until we get back 56-long message.

Flag is 58 bytes long, and keystream we can get is up to 56 bytes, but last flag character is `}` so we need to test only 16 hexdigits to recover full flag.

The simple session is:

```
len: 17
raw payload: 2d1f02a0a463f2bbb6dc4d89ffd3d8ed75
('secret', '175D0CF2A765')
('How are you?', '2C5718A0A363F8F6EFE551D3')
flag payload 375d0cf2a765a7f6c1e24d98eef5d8f420f4d73cb43f8fc8f02eecf2afba70d5a4072f336464fcb658f0b77225dee173e7bd8edbbce890f33a23
'How are you?' payload 2d1f02a0a331ffb9e2a604a5abd9d6ee7cb6c46ce262dbdbae39b9a2ebe320c3fd0d6070383ca7b043e4e67b3498e629b1f19fcca6b286fb
Secret: WhiteHat{63638833b68d6668d67415a749ffff899e7c5c7
```

The final flag is `WhiteHat{63638833b68d6668d67415a749ffff899e7c5c75}`
