## Oh Bob! (Crypto, 60p)

	Alice wants to send Bob a confidential message. They both remember the crypto lecture about
	RSA. So Bob uses openssl to create key pairs. Finally, Alice encrypts the message with 
	Bob's public keys and sends it to Bob. Clever Eve was able to intercept it. Can you help 
	Eve to decrypt the message?
	
###ENG
[PL](#pl-version)

In this task we got three public RSA keys and a `secret.enc` file containing three base64-encoded 
strings. After extracting modulus and exponent from the keys, we notice that modulus is 
somewhat short. After passing it to `yafu`, we found `p` and `q`, from which we could easily
decrypt the messages.

###PL version

W tym zadaniu dostaliśmy trzy klucze publiczne RSA, którymi zakodowano trzy wiadomości zawarte
w pliku `secret.enc`. Po wyciągnięciu `n` z klucza, zauważamy że jest on dość krótki. Program
`yafu` szybko sobie poradził z jego faktoryzacją, po czym odkodowaliśmy wiadomości.
