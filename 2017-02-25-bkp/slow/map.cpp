#include <cstdio>
#include <complex>
#include <vector>
#include <unordered_map>
#include <unordered_set>

using namespace std;

typedef complex<double> cd;

unordered_map<size_t, cd> state, temp;

void reduce(){
	unordered_set<size_t> to_remove;
	for(auto p: state){
		if(abs(p.second)<1e-9){
			to_remove.insert(p.first);
		}
	}
	for(auto x: to_remove){
		state.erase(x);
	}
}

void add(size_t which){
	temp.clear();
	for(auto p: state){
		size_t i=p.first;
		cd si=p.second;
		size_t index=i|(1LL<<which);
		if(i&(1LL<<which)){
			temp[index]-=si/sqrt(2);
		}
		else{
			temp[index]+=si/sqrt(2);
		}
		temp[i&~(1LL<<which)]+=si/sqrt(2);
	}
	swap(state, temp);
	reduce();
	printf("Add %zu.\n", which);
}

void xst(size_t a, size_t b){
	temp.clear();
	for(auto p: state){
		size_t i=p.first;
		cd si=p.second;
		if(i&(1LL<<a)){
			size_t idx=i^(1LL<<b);
			temp[idx]=si;
		}
		else{
			temp[i]=si;
		}
	}
	swap(state, temp);
	reduce();
	printf("Xor %zu and %zu.\n", a, b);
}

void rot(size_t which){
	for(auto& p: state){
		size_t i=p.first;
		cd& si=p.second;
		if(i&(1LL<<which)){
			si*=complex<double>(0,1);
		}
	}
	printf("Rotate %zu.\n", which);
}

int ilog2(long long num){
	for(int i=0;; i++){
		if((1LL<<i)==num){ 
			return i;
		}
	}
}

void roti(long long num){
	rot(ilog2(num));
}

void xsti(long long a, long long b){
	xst(ilog2(a), ilog2(b));
}

long long finalize(){
	long long ret=0;
	for(size_t it=0; it<48; it++){
		ret*=2;
		double sum1=0;
		double sum2=0;
		for(auto p: state){
			size_t i=p.first;
			cd si=p.second;
			double a=abs(si);
			if(i&(1LL<<it)){
				sum1+=a*a;
			}
			else{
				sum2+=a*a;
			}
		}
		temp.clear();
		if(sum1>=0.25){
			ret++;
			for(auto p: state){
				size_t i=p.first;
				cd si=p.second;
				if(i&(1LL<<it)){
					temp[i]=si/sum1;
				}
			}
		}
		else{
			for(auto p: state){
				size_t i=p.first;
				cd si=p.second;
				if(!(i&(1LL<<it))){
					temp[i]=si/sum2;
				}
			}
		}
		swap(state, temp);
	}
	return ret;
}

