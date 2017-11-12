# Hack-tac-toe (Web/Crypto)

In the task we have access to a webpage where two players can play tic-tac-toe.
Part of the logic is client-side and part is server side.
We notice right away that there is a cookie `Encrypted_Game_Session` which changes while we play.

By analysing how the cookie changes we can see that for example changing a single letter of player name the cookie changes by a single byte.
This indicates some kind of stream cipher applied over the game state.

However, since nothing else changes it indicates that the keystream stays the same, at least for the current user.
This means if we could retrieve the keystream, we could decrypt the game state and potentially change it however we want.
It is quite simple to recover the keystream following the player name, since keystream is simply XORed with plaintext, and we know the plaintext and we know the position of this plaintext (we can see where the ciphertext changed when we supplied a new player name).

We can:

1. Get the original cookie
2. Set name to 'a'*100
3. Get the new cookie
4. Notice that the difference starts at 112 byte
5. Get bytes [112:(112+100)] from the second cookie and XOR them with 'a'*100 to recover the keystream
6. XOR the keystream with original cookie from position 112

This gives us:

`ayer 1";s:5:"name2";s:8:"Player 2";s:5:"score";i:0;s:6:"score2";i:0;}`

Which is part of the decrypted cookie.
Here we were a bit confused what to do next. 
It seems we have here some PHP serialization, but no real way to exploit it.

Fortunately we looked at the recovered keystream:

`400ea7a58971b0f78fa9c6ed298764a8400ea7a58971b0f78fa9c6ed298764a8400ea7a58971b0f78fa9c6ed298764a8400ea7a58971b0f78fa9c6ed298764a8400ea7a58971b0f78fa9c6ed298764a8400ea7a58971b0f78fa9c6ed298764a8400ea7a5`

And we noticed that it repeats itself!
The unique part is just 32 bytes: `400ea7a58971b0f78fa9c6ed298764a8400ea7a58971b0f78fa9c6ed298764a8`

It means we can simply decrypt the whole payload by XORing the cookie with repeated key:

`a:5:{s:4:"flag";s:70:"DCTF{5740379144eb29f04ff6536733eba47e4bdfa0f0faade836b7bc0d70fa1ab006}";s:4:"name";s:8:"Player 1";s:5:"name2";s:8:"Player 2";s:5:"score";i:0;s:6:"score2";i:0;}`

The whole solver script [here](toe.py)
