## Calculator (ppc/Programming, 200p)

### PL Version
`for ENG version scroll down`

Zadanie polegało na połączeniu się za pomocą NC z podanym serwerem. Serwer podawał na wejściu działania i oczekiwał na ich rozwiązania. Należało rozwiązać kilkadziesiąt przykładów pod rząd aby uzyskać flagę. Działania przychodzące z serwera miały postać:

`eight hundred ninety nine million, one hundred sixty eight thousand eleven - 556226 * ( 576 - 21101236 ) * 948 - ( 29565441 + thirty six ) * 182,745 - 6,124,792 + CMLXXVI - 647 =`

Na co serwer w odpowiedzi oczekiwał na: `11121023402232863`

Zadanie rozwiązaliśmy wykorzystując parser liczb słownych, parser liczb rzymskich oraz pythonową funkcję `eval()`.
Same transformacje są raczej trywialne i łatwie do znalezienia w internecie, reszta solvera to:

	def solve(data):
		fixed = data.replace(",", "") #turn 3,200 into 3200
		fixed = " " + fixed #ensure word boundary on the left
		romans = re.findall("[^\d=\\-\\+/\\*\\(\\)\s]+", fixed)
		for romanNumber in romans:
			try:
				number = str(fromRoman(romanNumber))
				fixed = re.sub(r"\b%s\b" % romanNumber, number, fixed)
			except:
				pass
		literals = re.findall("[^\d=\\-\\+/\\*\\(\\)]+", fixed)
		for literal in sorted(literals, key=lambda x: len(x), reverse=True):
			if literal != ' ' and literal != "":
				try:
					number = str(text2int(literal))
					fixed = re.sub(r"\b%s\b" % literal.strip(), number, fixed)
				except:
					pass
		return eval(fixed[:-2]) #omit " ="

Czyli w skrócie:

* Usuwamy przecinki będące separatorami tysiąców
* Zamieniamy wszystkie znalezione liczby rzymskie na arabskie
* Zamieniamy wszystkie znalezione literały na liczby arabskie (uwaga: trzeba zamieniać od tych najdłuższych, żeby np. zamiana "one" nie była plikowana do "fifty one")
* Usuwamy znak `=` z końca
* Ewaluujemy wyrażenie

Po kilkudziesieciu przykładach dostajemy: `Congratulations!The flag is TMCTF{U D1D 17!}`

### ENG Version

The challenge was to connect to a server via NC. Server was providing equations and was waiting for their solutions. We had to solve few dozens consecutively in order to get the flag. The equations were for example:

`eight hundred ninety nine million, one hundred sixty eight thousand eleven - 556226 * ( 576 - 21101236 ) * 948 - ( 29565441 + thirty six ) * 182,745 - 6,124,792 + CMLXXVI - 647 =`

And server was expecting a solution: `11121023402232863`

We solved this using literal nubmbers parser, roman numbers parser and python `eval()` function.
The parsers are trivial and easy to find on the internet, the rest was:

	def solve(data):
		fixed = data.replace(",", "") #turn 3,200 into 3200
		fixed = " " + fixed #ensure word boundary on the left
		romans = re.findall("[^\d=\\-\\+/\\*\\(\\)\s]+", fixed)
		for romanNumber in romans:
			try:
				number = str(fromRoman(romanNumber))
				fixed = re.sub(r"\b%s\b" % romanNumber, number, fixed)
			except:
				pass
		literals = re.findall("[^\d=\\-\\+/\\*\\(\\)]+", fixed)
		for literal in sorted(literals, key=lambda x: len(x), reverse=True):
			if literal != ' ' and literal != "":
				try:
					number = str(text2int(literal))
					fixed = re.sub(r"\b%s\b" % literal.strip(), number, fixed)
				except:
					pass
		return eval(fixed[:-2]) #omit " ="

So in short:

* We remove thousands separator `,`
* We turn all roman numbers into integers
* We turn all literal numbers into integers (notice: you need to replace starting from longest numbers so that for example replacing "one" doesn't affect "fifty one")
* We remove `=` from the end
* We evaluate the expression

After mutiple examples we finally get:`Congratulations!The flag is TMCTF{U D1D 17!}`
