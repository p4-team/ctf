#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#include "aes.h"

#define MAX_KEY_LEN 16
#define KEY_SIZE_LEN 1
#define ENTRY_SIZE (MAX_KEY_LEN + KEY_SIZE_LEN)
#define NUM_KEYS 16
#define STORAGE_SIZE (ENTRY_SIZE * NUM_KEYS)
#define MASTER_KEY_INDEX 0
#define DATA_SIZE 16

uint8_t keys[STORAGE_SIZE];
uint8_t data[DATA_SIZE];
uint8_t current_key[MAX_KEY_LEN];

void regenerate_key(unsigned int index, unsigned int len) {
	unsigned int offset = index * ENTRY_SIZE;

	if (offset > STORAGE_SIZE - ENTRY_SIZE || len > MAX_KEY_LEN) {
		return;
	}

	int fd = open("/dev/urandom", O_RDONLY);
	read(fd, &keys[offset], len);
	close(fd);
	keys[offset + MAX_KEY_LEN] = len;
}


// [(MAX_KEY_LEN, KEY_SIZE_KEN), (MAX_KEY_LEN, KEY_SIZE_KEN), (MAX_KEY_LEN, KEY_SIZE_KEN), (MAX_KEY_LEN, KEY_SIZE_KEN) ...]

// index > NUM_KEYS - 1

void load_key(unsigned int index) {
	unsigned int offset = index * ENTRY_SIZE;
	unsigned int key_len = keys[offset + MAX_KEY_LEN];
	if (offset > STORAGE_SIZE - ENTRY_SIZE || key_len > MAX_KEY_LEN) {
		return;
	}
	memcpy(current_key, &keys[offset], key_len);
}

void encrypt(void) {
	uint8_t data_out[DATA_SIZE];
	AES128_ECB_encrypt(data, current_key, data_out);
	write(1, data_out, 16);
}

void load_data(void) {
	int ret;

	read(0, data, DATA_SIZE);
    if (ret < 1)
        exit(0);
}

int main(void) {

	int i;
	for (i = 0; i < NUM_KEYS; i++) {
		regenerate_key(i, MAX_KEY_LEN);
	}

	int fd = open("flag.txt", O_RDONLY);
	read(fd, data, DATA_SIZE);
	close(fd);

	load_key(MASTER_KEY_INDEX);
	encrypt();

	memset(data, 0, DATA_SIZE);
	regenerate_key(MASTER_KEY_INDEX, MAX_KEY_LEN);

	char cmd;
  int ret;
	unsigned int p1, p2;
	while(1) {
		ret = read(0, &cmd, 1);
        if (ret < 1)
            return 0;
		if (cmd == 'l') {
			load_data();
		} else if (cmd == 'e') {
			encrypt();
		} else if (cmd == 'r') {
			ret = read(0, &p1, sizeof(p1));
			if (ret < 1)
				return 0;
			read(0, &p2, sizeof(p2));
			if (ret < 1)
				return 0;
			regenerate_key(p1, p2);
		} else if (cmd == 'k') {
			read(0, &p1, sizeof(p1));
			if (ret < 1)
				return 0;
			load_key(p1);
		}
	}
}
