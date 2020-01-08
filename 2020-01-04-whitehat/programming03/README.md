# Programming 03

Very fun challenge in which we test if a logical formula is a [tautology](https://en.wikipedia.org/wiki/Tautology_(logic)) or not.

The server gives us two expressions and we must say if they are logically equal. `AND` function is denoted as `*`, `OR` function as `+` and `NOT` as `~`.

First tasks are very easy and may be solved even by hand:

```
~(A*A)
((~A)+(A))
```

Later more variables appear and things are getting more complicated...

```
~(((~(~((~(A+~E)*~C)+(~C+H))*~((C+~E)+~(F*~H)))+(~((A+G)+~(H*(I+~C)))+~(E+G)))+((~(H*F)*((D*~I)*~A))+((~(D+E)*((G*G)*(A+~B)))+((~G+E)*I))))*((~(~(E*(~D*A))*(((~H*~C)+~(B+F))+(~H*(F+C))))+~((~(D*(~A*B))+(~(G*A)+~(C*A)))+(~((G+I)*F)+(~F*~D))))+((~((B*~(D+A))+((G+I)*(F+~F)))*~((E*A)+~(C+C)))*~((E*(C+D))+(((E*B)+~G)+(A+D))))))
((~A*~B*~C*~D*~E*~F*~G*~H*~I)+(~A*~B*~C*~D*~E*~F*~G*~H*I)+(~A*~B*~C*~D*~E*~F*~G*H*~I)+(~A*~B*~C*~D*~E*~F*~G*H*I)+(~A*~B*~C*~D*~E*~F*G*~H*~I)+(~A*~B*~C*~D*~E*~F*G*~H*I)+(~A*~B*~C*~D*~E*~F*G*H*~I)+(~A*~B*~C*~D*~E*~F*G*H*I)+(~A*~B*~C*~D*~E*F*~G*~H*~I)+(~A*~B*~C*~D*~E*F*~G*~H*I)+(~A*~B*~C*~D*~E*F*G*~H*~I)+(~A*~B*~C*~D*~E*F*G*~H*I)+(~A*~B*~C*~D*E*~F*~G*~H*~I)+(~A*~B*~C*~D*E*~F*~G*~H*I)+(~A*~B*~C*~D*E*~F*~G*H*~I)+(~A*~B*~C*~D*E*~F*~G*H*I)+(~A*~B*~C*~D*E*~F*G*~H*~I)+(~A*~B*~C*~D*E*~F*G*~H*I)+(~A*~B*~C*~D*E*~F*G*H*~I)+(~A*~B*~C*~D*E*~F*G*H*I)+(~A*~B*~C*~D*E*F*~G*~H*~I)+(~A*~B*~C*~D*E*F*~G*~H*I)+(~A*~B*~C*~D*E*F*G*~H*~I)+(~A*~B*~C*~D*E*F*G*~H*I)+(~A*~B*~C*D*~E*~F*~G*~H*~I)+(~A*~B*~C*D*~E*~F*~G*~H*I)+(~A*~B*~C*D*~E*~F*~G*H*~I)+(~A*~B*~C*D*~E*~F*~G*H*I)+(~A*~B*~C*D*~E*~F*G*~H*~I)+(~A*~B*~C*D*~E*~F*G*~H*I)+(~A*~B*~C*D*~E*~F*G*H*~I)+(~A*~B*~C*D*~E*~F*G*H*I)+(~A*~B*~C*D*~E*F*~G*~H*~I)+(~A*~B*~C*D*~E*F*~G*~H*I)+(~A*~B*~C*D*~E*F*G*~H*~I)+(~A*~B*~C*D*~E*F*G*~H*I)+(~A*~B*~C*D*E*~F*~G*~H*~I)+(~A*~B*~C*D*E*~F*~G*~H*I)+(~A*~B*~C*D*E*~F*~G*H*~I)+(~A*~B*~C*D*E*~F*~G*H*I)+(~A*~B*~C*D*E*~F*G*~H*~I)+(~A*~B*~C*D*E*~F*G*~H*I)+(~A*~B*~C*D*E*~F*G*H*~I)+(~A*~B*~C*D*E*~F*G*H*I)+(~A*~B*~C*D*E*F*~G*~H*~I)+(~A*~B*~C*D*E*F*~G*~H*I)+(~A*~B*~C*D*E*F*G*~H*~I)+(~A*~B*~C*D*E*F*G*~H*I)+(~A*~B*C*~D*~E*~F*~G*~H*~I)+(~A*~B*C*~D*~E*~F*~G*~H*I)+(~A*~B*C*~D*~E*~F*~G*H*~I)+(~A*~B*C*~D*~E*~F*~G*H*I)+(~A*~B*C*~D*~E*~F*G*~H*~I)+(~A*~B*C*~D*~E*~F*G*~H*I)+(~A*~B*C*~D*~E*~F*G*H*~I)+(~A*~B*C*~D*~E*~F*G*H*I)+(~A*~B*C*~D*~E*F*~G*~H*~I)+(~A*~B*C*~D*~E*F*~G*~H*I)+(~A*~B*C*~D*~E*F*G*~H*~I)+(~A*~B*C*~D*~E*F*G*~H*I)+(~A*~B*C*~D*E*~F*~G*~H*~I)+(~A*~B*C*~D*E*~F*~G*~H*I)+(~A*~B*C*~D*E*~F*~G*H*~I)+(~A*~B*C*~D*E*~F*~G*H*I)+(~A*~B*C*~D*E*~F*G*~H*~I)+(~A*~B*C*~D*E*~F*G*~H*I)+(~A*~B*C*~D*E*~F*G*H*~I)+(~A*~B*C*~D*E*~F*G*H*I)+(~A*~B*C*~D*E*F*~G*~H*~I)+(~A*~B*C*~D*E*F*~G*~H*I)+(~A*~B*C*~D*E*F*G*~H*~I)+(~A*~B*C*~D*E*F*G*~H*I)+(~A*~B*C*D*~E*~F*~G*~H*~I)+(~A*~B*C*D*~E*~F*~G*~H*I)+(~A*~B*C*D*~E*~F*~G*H*~I)+(~A*~B*C*D*~E*~F*~G*H*I)+(~A*~B*C*D*~E*~F*G*~H*~I)+(~A*~B*C*D*~E*~F*G*~H*I)+(~A*~B*C*D*~E*~F*G*H*~I)+(~A*~B*C*D*~E*~F*G*H*I)+(~A*~B*C*D*~E*F*~G*~H*~I)+(~A*~B*C*D*~E*F*~G*~H*I)+(~A*~B*C*D*~E*F*G*~H*~I)+(~A*~B*C*D*~E*F*G*~H*I)+(~A*~B*C*D*E*~F*~G*~H*~I)+(~A*~B*C*D*E*~F*~G*~H*I)+(~A*~B*C*D*E*~F*~G*H*~I)+(~A*~B*C*D*E*~F*~G*H*I)+(~A*~B*C*D*E*~F*G*~H*~I)+(~A*~B*C*D*E*~F*G*~H*I)+(~A*~B*C*D*E*~F*G*H*~I)+(~A*~B*C*D*E*~F*G*H*I)+(~A*~B*C*D*E*F*~G*~H*~I)+(~A*~B*C*D*E*F*~G*~H*I)+(~A*~B*C*D*E*F*G*~H*~I)+(~A*~B*C*D*E*F*G*~H*I)+(~A*B*~C*~D*~E*~F*~G*~H*~I)+(~A*B*~C*~D*~E*~F*~G*~H*I)+(~A*B*~C*~D*~E*~F*G*~H*~I)+(~A*B*~C*~D*~E*~F*G*~H*I)+(~A*B*~C*~D*~E*F*~G*~H*~I)+(~A*B*~C*~D*~E*F*~G*~H*I)+(~A*B*~C*~D*~E*F*G*~H*~I)+(~A*B*~C*~D*~E*F*G*~H*I)+(~A*B*~C*~D*E*~F*~G*~H*~I)+(~A*B*~C*~D*E*~F*~G*~H*I)+(~A*B*~C*~D*E*~F*G*~H*~I)+(~A*B*~C*~D*E*~F*G*~H*I)+(~A*B*~C*~D*E*F*~G*~H*~I)+(~A*B*~C*~D*E*F*~G*~H*I)+(~A*B*~C*~D*E*F*G*~H*~I)+(~A*B*~C*~D*E*F*G*~H*I)+(~A*B*~C*D*~E*~F*~G*~H*~I)+(~A*B*~C*D*~E*~F*~G*~H*I)+(~A*B*~C*D*~E*~F*G*~H*~I)+(~A*B*~C*D*~E*~F*G*~H*I)+(~A*B*~C*D*~E*F*~G*~H*~I)+(~A*B*~C*D*~E*F*~G*~H*I)+(~A*B*~C*D*~E*F*G*~H*~I)+(~A*B*~C*D*~E*F*G*~H*I)+(~A*B*~C*D*E*~F*~G*~H*~I)+(~A*B*~C*D*E*~F*~G*~H*I)+(~A*B*~C*D*E*~F*G*~H*~I)+(~A*B*~C*D*E*~F*G*~H*I)+(~A*B*~C*D*E*F*~G*~H*~I)+(~A*B*~C*D*E*F*~G*~H*I)+(~A*B*~C*D*E*F*G*~H*~I)+(~A*B*~C*D*E*F*G*~H*I)+(~A*B*C*~D*~E*~F*~G*~H*~I)+(~A*B*C*~D*~E*~F*~G*~H*I)+(~A*B*C*~D*~E*~F*G*~H*~I)+(~A*B*C*~D*~E*~F*G*~H*I)+(~A*B*C*~D*~E*F*~G*~H*~I)+(~A*B*C*~D*~E*F*~G*~H*I)+(~A*B*C*~D*~E*F*G*~H*~I)+(~A*B*C*~D*~E*F*G*~H*I)+(~A*B*C*~D*E*~F*~G*~H*~I)+(~A*B*C*~D*E*~F*~G*~H*I)+(~A*B*C*~D*E*~F*G*~H*~I)+(~A*B*C*~D*E*~F*G*~H*I)+(~A*B*C*~D*E*F*~G*~H*~I)+(~A*B*C*~D*E*F*~G*~H*I)+(~A*B*C*~D*E*F*G*~H*~I)+(~A*B*C*~D*E*F*G*~H*I)+(~A*B*C*D*~E*~F*~G*~H*~I)+(~A*B*C*D*~E*~F*~G*~H*I)+(~A*B*C*D*~E*~F*G*~H*~I)+(~A*B*C*D*~E*~F*G*~H*I)+(~A*B*C*D*~E*F*~G*~H*~I)+(~A*B*C*D*~E*F*~G*~H*I)+(~A*B*C*D*~E*F*G*~H*~I)+(~A*B*C*D*~E*F*G*~H*I)+(~A*B*C*D*E*~F*~G*~H*~I)+(~A*B*C*D*E*~F*~G*~H*I)+(~A*B*C*D*E*~F*G*~H*~I)+(~A*B*C*D*E*~F*G*~H*I)+(~A*B*C*D*E*F*~G*~H*~I)+(~A*B*C*D*E*F*~G*~H*I)+(~A*B*C*D*E*F*G*~H*~I)+(~A*B*C*D*E*F*G*~H*I)+(A*~B*~C*~D*~E*~F*~G*~H*~I)+(A*~B*~C*~D*~E*~F*~G*~H*I)+(A*~B*~C*~D*~E*~F*~G*H*~I)+(A*~B*~C*~D*~E*~F*~G*H*I)+(A*~B*~C*~D*~E*~F*G*~H*~I)+(A*~B*~C*~D*~E*~F*G*~H*I)+(A*~B*~C*~D*~E*~F*G*H*~I)+(A*~B*~C*~D*~E*~F*G*H*I)+(A*~B*~C*~D*~E*F*~G*~H*~I)+(A*~B*~C*~D*~E*F*~G*~H*I)+(A*~B*~C*~D*~E*F*G*~H*~I)+(A*~B*~C*~D*~E*F*G*~H*I)+(A*~B*~C*D*~E*~F*~G*~H*~I)+(A*~B*~C*D*~E*~F*~G*~H*I)+(A*~B*~C*D*~E*~F*~G*H*~I)+(A*~B*~C*D*~E*~F*~G*H*I)+(A*~B*~C*D*~E*~F*G*~H*~I)+(A*~B*~C*D*~E*~F*G*~H*I)+(A*~B*~C*D*~E*~F*G*H*~I)+(A*~B*~C*D*~E*~F*G*H*I)+(A*~B*~C*D*~E*F*~G*~H*~I)+(A*~B*~C*D*~E*F*~G*~H*I)+(A*~B*~C*D*~E*F*G*~H*~I)+(A*~B*~C*D*~E*F*G*~H*I)+(A*~B*~C*D*E*~F*~G*~H*~I)+(A*~B*~C*D*E*~F*~G*~H*I)+(A*~B*~C*D*E*~F*~G*H*~I)+(A*~B*~C*D*E*~F*~G*H*I)+(A*~B*~C*D*E*~F*G*~H*~I)+(A*~B*~C*D*E*~F*G*~H*I)+(A*~B*~C*D*E*~F*G*H*~I)+(A*~B*~C*D*E*~F*G*H*I)+(A*~B*~C*D*E*F*~G*~H*~I)+(A*~B*~C*D*E*F*~G*~H*I)+(A*~B*~C*D*E*F*G*~H*~I)+(A*~B*~C*D*E*F*G*~H*I)+(A*~B*C*~D*~E*~F*~G*~H*~I)+(A*~B*C*~D*~E*~F*~G*~H*I)+(A*~B*C*~D*~E*~F*~G*H*~I)+(A*~B*C*~D*~E*~F*~G*H*I)+(A*~B*C*~D*~E*~F*G*~H*~I)+(A*~B*C*~D*~E*~F*G*~H*I)+(A*~B*C*~D*~E*~F*G*H*~I)+(A*~B*C*~D*~E*~F*G*H*I)+(A*~B*C*~D*~E*F*~G*~H*~I)+(A*~B*C*~D*~E*F*~G*~H*I)+(A*~B*C*~D*~E*F*G*~H*~I)+(A*~B*C*~D*~E*F*G*~H*I)+(A*~B*C*D*~E*~F*~G*~H*~I)+(A*~B*C*D*~E*~F*~G*~H*I)+(A*~B*C*D*~E*~F*~G*H*~I)+(A*~B*C*D*~E*~F*~G*H*I)+(A*~B*C*D*~E*~F*G*~H*~I)+(A*~B*C*D*~E*~F*G*~H*I)+(A*~B*C*D*~E*~F*G*H*~I)+(A*~B*C*D*~E*~F*G*H*I)+(A*~B*C*D*~E*F*~G*~H*~I)+(A*~B*C*D*~E*F*~G*~H*I)+(A*~B*C*D*~E*F*G*~H*~I)+(A*~B*C*D*~E*F*G*~H*I)+(A*~B*C*D*~E*F*G*H*I)+(A*~B*C*D*E*~F*~G*~H*~I)+(A*~B*C*D*E*~F*~G*~H*I)+(A*~B*C*D*E*~F*~G*H*~I)+(A*~B*C*D*E*~F*~G*H*I)+(A*~B*C*D*E*~F*G*~H*~I)+(A*~B*C*D*E*~F*G*~H*I)+(A*~B*C*D*E*~F*G*H*~I)+(A*~B*C*D*E*~F*G*H*I)+(A*~B*C*D*E*F*~G*~H*~I)+(A*~B*C*D*E*F*~G*~H*I)+(A*~B*C*D*E*F*G*~H*~I)+(A*~B*C*D*E*F*G*~H*I)+(A*B*~C*~D*~E*~F*~G*~H*~I)+(A*B*~C*~D*~E*~F*~G*~H*I)+(A*B*~C*~D*~E*~F*G*~H*~I)+(A*B*~C*~D*~E*~F*G*~H*I)+(A*B*~C*~D*~E*F*~G*~H*~I)+(A*B*~C*~D*~E*F*~G*~H*I)+(A*B*~C*~D*~E*F*G*~H*~I)+(A*B*~C*~D*~E*F*G*~H*I)+(A*B*~C*D*~E*~F*~G*~H*~I)+(A*B*~C*D*~E*~F*~G*~H*I)+(A*B*~C*D*~E*~F*G*~H*~I)+(A*B*~C*D*~E*~F*G*~H*I)+(A*B*~C*D*~E*F*~G*~H*~I)+(A*B*~C*D*~E*F*~G*~H*I)+(A*B*~C*D*~E*F*G*~H*~I)+(A*B*~C*D*~E*F*G*~H*I)+(A*B*~C*D*E*~F*~G*~H*~I)+(A*B*~C*D*E*~F*~G*~H*I)+(A*B*~C*D*E*~F*G*~H*~I)+(A*B*~C*D*E*~F*G*~H*I)+(A*B*~C*D*E*F*~G*~H*~I)+(A*B*~C*D*E*F*~G*~H*I)+(A*B*~C*D*E*F*G*~H*~I)+(A*B*~C*D*E*F*G*~H*I)+(A*B*C*~D*~E*~F*~G*~H*~I)+(A*B*C*~D*~E*~F*~G*~H*I)+(A*B*C*~D*~E*~F*G*~H*~I)+(A*B*C*~D*~E*~F*G*~H*I)+(A*B*C*~D*~E*F*~G*~H*~I)+(A*B*C*~D*~E*F*~G*~H*I)+(A*B*C*~D*~E*F*G*~H*~I)+(A*B*C*~D*~E*F*G*~H*I)+(A*B*C*D*~E*~F*~G*~H*~I)+(A*B*C*D*~E*~F*~G*~H*I)+(A*B*C*D*~E*~F*G*~H*~I)+(A*B*C*D*~E*~F*G*~H*I)+(A*B*C*D*~E*F*~G*~H*~I)+(A*B*C*D*~E*F*~G*~H*I)+(A*B*C*D*~E*F*G*~H*~I)+(A*B*C*D*~E*F*G*~H*I)+(A*B*C*D*E*~F*~G*~H*~I)+(A*B*C*D*E*~F*~G*~H*I)+(A*B*C*D*E*~F*G*~H*~I)+(A*B*C*D*E*~F*G*~H*I)+(A*B*C*D*E*F*~G*~H*~I)+(A*B*C*D*E*F*~G*~H*I)+(A*B*C*D*E*F*G*~H*~I)+(A*B*C*D*E*F*G*~H*I))
```

The longest and hardest examples have nine variables from A to I. The idea behind the solver is quite simple. We test each possible value (`True` or `False`) for every variable which is present in given expressions and check if they are equal.

```{python}
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
```

One important security-related comment is needed here. Personally I do not like to use `eval` when an input is unknown. This is why I require manual confirmation before each evaluation:

```{python}
print str1
print str2
junk = raw_input('ok? ')
if solver(str1,str2):
	s.sendall("YES\n")
else:
	s.sendall("NO\n")
```

Fortunately this time nothing suspicious was found, except the flag. ;-)

```
WhiteHat{BO0l3_1s_s1MpL3_f0R_Pr0gR4mM3R}
```
