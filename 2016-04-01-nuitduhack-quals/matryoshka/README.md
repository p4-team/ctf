## Matryoshka (Crackme, 50+100+300+500)

This task was a crackme, which given correct password, spits out the next stage (base64-encoded).
Let's start with the first one.

## Stage 1

Running the binary normally, we get the usage information:
```
$ ./stage1.bin
Usage: ./stage1.bin <pass>
$ ./stage1.bin test
Try again...
```
Hmm, let's trace the binary to see which libraries it calls:
```
$ ltrace ./stage1.bin testPass
__libc_start_main(0x40064d, 2, 0x7ffc81da72a8, 0x4007a0 <unfinished ...>
strcmp("testPass", "Much_secure__So_safe__Wow")  = 39
fwrite("Try again...\n", 1, 13, 0x7fd915fba740Try again...
)  = 13
+++ exited (status 1) +++
```
We see it compares our input against constant. Running `./stage1.bin Much_secure__So_safe__Wow` gives us the next
stage.

## Stage 2

This time we are out of luck: tracing the binary doesn't help. We need to disassemble the binary.
Looking at the code, we see it consists of about 15 comparisons, such as:
```
0x004007b0      mov rax, qword [rbp - local_30h]
0x004007b4      add rax, 8
0x004007b8      mov rax, qword [rax] ; rax=pass
0x004007bb      movzx eax, byte [rax] ; rax=pass[0]
0x004007be      movsx eax, al
0x004007c1      lea edx, [rax + 0x10] ; edx=pass[0]+0x10
0x004007c4      mov rax, qword [rbp - local_30h]
0x004007c8      add rax, 8
0x004007cc      mov rax, qword [rax] ; rax=pass
0x004007cf      add rax, 6
0x004007d3      movzx eax, byte [rax] ; rax=pass[6]
0x004007d6      movsx eax, al
0x004007d9      sub eax, 0x10 ; rax-=0x10
0x004007dc      cmp edx, eax
0x004007de      je 0x4007e7  ;[2]
0x004007e0      mov dword [rbp - local_14h], 0
0x004007e7      mov rax, qword [rbp - local_30h]
```
This particular comparison can be stated as `pass[0]+0x10=pass[6]-0x10`. I stepped through the whole binary and
keeped track of all the equations:
```
b[0]='P'
2*b[3]=200 <=> b[3]=100 <=> b[3]='d'
b[0]+0x10=b[6]-0x10 <=> b[6]='p'
b[5]=0x5f <=> b[5]='_'
b[1]=b[7] 
b[1]=b[10]
b[1]-0x11=b[0] <=> b[1]='a', b[7]='a', b[10]='a'
b[3]=b[9] <=> b[9]='d'
b[4]='i'
b[2]-b[1]=0xd <=> b[2]='n'
b[8]-b[7]=0xd <=> b[8]='n'

b="Pandi_panda"
```
We can construct a full password using those equations: `Pandi_panda`. Again, passing this phrase to the executable
gives us another stage.

## Stage 3

This binary was much funnier. Instead of using normal calls and jumps, it relied on Unix signals for flow control.
The original code could look something like this:
```c
int main(int argc, char** argv){
	// Stuff, checking for length and so on skipped.
	int pid=getpid();
	signal(SIGINT, fn1);
	for(int i=0;i<1024;i++){
		kill(pid, SIGINT);
	}
}

void fn1(int sig){
	if(first_pass_character_is_ok){
		signal(SIGINT, fn2);
	}
}

void fn2(int sig){
	if(second_pass_character_is_ok){
		signal(SIGINT, fn3);
	}
}

// And so on. The last function printed congratulations and next stage.
```
Each function sets SIGINT's handler to the next one if it's password character was correct. These functions were
quite boring to reverse (but if needed, I could do this). Instead, I relied on `LD_PRELOAD`.

Since each character was checked on its own, isolated from the others, I could brute force each character
individually. It turned out to be quite problematic - as these functions were returning `void`, I couldn't know
if the character is good. I decided to replace `signal` function as well - this way, if it was called, I knew that
password was OK.

This is the code I wrote:
```c
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
```
It was basically iterating over hardcoded handler addresses and all printable characters, checking when
the handler calls `signal`, indicating success. Let's see if it works:
```
$ gcc -o brute.so -shared -fPIC ld_preload_call.c
$ LD_PRELOAD=./brute.so ./stage3.bin 
D
Di
Did
Did_
Did_y
Did_yo
Did_you
Did_you_
Did_you_l
Did_you_li
Did_you_lik
Did_you_like
Did_you_like_
Did_you_like_s
Did_you_like_si
Did_you_like_sig
Did_you_like_sign
Did_you_like_signa
Did_you_like_signal
Did_you_like_signals
Did_you_like_signals?
```
Running the binary with this string we see, that it is really the password.

## Stage 4





