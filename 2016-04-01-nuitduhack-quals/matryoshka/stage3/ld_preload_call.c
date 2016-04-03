#include <stdio.h>
#include <stdlib.h>

unsigned int tab[]= { 0x4007fd,0x40085c,0x4008c7,0x400926,0x40098a,
	0x4009e8,0x400a4c,0x400ab0,0x400b14,0x400b73,0x400bd7,0x400c36,
	0x400c95,0x400d0c,0x400d6b,0x400dcf,0x400e2e,0x400e8d,0x400eec,
	0x400f4b,0x400faa,0x40100e };
char* pass=(char*)0x6040c0;
void testx(int a){}

char password[50];
int i;
unsigned char cc;

typedef void (*sighandler_t)(int);
sighandler_t signal(int signum, sighandler_t handler){
	password[i]=cc;
	printf("%s\n", password);
	return testx;
}

__attribute__((constructor)) 
void init(){
	for(i=0;i<sizeof(tab)/sizeof(tab[0]);i++){
		sighandler_t f = (sighandler_t)tab[i];
		for(cc=0;cc<128;cc++){
			pass[i]=cc;
			f(11); // SIGINT
		}
	}
	exit(0);
}
