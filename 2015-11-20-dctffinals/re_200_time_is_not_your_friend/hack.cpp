#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool test(int a1) {
  int v3 = a1;
  int v4 = 0;
  while (v3) {
    v4 += v3 % 10;
    v3 /= 10;
  }
  return v4 == 41;
}

int getint() {
    return 49000000;
}

bool isprime(int number) { 
    if(number == 2) return true;
    if(number % 2 == 0) return false;
    for(int i=3; (i*i)<=number; i+=2){
        if(number % i == 0 ) return false;
    }
    return true;
}

int main() {
    int v2 = 49000000; 
    int v4 = 961748862;
    while(true) {
        if (isprime(v4)) {
            v2++;
            if(getint() <= v2 && test(v4)) {
                printf("DCTF{%d}\n", v4);
                break;
            }
        } v4++;
    }
}
