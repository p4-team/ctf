#include <cstdio>
#include <cstdint>
#include <map>

using namespace std;

char s[] = " .::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::. ";
uint64_t poly = 0xC96C5795D7870F42;

uint64_t table[256];

void generate_table()
{
    for(int i=0; i<256; ++i)
    {
    	uint64_t crc = i;

    	for(unsigned int j=0; j<8; ++j)
    	{
            // is current coefficient set?
    		if(crc & 1)
            {
                // yes, then assume it gets zero'd (by implied x^64 coefficient of dividend)
                crc >>= 1;
    
                // and add rest of the divisor
    			crc ^= poly;
            }
    		else
    		{
    			// no? then move to next coefficient
    			crc >>= 1;
            }
    	}
    
        table[i] = crc;
    }
}

uint64_t calculate_crc(uint8_t* stream, unsigned int n, uint64_t crc)
{

    for(unsigned int i=0; i<n; ++i)
    {
        uint8_t index = stream[i] ^ crc;
        uint64_t lookup = table[index];

        crc >>= 8;
        crc ^= lookup;
    }

    return crc;
}

char buf1[100];
char buf2[100];
uint64_t crc;


map<int, map<int, char>> hints = {

};

char charset[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890";

#include <string.h>
int main() {
	generate_table();
	FILE* f = fopen("FLAGZ.DAT", "rb");
	for (int row=0; row<65; row++) {
		fread(buf2, 80, 1, f);
		fread(&crc, 8, 1, f);
		if (row < 53) continue;
		if (row == 53) {
			strcpy(buf1, ":                                                                              :");
			continue;
		}
		for (int i=0; i<80; i++) {
			buf1[i] ^= buf2[i];
		}
		for (auto& hint: hints[row]) {
			buf1[hint.first] = hint.second;
		}
		int found = 0;
		int cnt=0;
#define BRU1() for (int i=iprev; i<80 && !found; i++) for(int  j=32; j<128; j++) { int old=buf1[i]; buf1[i] = j; int iprev = i;
#define BRU() for (int i=iprev+1; i<=76 && !found; i++) for(char* p = charset; *p; p++) { int old=buf1[i]; buf1[i] = *p; int iprev = i;
#define BRE() buf1[i] = old; }
E0:
		int iprev = 0;
		BRU1()
			uint64_t c = calculate_crc((uint8_t*)buf1, 80, 0);
			if (c == crc) {
				found = true;
				cnt = 1;
				goto E1;
			}
		BRE()
		E1:

		if (!found) {
			printf("Help! (row %d)\n", row);
			printf("%s\n", buf1);
			for (int i=0; i<80; i++){
				printf("%d", i/10);
			}
			printf("\n");
			for (int i=0; i<80; i++){
				printf("%d", i%10);
			}
			printf("\n");
			int col;
			char bu[10];
			scanf("%d %s", &col, bu);
			if(bu[0] == 's' && bu[1] == 'p') bu[0] = ' ';
			if(bu[0] == 'e' && bu[1] == 'x') goto E6;
			buf1[col] = bu[0];
			goto E0;
		}
E6:
		iprev = 70;
		uint64_t c1 = calculate_crc((uint8_t*)buf1, 70, 0);
		BRU()
			printf("%c\n", *p);
		BRU()
			uint64_t c = calculate_crc((uint8_t*)buf1+70, 10, c1);
			printf("..%s %lx\n", buf1, c);
		BRU()
		BRU()
		BRU()
		BRU()
			uint64_t c = calculate_crc((uint8_t*)buf1+70, 10, c1);
			if (c == crc) {
				found = true;
				cnt = 2;
				goto E7;
			}
		BRE()
		BRE()
		BRE()
		BRE()
		BRE()
		BRE()
		E7:

		if (!found) printf(":<\n");
		printf("%s ", buf1);
		printf("%d ", cnt);
						uint64_t c = calculate_crc((uint8_t*)buf1, 80, 0);
		printf("\t%lx %lx\n", c, crc);
	}
}




