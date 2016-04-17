## Rabit (Crypto, 175 points, 71 solves)

	Just give me a bit, the least significant's enough. Just a second we’re not broken, just very, very insecure. 
	Running at rabit.pwning.xxx:7763

###ENG
[PL](#pl-version)

We get the [server files](server) so we can analyse the cryptosystem.
It turns out that the flag is encrypted with Rabin cryptosystem so if encodes the data as `message^2 mod N`.
The server provides us with the `N` modulus value and with the encrypted flag `CT`.
We would like to get the value of `PT = sqrt_mod(CT, N)`
The server lets us to ask for the least-significant-bit (LSB) of selected decrypted ciphertexts of our choosing.
This means that the server acts a `least significant bit oracle` and we need to use this to our advantage.

If we send the encrypted flag as input the server will tell us the lowest bit for the plaintext flag, now we just need all the rest.
We can exploit this oracle using a binary-search algorithm.

It is quite obvious that if we multiply a number by 2 it will become an even number.
This means that the LSB will have to be 0 as it's always for even numbers.
Now if we perform a modular division by an odd number we can get two possible results:

- The number was smaller than the modulus and therefore it is still even and the LSB is 0
- The number was greater than the modulus and therefore it is now odd and the LSB is 1

The N modulus in our case is an odd number, since it's a product of two large primes.
This means that if we ask the oracle for the LSB of `2*PT mod N` we will get one of the two possible results:

- If LSB is 0 then the number was smaller than modulus and therefore `2*PT < N` which means `PT < N/2`
- If LSB is 1 then the number was greater than modulus and therefore `2*PT > N` which means `PT > N/2`

Now if we ask for LSB of `4*PT mod N` we can again get one of two possible results

- If LSB is 0 then either `4*PT < N` which means `PT < N/4` if `PT < N/2` or `PT < 3*N/4` if `PT > N/2`
- If LSB is 1 then either `4*PT > N` which means `PT > N/4` if `PT < N/2` or `PT > 3*N/4` if `PT > N/2`

This means that we can get lower and upper bounds for `PT` simply by asking for LSB for PT multiplied by powers of 2.
This is exactly binary search algorithm - we are looking for the `PT` value and the oracle tells us if it's bigger or smaller than given number.

The server first performs decryption of our input, which means it performs a modular square root on it.
So if we want the server to tell us LSB of `2*PT mod N` we need to provide `4*CT` as input since: 

`sqrt_mod(4*CT, N) = sqrt_mod(4,N)*sqrt_mod(CT,N) = 2*PT mod N` 

We automate it with a simple script:

```python
def oracle(ciphertext, s):
    print("sent ciphertext " + str(ciphertext))
    s.sendall(str(ciphertext) + "\n")
    data = recvline(s)
    print("oracle response: " + data)
    lsb = int(re.findall("lsb is (.*)", data)[0])
    return lsb


def brute_flag(encrypted_flag, N, socket):
    flag_lower_bound = 0
    flag_upper_bound = N
    mult = 0
    ciphertext = (encrypted_flag * pow(4, mult)) % N
    while flag_upper_bound > flag_lower_bound:
        data = s.recv(512)
        ciphertext = (ciphertext * 4) % N
        mult += 1
        print("main loop: " + data)
        print("upper = %d" % flag_upper_bound)
        print("upper flag = %s" % long_to_bytes(flag_upper_bound))
        print("lower = %d" % flag_lower_bound)
        print("lower flag = %s" % long_to_bytes(flag_lower_bound))
        print("multiplier = %d" % mult)
        if oracle(ciphertext, socket) == 0:
            flag_upper_bound = (flag_upper_bound + flag_lower_bound) / 2
        else:
            flag_lower_bound = (flag_upper_bound + flag_lower_bound) / 2
    return flag_upper_bound
```

The script updates the upper and lower bounds for the `PT` value depending on server responses.
This way we finally get:

```
main loop: Give a ciphertext: 
upper = 220166400929873038171224043083387335590015857856801737690673880396419795615547577312678070179481369128029264724566861040868992922377738134245284720456363270069895363821431128690061826490011022637831305626391095236981088399616123236780868219333517868946867381881069203811100413120301449973114417385114578488
upper flag = PCTF{LSB_is_4ll_y0u_ne3d}�MT�Ҵņ�|O�a�.Gȵ�j~R���Rڟ��NL�����o��Z�l����)�A�8{����Mm�Q1fܛ�H�[���"7���rɭEi�h9��f�.8
lower = 220166400929873038171224043083387335590015857856801737690673855617979183125104747088116187584366205351152315709323988324491729476435566167017734911926070078152771437195128495335458854458923475782666648931612841151096923643810580803048301608534266786867097762790952153653675570921913681095277174947521916134
lower flag = PCTF{LSB_is_4ll_y0u_ne3d}��P6�X�����ꕎ81���e�3�~��ę���4$Pz9��� ���0en"��̥�o�cȢ���.*z��?n�Ƨ>6�o���#���)G�jl�
multiplier = 212
sent ciphertext 50250755854349060273600748058347492460054410259628835643065315292422667886974689433086807089032905814811219345716171958732300878077805295946155889286309957357352555060432038801287412773647082525563214208397848831588353216532718958889969188087964218777646467718967423926109023022887010446083219487280951409895
oracle response: lsb is 0
```

At which point we can stop since we don't really need the rest 800 bits of padding and the flag is: `PCTF{LSB_is_4ll_y0u_ne3d}`

###PL version

Dostajemy [pliki serwera](server) więc możemy rozpocząc od analizy kryptosystemu.
Okazuje się, że flaga jest szyfrowana kryptosystemem Rabina, czyli szyfruje się poprzez `message^2 mod N`.
Serwer podaje nam wartość modulusa `N` oraz wartość zaszyfrowanej flagi `CT`.
Chcemy uzyskać wartość `PT = sqrt_mod(CT, N)`
Serwer pozwala nam pytać o wartość najniższego bitu plaintextu dla wybranych przez nas ciphertextów.
To oznacza że serwer działa jako `wyroczna najniższego bitu` a my mamy to wykorzystać.

Jeśli wyślemy zaszyfrowaną flagę jako dane do serwera, serwer powie nam jaki jest najniższy bit odszyfrownej flagi, a teraz potrzebujemy tylko pozostałe bity.
Możemy exploitować wyrocznie za pomocą algorytmu poszukiwania binarnego.

Jest dość oczywistym, że liczba pomnożona przez 2 będzie zawsze liczbą przystą.
To oznacza że LSB będzie zawsze 0.
Teraz jeśli wykonamy dzielenie modulo przez liczbe nieparzystą to możemy uzyskać dwa wyniki:

- Liczba jest mniejsza niż modulus więc jest nadal parzysta i LSB jest 0
- Liczba jest większa niż modulus więc jest teraz nieparzysta i LSB wynosi 1

Modulus N w naszym przypadku jest nieparzysty bo jest iloczynem dwóch dużych liczb pierwszych.
To oznacza że możemy spytać wyrocznie o LSB dla `2*PT mod N` i dostaniemy jedną z dwóch możliwości:

- Jeśli LSB jest 0 to znaczy że liczba była mniejsza niż modulus więc `2*PT < N` z czego wynika `PT < N/2`
- Jeśli LSB jest 1 to znaczy że liczba była większa niż modulus więc `2*PT > N` z czego wynika `PT > N/2`

Jeśli etraz zapytamy o LSB dla `4*PT mod N` znów możemy uzyskać dwie możliwości:

- Jeśli LSB jest 0 to albo `4*PT < N` z czego wynika `PT < N/4` jeśli `PT < N/2` lub `PT < 3*N/4` jeśli `PT > N/2`
- Jeśli LSB jest 1 to albo `4*PT > N` z czego wynika `PT > N/4` jeśli `PT < N/2` lub `PT > 3*N/4` jeśli `PT > N/2`

To oznacza że możemy wyliczyć górne oraz dolne ograniczenie na `PT` pytając wyrocznie o LSB dla PT pomnożonego przez kolejne potęgi 2.
To jest dokładnie wyszukiwanie binarne - szukamy liczby `PT` a wyrocznia mówi nam czy jest ona większa czy mniejsza od pewnej liczby.

Serwer wykonuje deszyfrowanie danych które wysyłamy, co oznacza że dokonuje na nich pierwiastkowania modularnego.
Więc jeśli chcemy aby serwer podał nam LSB `2*PT mod N` to musimy podać jako dane `4*CT` ponieważ:

`sqrt_mod(4*CT, N) = sqrt_mod(4,N)*sqrt_mod(CT,N) = 2*PT mod N` 

Automatyzujemy to prostym skryptem:

```python
def oracle(ciphertext, s):
    print("sent ciphertext " + str(ciphertext))
    s.sendall(str(ciphertext) + "\n")
    data = recvline(s)
    print("oracle response: " + data)
    lsb = int(re.findall("lsb is (.*)", data)[0])
    return lsb


def brute_flag(encrypted_flag, N, socket):
    flag_lower_bound = 0
    flag_upper_bound = N
    mult = 0
    ciphertext = (encrypted_flag * pow(4, mult)) % N
    while flag_upper_bound > flag_lower_bound:
        data = s.recv(512)
        ciphertext = (ciphertext * 4) % N
        mult += 1
        print("main loop: " + data)
        print("upper = %d" % flag_upper_bound)
        print("upper flag = %s" % long_to_bytes(flag_upper_bound))
        print("lower = %d" % flag_lower_bound)
        print("lower flag = %s" % long_to_bytes(flag_lower_bound))
        print("multiplier = %d" % mult)
        if oracle(ciphertext, socket) == 0:
            flag_upper_bound = (flag_upper_bound + flag_lower_bound) / 2
        else:
            flag_lower_bound = (flag_upper_bound + flag_lower_bound) / 2
    return flag_upper_bound
```

Skrypt aktualizuje górne oraz dolne ograniczenie dla `PT` w zależności od odpowiedzi serwera
W efekcie dostajemy wreszcie:

```
main loop: Give a ciphertext: 
upper = 220166400929873038171224043083387335590015857856801737690673880396419795615547577312678070179481369128029264724566861040868992922377738134245284720456363270069895363821431128690061826490011022637831305626391095236981088399616123236780868219333517868946867381881069203811100413120301449973114417385114578488
upper flag = PCTF{LSB_is_4ll_y0u_ne3d}�MT�Ҵņ�|O�a�.Gȵ�j~R���Rڟ��NL�����o��Z�l����)�A�8{����Mm�Q1fܛ�H�[���"7���rɭEi�h9��f�.8
lower = 220166400929873038171224043083387335590015857856801737690673855617979183125104747088116187584366205351152315709323988324491729476435566167017734911926070078152771437195128495335458854458923475782666648931612841151096923643810580803048301608534266786867097762790952153653675570921913681095277174947521916134
lower flag = PCTF{LSB_is_4ll_y0u_ne3d}��P6�X�����ꕎ81���e�3�~��ę���4$Pz9��� ���0en"��̥�o�cȢ���.*z��?n�Ƨ>6�o���#���)G�jl�
multiplier = 212
sent ciphertext 50250755854349060273600748058347492460054410259628835643065315292422667886974689433086807089032905814811219345716171958732300878077805295946155889286309957357352555060432038801287412773647082525563214208397848831588353216532718958889969188087964218777646467718967423926109023022887010446083219487280951409895
oracle response: lsb is 0
```

I możemy tutaj przerwać obliczenia ponieważ nie potrzebujmemy pozostałych 800 bitów paddingu a flaga to: `PCTF{LSB_is_4ll_y0u_ne3d}`
