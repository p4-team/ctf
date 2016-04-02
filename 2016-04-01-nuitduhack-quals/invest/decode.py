import sys

data = "010001110101111001100011011011100100100100111001010111100100011101000111001110010100011100111001010001110011100101000111001110010101111001100011011011100100100101101110010010010011100100110101010111100110001100111001001101010110111001001001011011100100100101000111010111100011100100110101011011100100100101011110011000110100011101011110001110010011010101011110011000110101111001100011010111100110001101000111010111100101111001100011011011100100100101000111010111100011100100110101010001110101111001101110010010010101111001100011010111100110001101101110010010010101111001100011010111100110001100111001001101010100011101011110010111100110001101011110011000110101111001100011010001110101111001000111010111100101111001100011011011100100100101101110010010010101111001100011"

chunkLen = 8

def f_and(a, b):
	if(a == "1" and b == "1"):
		return "1"
	return "0"

def f_or(a, b):
	if(a == "1" or b == "1"):
		return "1"
	return "0"

def f_xor(a, b):
	if(a != b):
		return "1"
	return "0"

def f_not(a):
	if(a == "1"):
		return "0"
	if(a == "0"):
		return "1"
	else :
		print("Illegal char")
		print(a)
		print("/Illegal char")

for q in range(0, len(data), chunkLen):
	inputs = []
	for i in range(0, 8):
		inputs.append(data[q+i:q+i+1])


	first = ["0", "0", "0", "0", "0", "0"]
	first[0] = f_not(inputs[2])
	first[1] = f_not(inputs[3])
	first[2] = f_not(inputs[4])
	first[3] = f_not(inputs[1])
	first[4] = f_not(inputs[5])
	first[5] = f_not(inputs[7])


	second = ["0", "0", "0", "0", "0"]
	second[0] = f_and(inputs[0], first[0])
	second[1] = f_and(first[0], first[3])
	second[2] = f_and(inputs[0], inputs[1])
	second[3] = f_xor(inputs[6], inputs[5])
	second[4] = f_xor(first[3], first[5])

	third = ["0", "0", "0", "0", "0"]
	third[0] = f_and(second[0], first[1])
	third[1] = f_and(first[1], second[1])
	third[2] = f_and(second[2], first[1])
	third[3] = f_and(first[4], inputs[2])
	third[4] = f_and(inputs[2], second[4])


	fourth = ["0", "0", "0", "0"]
	fourth[0] = f_and(third[0], first[2])
	fourth[1] = f_and(first[2], third[1])
	fourth[2] = f_and(first[2], third[2])
	fourth[3] = f_and(third[3], second[3])


	fifth = ["0", "0"]
	fifth[0] = f_or(fourth[0], fourth[1])
	fifth[1] = f_or(fourth[2], fourth[3])


	sixth = [0]
	sixth[0] = f_or(fifth[1], third[4])

	seventh = f_or(fifth[0], sixth[0])

	sys.stdout.write(seventh)
print
