#include <cstdio>

#define PRE 1000000000

short pre[PRE];

typedef unsigned long long ull;

ull collatz(ull n){
	if(n%2 == 0){
		return n/2;
	}
	return n*3+1;
}

short collatzcnt(ull n){
	if(n>=PRE){
		return 1+collatzcnt(collatz(n));
	}
	if(pre[n]==-1){
		pre[n]=1+collatzcnt(collatz(n));
	}
	return pre[n];
}

ull fibmod(ull n, ull m){
	if(n<=1){
		return n%m;
	}
	ull a=0;
	ull b=1;
	for(ull i=0; i<n; i++){
		ull c=(a+b)%m;
		a=b;
		b=c;
	}
	return a;
}

int main(){
	ull n;
	scanf("%llu", &n);
	for(int i=0; i<PRE; i++){
		pre[i]=-1;
	}
	pre[0]=0;
	pre[1]=0;
	
	ull sum=0;
	for(ull i=1; i<=n; i++){
		if(i%100000000 == 0){ fprintf(stderr, "%llu/%llu\n", i/100000, n/100000); }
		sum+=collatzcnt(i);
	}
	printf("%llx\n", fibmod(n, sum));
}
