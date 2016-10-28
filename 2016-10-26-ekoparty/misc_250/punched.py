import Image
import sys
import os

IBM_MODEL_029_KEYPUNCH = [
"    /&-0123456789ABCDEFGHIJKLMNOPQR/STUVWXYZ:#@'=x`.<(+|!$*);^~,%_>? |",
"12 / O           OOOOOOOOO                        OOOOOO             |",
"11|   O                   OOOOOOOOO                     OOOOOO       |",
" 0|    O                           OOOOOOOOO                  OOOOOO |",
" 1|     O        O        O        O                                 |",
" 2|      O        O        O        O       O     O     O     O      |",
" 3|       O        O        O        O       O     O     O     O     |",
" 4|        O        O        O        O       O     O     O     O    |",
" 5|         O        O        O        O       O     O     O     O   |",
" 6|          O        O        O        O       O     O     O     O  |",
" 7|           O        O        O        O       O     O     O     O |",
" 8|            O        O        O        O OOOOOOOOOOOOOOOOOOOOOOOO |",
" 9|             O        O        O        O                         |",
"  |__________________________________________________________________|",
]

files = ["07d561df3da01f31590066f014652e995f7b76f1.png","4a95fea0f5e9af0af550b94fb960222e934ad09b.png","a034586b253b057c96da0b6707364853886b22b6.png","d3860afefe98f2408e24218a882aaf227d9287b9.png","19756efa72339faa9c9b5fe1743c3abedbc5079d.png","85a749d44bcba42869f21fb58f9725a443066a4f.png","a8a103961eccf8a991edfed1aaa39a8f9a3fe622.png","f7191b128c49ecfef0b27cd049550ae75249f86b.png","24c1e220c056210e6507c4c57079ffb99ffeb96c.png","89596be1f6463cb83abaecac7a375546069ecf0f.png","a9aba85ebcb160a7b18ea22abfb9589bd3ce1914.png","2d77fbd5eda9ed661a7834d8273815722fb97ccc.png","93ec404ba9266f5d059a727a6460b2693fc4c440.png","cdeea42d7f7216f93a9f1eb93b2723c70e693bea.png"]


def getRow(q):
	out = ""
	for i in range(len(IBM_MODEL_029_KEYPUNCH)):
		out += IBM_MODEL_029_KEYPUNCH[i][q]
	return out

def check(n, need):
	for i in range(len(need)):
		if(need[i] != getRow(n)[i+1]):
			return False
	return True



def find(need):
	for i in range(5, 69):
		if(check(i, need)):
			return i
	return -1

for f in files:

	im = Image.open("qr/"+f)
	pix = im.load()


	def isWhite(a):
		for q in a:
			if q != 255:
				return False
		return True


	for x in range(2, 82):
		column = ""
		for y in range(2, 25, 2):
			if(isWhite(pix[x*7 + 4, y*10 + 5])):
				column += ("O")
			else:
				column += (" ")
		sys.stdout.write(IBM_MODEL_029_KEYPUNCH[0][find(column)])
	print("")
