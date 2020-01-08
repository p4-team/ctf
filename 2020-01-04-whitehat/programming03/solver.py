#!/usr/bin/python
# nc 52.78.36.66 82

def solver(str1,str2):
	finalstr = str1 + '==' + str2
	result = True
	tab = [[0,1] if x in finalstr else [0] for x in ['A','B','C','D','E','F','G','H','I']]
	for A in tab[0]:
		for B in tab[1]:
			for C in tab[2]:
				for D in tab[3]:
					for E in tab[4]:
						for F in tab[5]:
							for G in tab[6]:
								for H in tab[7]:
									for I in tab[8]:
										result &= eval(finalstr.replace('*','&').replace('+','|').replace('A', str(A)).replace('B',str(B)).replace('C',str(C)).replace('D',str(D)).replace('E', str(E)).replace('F', str(F)).replace('G',str(G)).replace('H',str(H)).replace('I',str(I)))
										if result is False:
											return result
	return result



import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('52.78.36.66',82))

while True:
	x = s.recv(999999)
	if 'flag' in x:
		break
	i1 = x.index('E1')
	i2 = x.index('E2')
	str1 = x[(i1+4):(i2-1)]
	str2 = x[(i2+4):(len(x)-3)]
	print str1
	print str2
	junk = raw_input('ok? ')
	if solver(str1,str2):
		s.sendall("YES\n")
	else:
		s.sendall("NO\n")

print x


# WhiteHat{BO0l3_1s_s1MpL3_f0R_Pr0gR4mM3R}
