## SecCoding (Misc, 100p)

> You should fix vulnerabilities of the given source code, WITHOUT changing its normal behaviour. Link 

###ENG
[PL](#pl-version)

We are given following code, and are tasked with repairing bugs and vulnerabilities in it:

```cpp
#include <vector>
#include <iostream>
#include <windows.h>

using namespace std;


int main()
{
	vector<char> str(MAX_PATH);
	
	cout << "Enter your name: ";
	cin >> str.data();

	cout << "Hello " << str.data() << " :)" << endl;

	return -14;
}
```

This code is so bad, that if anyone seriously wrote code like that, he should immediately give up on programming and become baker instead.

We don't even try to repair this program, we just scrap it and write everything from zero:

```cpp
#include <iostream>
#include <string>

using namespace std;

int main() {
	string str;

	cout << "Enter your name: ";
	cin >> str;

	cout << "Hello " << str << " :)" << endl;

	return -14;
}
```

Challenge solved.

###PL version

Dostajemy taki kod i mamy go poprawić:

```cpp
#include <vector>
#include <iostream>
#include <windows.h>

using namespace std;


int main()
{
	vector<char> str(MAX_PATH);
	
	cout << "Enter your name: ";
	cin >> str.data();

	cout << "Hello " << str.data() << " :)" << endl;

	return -14;
}
```

Jest on tak dramatycznie napisany, że jeśli ktoś faktycznie napisał taki kod powinien prawdopodobnie zrezygnować z kariery programisty i przemyśleć karierę piekarza.

Darujemy sobie poprawki i po prostu piszemy go od zera:

```cpp
#include <iostream>
#include <string>

using namespace std;

int main() {
	string str;

	cout << "Enter your name: ";
	cin >> str;

	cout << "Hello " << str << " :)" << endl;

	return -14;
}
```

Zadanie rozwiązane.
