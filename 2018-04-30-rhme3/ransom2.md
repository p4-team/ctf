# Ransom 2.0, RE, 150pts

> In theory, this firmware mod was supposed to give you 30% extra horsepower and torque. In reality, it's something different. For real this time.

This is the exact same challenge as `Ransom`, except this time
with the password checking bugfix. Reversing the code checking
routine revealed the underlying algorithm, which we rewrote
into C:

```c
#include <stdint.h>
#include <stdio.h>

uint16_t cash = 0x1337;

uint16_t get(uint16_t n) {
	while (n--) {
		cash = (((cash ^ (cash >> 2) ^ (cash >> 3) ^ (cash >> 5)) & 1) << 15) | (cash >> 1);
	}
	return cash;
}

int main() {
	uint8_t id[] = "\x38\x35\x32\x07\x19\x00\x14\x00";
	for (int i = 0; i < 8; i++) {
		uint16_t x = id[i] + (id[i+1] * 256);
		uint16_t f = get(x ^ (0xcafe << i));
		printf("%02X%02X", f & 0xff, (f >> 8) & 0xff);
	}
	printf("\n");
}
```

Running this yields the password, which upon typing it into UART
interface, gives us the flag.