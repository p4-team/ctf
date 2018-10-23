#include "twofish.h"
#include <cstdio>
#include <cstdint>
#include <cstring>
#include "dump"

TwofishKey key;

uint32_t raw[] = {
0x0C01A4D6E,
0x0A4CB6636,
0x5B0F5BA1,
0x2B266926,
0x0EF75CB8F,
0x0A037222A,
0x0BA69619A,
0x60798932,
0x26EA859,
0x0F1315893,
0x8B5933A6,
0x0E72BAC67,
0x1ACC8904,
0x2E48D1EF,
0x3F21D5AB,
0x69335A1F,
0x0BE8368F0,
0x0F1F784C3,
0x18204990,
0x18CEA168,
0x33969157,
0x21EBF147,
0x0FA7AF872,
0x0ABE6BE6C,
0x514E617E,
0x0EC773FC2,
0x0C618C36A,
0x0F9CEF7A4,
0x75DCB301,
0x0AEE18C7A,
0x24F22669,
0x9ADB355F,
0x774EE123,
0x0C8F434A0,
0x0F47E97EF,
0x43797DF7,
0x0F6E46A45,
0x5B780D5,
0x0E3E1BF40,
0x54DD7532,
};

unsigned char expected[] = 
"\x4F\x6F\xA7\x87\xE9\x51\x87\x64\x38\x2A\x46\xE5\x4F\x21\x9E\x1C"
"\xCD\x65\xE1\x9A\x4F\xCF\xDE\x52\x09\xBF\x53\xC4\xB0\x95\x75\x31"
"\xAC\x2F\xF4\x97\x1D\xA5\x9A\x02\xA8\xFF\xAE\x2E\xB9\x70\xCC\x02";

unsigned char output[100];

void xr(unsigned char* a, unsigned char* b){
	for (int i = 0; i < 16; i++) {
		a[i] ^= b[i];
	}
}

int main() {
	memcpy(key.s, words, sizeof(words));
	memcpy(key.K, raw, sizeof(raw));
	Twofish two;
	two.Decrypt(&key, expected, output);
	printf("hitcon{%s", output);
	two.Decrypt(&key, expected+16, output+16);
	xr(output+16, expected);
	printf("%s", output+16);
	two.Decrypt(&key, expected+32, output+32);
	xr(output+32, expected+16);
	printf("%s}\n", output+32);
}
