## URE (Crypto, 100p)

> Flag is : The valid input
> [Download](dMd)

###ENG
[PL](#pl-version)

We downloaded the program and started analysing it with help of disasembler. Skipping boring parts, most important part of program was looking like:

```c
int main() {
  // ...
  input = md5(input);
  // ...
  if (input[0] != 55
   || input[1] != 56
   || input[2] != 48
   || input[3] != 52
   || input[4] != 51
   || input[5] != 56
   || input[6] != 100
   || input[7] != 53
   || input[8] != 98
   || input[9] != 54
   || input[10] != 101
   || input[11] != 50
   || input[12] != 57
   || input[13] != 100
   || input[14] != 98
   || input[15] != 48
   || input[16] != 56
   || input[17] != 57
   || input[18] != 56
   || input[19] != 98
   || input[20] != 99
   || input[21] != 52
   || input[22] != 102
   || input[23] != 48
   || input[24] != 50
   || input[25] != 50
   || input[26] != 53
   || input[27] != 57
   || input[28] != 51
   || input[29] != 53
   || input[30] != 99
   || input[31] != 48 ) {
        // FAIL
    } else {
        // OK
    }
}
```

We just concatenated all hash characters and got to:

    780438d5b6e29db0898bc4f0225935c0
 
This is equal to md5("b781cbb29054db12f88f08c6e161c199"), so that's what the flag is.

Interesting fact, that text is also equal to md5(md5("grape")), so that's probably how task authors generated that hash.

###PL version

Pobieramy program i analizujemy go za pomocą disasemblera. Żeby nie przedłużać, widać najważniejsze miejsce programu od razu:

```c
int main() {
  // ...
  input = md5(input);
  // ...
  if (input[0] != 55
   || input[1] != 56
   || input[2] != 48
   || input[3] != 52
   || input[4] != 51
   || input[5] != 56
   || input[6] != 100
   || input[7] != 53
   || input[8] != 98
   || input[9] != 54
   || input[10] != 101
   || input[11] != 50
   || input[12] != 57
   || input[13] != 100
   || input[14] != 98
   || input[15] != 48
   || input[16] != 56
   || input[17] != 57
   || input[18] != 56
   || input[19] != 98
   || input[20] != 99
   || input[21] != 52
   || input[22] != 102
   || input[23] != 48
   || input[24] != 50
   || input[25] != 50
   || input[26] != 53
   || input[27] != 57
   || input[28] != 51
   || input[29] != 53
   || input[30] != 99
   || input[31] != 48 ) {
        // FAIL
    } else {
        // OK
    }
}
```

Po zebraniu wszystkich znaków, otrzymujemy

    780438d5b6e29db0898bc4f0225935c0
 
Jest to md5("b781cbb29054db12f88f08c6e161c199"), i to wprowadzamy jako flagę.

Co ciekawe, jest to też md5(md5("grape")), ale nie ma to wpływu na rozwiązanie zadania.
