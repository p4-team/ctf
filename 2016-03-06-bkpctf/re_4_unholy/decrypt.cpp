#include <cstdint>
#include <cstdio>
// http://tpforums.org/forum/threads/2158-XTEA-Encryption-Decryption-Code/page4
void process_decrypt(uint32_t *v, uint32_t *k){
	uint32_t v0 = v[0],	v1 = v[1], i, 
		delta = 0x61C88647,
		sum = 0xC6EF3720;
	for(i = 0; i < 32; i++){   
		v1 -= ((v0 << 4 ^ v0 >> 5) + v0) ^ (sum + k[sum >> 11 & 3]);
		sum += delta;
		v0 -= ((v1 << 4 ^ v1 >> 5) + v1) ^ (sum + k[sum & 3]);
	}
	v[0] = v0;
	v[1] = v1;
}

void print(uint32_t x){
	printf("%c%c%c%c", x&0xFF, (x&0xFF00)>>8,
			(x&0xFF0000)>>16, (x&0xFF000000)>>24);
}

int main(){
	uint32_t key[]={0x74616877U, 0x696F6773U, 0x6E6F676E, 0x65726568};
	for(int i=0;i<4;i++){
		print(key[i]);
	}
	printf("\n");
	uint32_t matrix[]={
		2990080719,
		722035088,
		1368334760,
		1473172750,
		412774077,
		3386066071,
		3804000291,
		563111828,
		3342378109,
		0x4De3F9FD
	};
	for(int i=0;i<5;i++){
		process_decrypt(matrix+2*i, key);
	}
	for(int i=0;i<10;i++){
		print(matrix[i]);
	}
}
