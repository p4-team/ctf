#include <cstdio>
#include <cstdlib>
#include <cstdint>

#define	_rotr(x, n)   ((((x)>>(n)) | ((x) << (32 - (n)))))
#define _rotl(x, n)   (((x)<<(n))|((x)>>(32-(n))))

uint32_t hash(uint32_t num){
	num^=0x24f50094U;
	num=_rotr(num, num&0xF);
	num+=0x2219ab34U;
	num=_rotl(num, num&0xF);
	num*=0x69a2c4feU;
	return num;
}

void find_collisions(uint32_t hash_to){
	uint32_t block=0;
	do{
		uint32_t h=hash(block);
		if(h==hash_to){
			printf("%08X %c%c%c%c\n", block, block, block>>8, block>>16, block>>24);
		}
	}while(++block);
}

unsigned char hashes[]="\x95\x13\xaa\xa5\x52\xe3\x2e\x2c\xad\x62\x33\xc4\xf1\x3a\x72\x8a\x5c\x5b\x8f\xc8\x79\xfe\xbf\xa9\xcb\x39\xd7\x1c\xf4\x88\x15\xe1\x0e\xf7\x76\x64\x05\x03\x88\xa3";

int main(){
	uint32_t hh=0xf113cca1;
	printf("Debug: %x %x %x %x\n", hh, hash(hh), hash(hh)^0x9513aaa5, _rotr(hash(hh)^0x9513aaa5,7));

	uint32_t temp=0;
	for(int i=0;i<10;i++){
		uint32_t newtemp=hashes[i*4]<<24;
		newtemp|=hashes[i*4+1]<<16;
		newtemp|=hashes[i*4+2]<<8;
		newtemp|=hashes[i*4+3]<<0;
		printf("newtemp is %x\n", newtemp);
		// newtemp=_rotr(temp^hash(block), 7)
		// thus:
		// _rotl(newtemp,7)=temp^hash(block)
		// hash(block)=_rotl(newtemp)^temp;
		printf("Rotled: %x\n", _rotl(newtemp, 7));
		printf("temp: %x\n", temp);
		printf("xored: %x\n", _rotl(newtemp, 7)^temp);
		uint32_t h=_rotl(newtemp, 7)^temp;
		printf("Finding hash for %x\n", h);
		find_collisions(h);

		temp=newtemp;
	}
}
