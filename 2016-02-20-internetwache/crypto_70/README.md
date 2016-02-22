## Hashdesigner (Crypto, 70p)

	There was this student hash design contest. All submissions were crap, but had promised 
	to use the winning algorithm for our important school safe. We hashed our password and 
	got '00006800007d'. Brute force isn't effective anymore and the hash algorithm had to 
	be collision-resistant, so we're good to go, aren't we?
	
###ENG
[PL](#pl-version)

In this task we got homemade hashing code. Although description says brute force is impossible,
it is easy to see that hash is effectively only two bytes long, which makes bruting it very easy.
Reusing given code, we quickly created a collision and submitted it manually to the service.

###PL version

W tym zadaniu dostejemy domowej roboty kod hashujący. Łatwo zauważyć, że ma on efektywnie tylko
dwa bajty długości, więc pomimo opisu zadania, zbrutowanie go jest proste. Korzystając z kodu,
który dostaliśmy, szybko znaleźliśmy kolizję i wysłaliśmy hasło.
