## SecCoding 2 (Misc, 300p)

> You should fix vulnerabilities of the given source code, WITHOUT changing its normal behaviour. Link 

###ENG
[PL](#pl-version)

We are given following code, and are tasked with repairing bugs and vulnerabilities in it:

```cpp
#include <math.h>
#include <stdio.h>
#include <windows.h>


int main(int argc, char **argv)
{
	// STRING ECHO
	//
	// Sample usage:
	//   strecho repeat=4,str=pleaseechome

	char *str = (char *)malloc(100);
	int repeat = 0;

	char *line = GetCommandLineA();

	while (*line != ' ')
		line++;
	line++;

	if (strncmp(line, "repeat=", 7) == 0)
	{
		line += 7;
		repeat = atoi(line);
		line += (int)ceil(log10((double)repeat)) + 1;
	}

	if (strncmp(line, "str=", 4) == 0)
	{
		line += 4;
		str = strtok(line, " ");
	}

	for (int i = 0; i < repeat; i++)
		printf("%s\n", str);

	line += strlen(str);
	for (; line >= GetCommandLineA(); line--)
		*line = '\x0';

	free(str);

	return -14;
}
```

This code doesn't suck as much as previous one, but still is way worse that anything that could hope to pass any code review.
Regardless, we tweaked this code, added few checks here and there, and managed to solve this challenge:

```cpp
#include <errno.h>
#include <math.h>
#include <stdio.h>
#include <windows.h>


int main(int argc, char **argv) {
	// STRING ECHO
	//   strecho repeat=4,str=pleaseechome

	char *line = GetCommandLineA();
    int repeat = 0;

	while (*line != ' ') {
		line++;
        if (*line == '\0') { puts("error"); return -14; }
    }
	line++;
    if (*line == '\0') { puts("error"); return -14; }

	if (strncmp(line, "repeat=", 7) == 0) {
		line += 7;
		repeat = strtol(line, &line, 10);
        if (repeat <= 0) { puts("error"); return -14; }
        if (errno == ERANGE) { puts("error"); return -14; }
	}
    line++;
    if (*line == '\0') { puts("error"); return -14; }

	if (strncmp(line, "str=", 4) == 0) {
		line += 4;
        for (int i = 0; i < repeat; i++) {
            printf("%s\n", line);
        }
	}
	return -14;
}
```

###PL version

Dostajemy następujący kod, i mamy naprawić w nim błędy i vulny:

```cpp
#include <math.h>
#include <stdio.h>
#include <windows.h>


int main(int argc, char **argv)
{
	// STRING ECHO
	//
	// Sample usage:
	//   strecho repeat=4,str=pleaseechome

	char *str = (char *)malloc(100);
	int repeat = 0;

	char *line = GetCommandLineA();

	while (*line != ' ')
		line++;
	line++;

	if (strncmp(line, "repeat=", 7) == 0)
	{
		line += 7;
		repeat = atoi(line);
		line += (int)ceil(log10((double)repeat)) + 1;
	}

	if (strncmp(line, "str=", 4) == 0)
	{
		line += 4;
		str = strtok(line, " ");
	}

	for (int i = 0; i < repeat; i++)
		printf("%s\n", str);

	line += strlen(str);
	for (; line >= GetCommandLineA(); line--)
		*line = '\x0';

	free(str);

	return -14;
}
```

Ten kod nie jest tak dramatycznie zły jak poprzedni, ale ciągle nie miałby szans na przejście code-review gdziekolwiek.
Tak czy inaczej, poprawiliśmy go troche, dodaliśmy trochę sprawdzeń tu i tam, i udało nam się dostać 300p za to zadanie:

```cpp
#include <errno.h>
#include <math.h>
#include <stdio.h>
#include <windows.h>


int main(int argc, char **argv) {
	// STRING ECHO
	//   strecho repeat=4,str=pleaseechome

	char *line = GetCommandLineA();
    int repeat = 0;

	while (*line != ' ') {
		line++;
        if (*line == '\0') { puts("error"); return -14; }
    }
	line++;
    if (*line == '\0') { puts("error"); return -14; }

	if (strncmp(line, "repeat=", 7) == 0) {
		line += 7;
		repeat = strtol(line, &line, 10);
        if (repeat <= 0) { puts("error"); return -14; }
        if (errno == ERANGE) { puts("error"); return -14; }
	}
    line++;
    if (*line == '\0') { puts("error"); return -14; }

	if (strncmp(line, "str=", 4) == 0) {
		line += 4;
        for (int i = 0; i < repeat; i++) {
            printf("%s\n", line);
        }
	}
	return -14;
}
