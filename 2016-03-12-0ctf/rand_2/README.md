## rand2 (Web, 2p)
	
###ENG
[PL](#pl-version)

Page uses rand() to generate random numbers.
One is printed at the start of the script.
Five next is stored and only md5 hash is returned.
Flag is displayed after we submit five unknown (for us numbers).

The seed has only 32 bit. Given enough CPU power we can exhaust a lot of this space.
It also helps to try several rand() outputs at once - we need just one correct solution.
To generate seeds producing given rand() output C program is used: 
```cpp
static unsigned int rnd(unsigned int seed) {
	srand(seed);
	return rand();
}

int main(int argc, char*argv[]) {
	int n[100];
	for(int i=0;i<argc-1;i++) {
		n[i]=atoi(argv[i+1]);
	}
	int skip = !!fork() + 2*(!!fork());
	for (uint32_t i=skip;i!=INT_MAX;i+=4) {
		int x = rnd(i);
		for(int j=0;j<argc-1;j++) {
			if(n[j] == x) {
				printf("%d %d\n", j, i);
				fflush(stdout);
			}
		}
	}
}
```
To check if given seed produces numbers matching md5, php script is used:
```php
<?php
srand((int)($argv[1]));
echo rand();
echo "\n";
$rand = array();
$i = 5;
$d = '';
$_d = '';
while($i--){
	$r = (string)rand();
	$rand = $r;
	$d .= $r;
	$_d .= 'check[]=';
	$_d .= $r;
	$_d .= "&";
}
echo md5($d);
echo "\n";
echo $_d;
echo "\n";
?>
```
All is stiched up with a python script:
```python
import requests
import subprocess

url = "http://202.120.7.202:8888/"
N = 8

session = [None] * N;
rands = [None] * N
hashes = [None] * N

for i in xrange(len(session)):
	session[i] = requests.session()
	p = session[i].get(url+"?go")
	md5 = p.text[len(p.text)-32:]
	r = p.text[:len(p.text)-32]
	rands[i] = r
	hashes[i] = md5
	print i, r, md5


proc = subprocess.Popen(["./a.out"]+rands, stdout=subprocess.PIPE)
for output in iter(proc.stdout.readline,''):
	print output
	i,s = output.split(" ")
	r_output = subprocess.Popen(["php", "rand.php", s], stdout=subprocess.PIPE).communicate()[0]
	g_rand,g_hash,g_d,_ = r_output.split("\n")
	print hashes[int(i)], g_hash
	if hashes[int(i)] == g_hash:
		print g_d
		print session[int(i)].get(url+"?"+g_d).text
		proc.kill()
		break
```
We try 8 sessions at once. After only a few tries valid seed is found and flag returned.


###PL version


Stronka używa funckcji rand() do generowania liczn.
Pierwsza jest wypisywana przy starcie skryptu.
Pięć następnych jest zapisywanych a zwracany jest tylko hasz md5.
Flaga zostanie nam ujawniona gdy podamy te pięć nieznanych nam liczb.

Ziarno dla funkcji rand() ma tylko 32 bity.
Przy dostatecznie dużej mocy obliczeniowej możemy przeszukać znaczącą część tej przestrzeni.
Możemy też próbować odgadnąć kilka ziaren na raz - potrzebne nam tylko jedno poprawne rozwiązanie a błędne nic na nie kosztują.
Aby wygenerować możliwe ziarna dla podanej wartośći rand() używamy poniższego programu w C:
```cpp
static unsigned int rnd(unsigned int seed) {
	srand(seed);
	return rand();
}

int main(int argc, char*argv[]) {
	int n[100];
	for(int i=0;i<argc-1;i++) {
		n[i]=atoi(argv[i+1]);
	}
	int skip = !!fork() + 2*(!!fork());
	for (uint32_t i=skip;i!=INT_MAX;i+=4) {
		int x = rnd(i);
		for(int j=0;j<argc-1;j++) {
			if(n[j] == x) {
				printf("%d %d\n", j, i);
				fflush(stdout);
			}
		}
	}
}
```
Każda podana liczba może być wygenerowana przez kilka różnych ziaren.
Aby odrzucić fałszywe, generujemy hasz 5 kolejnych liczb skryptem PHP.
Ziarno jest odrzucane jeżeli hasz różni się od wartośći orzymanej ze strony.
```php
<?php
srand((int)($argv[1]));
echo rand();
echo "\n";
$rand = array();
$i = 5;
$d = '';
$_d = '';
while($i--){
	$r = (string)rand();
	$rand = $r;
	$d .= $r;
	$_d .= 'check[]=';
	$_d .= $r;
	$_d .= "&";
}
echo md5($d);
echo "\n";
echo $_d;
echo "\n";
?>
```
Całość połączona jest skryptem w Pythonie:
```python
import requests
import subprocess

url = "http://202.120.7.202:8888/"
N = 8

session = [None] * N;
rands = [None] * N
hashes = [None] * N

for i in xrange(len(session)):
	session[i] = requests.session()
	p = session[i].get(url+"?go")
	md5 = p.text[len(p.text)-32:]
	r = p.text[:len(p.text)-32]
	rands[i] = r
	hashes[i] = md5
	print i, r, md5


proc = subprocess.Popen(["./a.out"]+rands, stdout=subprocess.PIPE)
for output in iter(proc.stdout.readline,''):
	print output
	i,s = output.split(" ")
	r_output = subprocess.Popen(["php", "rand.php", s], stdout=subprocess.PIPE).communicate()[0]
	g_rand,g_hash,g_d,_ = r_output.split("\n")
	print hashes[int(i)], g_hash
	if hashes[int(i)] == g_hash:
		print g_d
		print session[int(i)].get(url+"?"+g_d).text
		proc.kill()
		break
```
Próbująć odgadnąć 8 ziaren na raz, wystarczyło tylko kilka prób aby odgadnąć jedno odgadnąć mieszcząć się w czasie.

