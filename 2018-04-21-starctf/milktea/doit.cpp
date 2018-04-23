#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <cstring>

char bufkey_str[1000] = "I'm a big fan of septyem46c7eb3f858c137f9bdffa5e0f880e8959bb2e65";

int* bufkey = (int*) bufkey_str;

unsigned int all_v5[] = {
	0x363DDF8A,
	0x0E3707311,
	0x0E879FDD,
	0x24BEA3C7,
	0x9B7E408B,
	0x3074528A,
	0x0C6445404,
	0x0A35E8A61,
	0x99B3FD42,
	0x4DF979E2,
	0x1F8C4B0E,
	0x1447FFFA,
	0x8B99BBFD,
	0x0AF5F33D7,
	0x2F51FB8C,
	0x0ADC702EB,
	0x0B5A5319C,
	0x33984815,
	0x41535A36,
	0x0E657EB0B,
	0x0A4B199FF,
	0x0D1C6CD38,
	0x0BF583A5E,
	0x930ABA46,
	0x0D72C79D9,
	0x6BFEFE79,
	0x0C078D7C2,
	0x4E7543D1,
	0x4CD7A6F5,
	0x86E471D0,
	0x0A3AF0F50,
	0x5347B2A8,
	0x32C531A5,
	0x6917DC30,
	0x47BB052F,
	0x0CBF37B13,
	0x0D78FCCAA,
	0x0B69B15D6,
	0x13CE1C8E,
	0x38FEA0C8,
	0x4B0F668A,
	0x680AFFA0,
	0x6F6DCF36,
	0x4D5B77E0,
	0x0AE297FA2,
	0x0F059DF29,
	0x4C598EFB,
	0x0E006177F,
	0x60F2E72D,
	0x9060FA96,
	0x7B264647,
	0x69982847,
	0x0B2722356,
	0x586C7009,
	0x0A2208796,
	0x1DB31180,
	0x0F6CBF07E,
	0x8FE301BC,
};

uint64_t round(uint64_t in, int n) {
	uint32_t v4 = in;
	uint32_t v6 = in >> 32;

	uint32_t v5a = all_v5[n * 2];
	uint32_t v5b = all_v5[n * 2 + 1];
	v6 += ((v5a + bufkey[v4 & 0xf]) ^ (v4 + ((v4 >> 5) ^ (16 * v4))));
	v4 += ((v5b + bufkey[v6 & 0xF]) ^ (v6 + ((v6 >> 5) ^ (16 * v6))));
	
	uint64_t fin = ((uint64_t) v6 << 32) | v4;
	return fin;
}

uint64_t invround(uint64_t out, int n) {
	uint32_t v4 = out;
	uint32_t v6 = out >> 32;

	uint32_t v5a = all_v5[n * 2];
	uint32_t v5b = all_v5[n * 2 + 1];
	v4 -= ((v5b + bufkey[v6 & 0xF]) ^ (v6 + ((v6 >> 5) ^ (16 * v6))));
	v6 -= ((v5a + bufkey[v4 & 0xf]) ^ (v4 + ((v4 >> 5) ^ (16 * v4))));

	uint64_t fin = ((uint64_t) v6 << 32) | v4;
	return fin;
}

uint64_t dec(uint64_t state) {
	state = (state << 32) | (state >> 32);
	for (int j = 28; j >= 0; j--) {
		state = invround(state, j);
	}
	return state;
}

char buf[1000];

uint64_t xor1[] = {
	0x4FFCD296B19AFA37,
	0x0C912086E763430B7,
	0x9B2B79EE86ABC820,
	0x0A05322E3934CC3EA,
	0x0A05322E3934CC3EA,
	0x0A05322E3934CC3EA,
	0x4AA443CAD9CBE242,
};

uint64_t xor2[] = {
	0x801135AA0BF7AC52LL,
	0x8C2842785341B12ELL,
	0xF0D4BB6A879413EELL,
	0x1498DC7D3336515CLL,
	0x310FE5B80BE8AD86LL,
	0x5603371B3DEEAFD4LL,
	0,
};

int main() {
	for (int i = 0; i < 7; i++) {
		uint64_t state = xor1[i] ^ xor2[i];
		state = dec(state);
		*(uint64_t*)buf = state;
		printf("%s", buf);
	}
	printf("\n");
}