int main(){
	state[0]=1;

	add(0);
	add(3);
	add(4);
	add(7);
	add(8);
	add(9);
	add(10);
	add(11);
	add(14);
	add(20);
	add(21);
	add(24);
	add(25);
	add(26);
	add(33);
	add(35);
	add(40);
	add(41);
	add(43);
	add(45);
	add(46);
	add(47);

	xsti(0x10000000000LL, 0x400000000LL);
	xst(45, 0);
	xst(32, 20);
	xst(44, 47);
	xst(45, 10);
	xst(45, 24);
	xst(5, 28);
	xst(41, 15);
	roti(0x1000000);
	xst(25, 12);
	roti(0x100000000LL);
	xst(43, 25);
	roti(0x20);
	xst(24, 9);
	xst(10, 37);
	xst(26, 37);
	roti(0x20);
	xst(35, 11);
	roti(0x10000000000LL);
	xst(12, 19);
	xst(24, 5);
	xst(24, 9);
	roti(0x40);
	xst(0, 43);
	xst(45, 33);
	xst(11, 42);
	xst(34, 35);
	xst(3, 44);
	xst(25, 21);
	xst(4, 18);
	roti(0x4000000000LL);
	xst(10, 43);
	xst(21, 39);
	xst(39, 20);
	roti(0x40000000);
	xst(24, 45);
	xst(46, 0);
	xst(47, 16);
	roti(0x100000000000LL);
	xst(35, 24);
	xst(19, 14);
	xst(38, 17);
	xst(13, 38);
	xst(5, 24);
	xst(19, 10);
	xst(6, 41);
	xst(3, 26);
	xst(43, 37);
	xst(45, 46);
	xst(40, 6);
	roti(0x40000000);
	xst(10, 27);
	xst(37, 1);
	xst(18, 42);
	roti(2);
	xst(37, 25);
	xst(20, 32);
	xst(37, 3);
	xst(34, 40);
	roti(0x100000000000LL);
	xst(13, 35);
	xst(7, 6);
	xst(28, 16);
	xst(40, 35);
	xst(35, 5);
	roti(1);
	xst(14, 42);
	xst(46, 34);
	xst(7, 43);
	xst(38, 42);
	xst(32, 30);
	xst(27, 16);
	xst(1, 21);
	xst(35, 13);
	xst(33, 34);
	xst(10, 28);
	xst(23, 45);
	roti(0x800000000000LL);
	xst(8, 13);
	xst(21, 31);
	xst(16, 40);
	xst(37, 20);
	xst(3, 32);
	xst(28, 29);
	xst(15, 10);
	xst(19, 47);
	xst(6, 36);
	xst(4, 34);
	roti(0x100000000000LL);
	xst(23, 19);
	xst(19, 12);
	xst(40, 18);
	xst(38, 19);
	xst(16, 3);
	xst(22, 26);
	roti(0x100000000000LL);
	xst(11, 44);
	xst(6, 16);
	roti(0x4000000);
	xst(1, 0);
	xst(0, 10);
	roti(0x800000);
	roti(0x400000000000LL);
	roti(0x80000000000LL);
	xst(42, 9);
	xst(21, 6);
	xst(42, 31);
	xst(32, 6);
	xst(11, 22);
	xst(36, 44);
	xst(9, 8);
	xst(45, 1);
	xst(26, 27);
	xst(16, 13);
	xst(36, 33);
	xst(42, 26);
	xst(28, 18);
	xst(27, 21);
	roti(2);
	xst(16, 31);
	xst(1, 41);
	xst(19, 46);
	xst(34, 16);
	xst(11, 47);
	xst(9, 47);
	xst(42, 12);
	roti(4);
	xst(46, 13);
	roti(0x40000000);
	xst(3, 45);
	xst(3, 36);
	roti(0x4000000);
	roti(0x800);
	xst(25, 37);
	roti(0x8000000);
	xst(0, 3);
	xst(0, 36);
	xst(22, 27);
	xst(46, 0);
	roti(0x200);
	roti(0x80);
	xst(32, 46);
	xst(36, 17);
	roti(0x8000000000LL);
	roti(0x100000000LL);
	xst(20, 39);
	roti(0x20000000000LL);
	xst(34, 17);
	xst(2, 35);
	roti(0x10000000);
	roti(0x800);
	xst(23, 42);
	xst(29, 35);
	xst(34, 29);
	roti(0x40);
	xst(41, 33);
	roti(0x20000000000LL);
	xst(33, 22);
	roti(0x10000000);
	xst(15, 34);
	xst(34, 25);
	roti(0x800000);
	xst(20, 28);
	xst(39, 38);
	xst(10, 23);
	xst(35, 31);
	roti(0x10000);
	xst(41, 28);
	xst(32, 0);
	roti(0x40000000);
	xst(47, 30);
	roti(0x400000);
	xst(33, 12);
	xst(2, 22);
	xst(26, 24);
	xst(44, 21);
	xst(38, 43);
	roti(0x200000000000LL);
	xst(46, 30);
	roti(0x1000000);
	xst(26, 29);
	roti(0x200000000000LL);
	xst(19, 36);
	roti(0x100000000000LL);
	roti(0x400000000LL);
	xst(14, 42);
	roti(0x200000);
	xst(41, 0);
	xst(16, 31);
	xst(27, 22);
	xst(30, 26);
	xst(11, 4);
	xst(13, 31);
	xst(16, 10);
	xst(3, 11);
	xst(20, 33);
	roti(0x400000000LL);
	xst(23, 14);
	xst(30, 21);
	xst(41, 29);
	xst(43, 37);
	xst(7, 24);
	xst(13, 12);
	roti(4);
	xst(19, 42);
	xst(34, 9);
	xst(34, 8);
	xst(40, 23);
	xst(23, 36);
	xst(6, 45);
	xst(19, 26);
	xst(13, 28);
	xst(35, 36);
	roti(0x20000000);
	roti(2);
	roti(0x8000);
	xst(19, 2);
	xst(10, 36);
	xst(3, 15);
	roti(0x2000000);
	roti(0x100000000000LL);
	xst(0, 20);
	xst(32, 20);
	xst(10, 41);
	xst(6, 11);
	xst(43, 26);
	xst(23, 5);
	roti(0x10000);
	xst(28, 17);
	xst(4, 15);
	xst(37, 43);
	xst(37, 22);
	xst(46, 21);
	roti(0x40000);
	roti(1);
	xst(47, 33);
	xst(24, 15);
	xst(27, 35);
	xst(2, 1);
	roti(0x100000000000LL);
	xst(39, 0);
	xst(36, 13);
	xst(0, 1);
	roti(0x10000);
	xst(18, 25);
	xst(11, 47);
	xst(10, 25);
	xst(13, 21);
	xst(8, 33);
	xst(30, 21);
	xst(22, 29);
	xst(35, 24);
	xst(18, 38);
	xsti(0x40, 0x2000000);
	xst(40, 37);
	xst(10, 32);
	roti(0x80000000);
	roti(0x200);
	xst(20, 23);
	roti(2);
	xst(4, 33);
	xst(14, 31);
	xst(3, 22);
	roti(0x10);
	xst(17, 21);
	xst(4, 13);
	xst(36, 14);
	xst(45, 8);
	xst(47, 43);
	xst(14, 40);
	xst(4, 46);
	xst(47, 13);
	xst(5, 47);
	xst(39, 20);
	xst(45, 39);
	xst(31, 7);
	roti(0x4000000000LL);
	xst(16, 40);
	xst(3, 43);
	xst(20, 43);
	roti(0x40);
	xst(24, 2);
	xst(3, 35);
	xst(21, 46);
	roti(0x8000000);
	xst(20, 24);
	roti(0x8000000);
	roti(0x100000);
	roti(0x2000000);
	xst(24, 22);
	xst(15, 34);
	xst(26, 11);
	roti(0x100000000LL);
	roti(0x800000000LL);
	xst(31, 30);
	xst(2, 14);
	xst(39, 34);
	xst(35, 43);
	xst(4, 18);
	roti(0x4000000000LL);
	xst(15, 20);
	xst(36, 17);
	xst(16, 5);
	roti(0x20);
	xst(46, 45);
	xst(5, 6);
	xst(41, 17);
	xst(20, 19);
	xst(16, 12);
	xst(30, 9);
	roti(0x2000000000LL);
	roti(0x200);
	xst(45, 4);
	xst(22, 37);
	roti(0x80000000);
	roti(0x200000);
	xst(33, 30);
	xst(12, 23);
	xst(23, 32);
	xst(32, 37);
	roti(0x80000);
	xst(39, 28);
	xst(3, 23);
	xst(41, 43);
	xst(15, 33);
	xst(26, 1);
	roti(0x40000);
	xst(19, 26);
	roti(0x800000000LL);
	xst(36, 7);
	xst(31, 18);
	xst(17, 23);
	xst(26, 34);
	roti(0x400);
	roti(0x200000000000LL);
	xst(18, 39);
	xst(35, 12);
	xst(28, 1);
	xst(10, 20);
	roti(0x1000000);
	xst(8, 44);
	xst(19, 5);
	xst(44, 13);
	xst(4, 19);
	roti(0x20);
	xst(10, 40);
	roti(0x80000000);
	roti(0x10000000000LL);
	xst(22, 34);
	xst(31, 16);
	xst(13, 19);
	roti(0x200000);
	xst(25, 19);
	xst(12, 10);
	roti(0x800000);
	xst(27, 37);
	xst(44, 21);
	xst(47, 23);
	roti(0x4000000);
	xst(9, 25);
	xst(27, 15);
	xst(9, 12);
	xst(41, 43);
	xst(21, 4);
	roti(0x40000000);
	xst(20, 5);
	xst(15, 41);
	roti(0x100000);
	roti(0x4000000000LL);
	roti(0x400000000000LL);
	xst(31, 32);
	xst(35, 34);
	xst(1, 38);
	xst(16, 20);
	xst(43, 23);
	xst(27, 25);
	xst(29, 17);
	xst(8, 9);
	roti(0x40000000);
	xst(13, 0);
	roti(0x400000);
	xst(16, 7);
	xst(43, 45);
	xst(6, 10);
	xst(43, 22);
	xst(1, 8);
	xst(18, 36);
	xst(30, 5);
	roti(0x40000000);
	xst(32, 26);
	roti(0x200000000000LL);
	roti(4);
	xst(34, 20);
	xst(28, 47);
	xst(46, 8);
	xst(22, 20);
	xst(16, 1);
	roti(4);
	xst(38, 47);
	xst(5, 6);
	roti(0x800000000000LL);
	xst(45, 22);
	roti(0x10000);
	roti(0x200000000LL);
	roti(0x8000000);
	xst(40, 8);
	xst(2, 36);
	xst(27, 16);
	xst(7, 2);
	xst(46, 0);
	xst(37, 6);
	xst(36, 4);
	xst(27, 17);
	xst(19, 37);
	roti(0x40000000000LL);
	xst(1, 31);
	xst(4, 43);
	roti(0x40000000000LL);
	roti(0x800000);
	xst(30, 43);

	long long result=finalize();
	printf("FLAG{%lld}\n", result);
}
