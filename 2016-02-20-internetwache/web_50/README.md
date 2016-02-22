## Mess of Hash (Web, 50p)

	Students have developed a new admin login technique. I doubt that it's secure, but the 
	hash isn't crackable. I don't know where the problem is...
	
###ENG
[PL](#pl-version)

In this task, we got a hash of password and are asked to log into the account. The hash was as
follows: 0e408306536730731920197920342119. We can notice it is pretty strange: only one 'e' letter,
and the rest of characters are digits. We can guess that the hash is incorrectly compared to
the stored one, and it gets interpreted as number 0. We could generate another password with
such property in a reasonable amount of time using attached script.

###PL version

W tym zadaniu dostaliśmy hash hasła: 0e408306536730731920197920342119. Wygląda on dość nietypowo,
gdyż ma tylko jedną literę 'e', a reszta znaków to cyfry. Jeśli zinterpretować go jako liczbę
z wykładnikiem, dostaniemy 0. Korzystając z załączonego skryptu, generujemy dowolne hasło z 
hashem o takiej własności w sensownym czasie.
