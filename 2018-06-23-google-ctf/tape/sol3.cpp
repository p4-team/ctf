#include <cstdio>
#include <cstdint>

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

char buf1[100] = ": You probably just want the flag.  So here it is: CTF{dZXi----------PIUTYMI}. :";
char buf2[] =    ": You probably just want the flag.  So here it is: CTF{dZXi\xff\x9a\xc3\x25\x99\xee\xb2\x41--PIUTYMI}. :";
uint64_t wantcrc = 0x30d498cbfb871112;


int main() {
	generate_table();
	// Set dashes, so that:
	// wantcrc == calculate_crc(buf1, 80, 0);
	printf("%lx\n", calculate_crc((uint8_t*)buf2, 80, 0));
}
