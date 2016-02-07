##Kick Tort Teen (Forensics, 50p)
	Anagram, anyone?
[Download](data.xls)

###ENG
[PL](#pl-version)


We start by converting the xls file to csv. Then we load up the values into a python script that counts the number occurences:

```python
occurences = []
for i in range(1000):
	occurences.append(0)

for y in data:
	for x in y:
		occurences[x]=occurences[x]+1

for i in range(len(occurences)):
	print(i, occurences[i])`
```

It turns out that there are 256 different numbers in the file, let's try swapping each number with its index in the list of all numbers that appear in the file. [decode.cpp](decode.cpp)

We get a ELF file that prints out the flag:

`SharifCTF{5bd74def27ce149fe1b63f2aa92331ab}`


###PL version

Pierwsze co zrobimy to przekonwertujemy spredsheeta do csv. Wartości wczytamy do prostego programu w pythonie zwracającego wystąpienia poszczególnych liczb: 

```python
occurences = []
for i in range(1000):
	occurences.append(0)

for y in data:
	for x in y:
		occurences[x]=occurences[x]+1

for i in range(len(occurences)):
	print(i, occurences[i])`
```

Okazuje się, że w pliku znajduje się 256 różnych liczb, spróbujmy zatem zastąpić każdą liczbę jej pozycją w liście wszystkich liczb które występują w tekście. [decode.cpp](decode.cpp)

Dostajemy plik ELF który po uruchomieniu wypisuje nam flagę: 

`SharifCTF{5bd74def27ce149fe1b63f2aa92331ab}`
