#include <stdio.h>
#include <stdbool.h>
#include <stdarg.h>
#include <string.h>

uint16_t be2le(uint16_t be) {
    return (be << 8) | (be >> 8);
}

#pragma pack(0)
struct packet {
    uint16_t hash;
    uint16_t magic1;
    uint16_t conn_id;
    uint16_t seq_id;
    uint16_t unk2;
    uint8_t raw[10000];
} buf;

bool data_only = false;
bool text_dump = false;
bool decrypt = false;

void print_info(const char *fmt, ...) {
    if (data_only) { return; }

    va_list args;
    va_start(args, fmt);
    vprintf(fmt, args);
    va_end(args);
}

uint8_t getxor(int ndx, uint16_t current_hash) {
    if (!decrypt) { return 0; }
    return (ndx % 2 == 0)
        ? (current_hash & 0x00FF)
        : (current_hash & 0xFF00) >> 8;
}

int main(int argc, char *argv[]) {
    FILE *f = fopen("rawdata.bin", "rb");

    for (int i = 1; i < argc; i++) {
        if (argv[i][0] != '-') {
            printf("Invalid argument: %s\n", argv[i]);
        }
        for (int j = 1; j < strlen(argv[i]); j++) {
            switch (argv[i][j]) {
                case 'd': data_only = true; break;
                case 't': text_dump = true; break;
                case 'c': decrypt = true; break;
            }
        }
    }

    for (int packet_ndx = 0; ; packet_ndx++) {
        uint16_t packet_len;
        int read = fread(&packet_len, 1, sizeof packet_len, f);
        if (read == 0) { 
            break;
        }
        packet_len = be2le(packet_len);

        if (packet_len == 0x454e) {
            uint8_t c;
            fread(&c, 1, 1, f);
            if (c != 0x44) {
                print_info("Ups :|.\n"); return 1;
            }
            print_info("END PACKET\n");
            continue;
        }

        print_info("PACKET %d\n", packet_ndx);
        
        print_info(" - size: %d bytes\n", packet_len);
        fread(&buf, 1, packet_len - 2, f);
        buf.hash = be2le(buf.hash);
        buf.magic1 = be2le(buf.magic1);
        buf.conn_id = be2le(buf.conn_id);
        buf.seq_id = be2le(buf.seq_id);
        buf.unk2 = be2le(buf.unk2);

        print_info(" - hash: %2x\n", buf.hash);
        print_info(" - magic1: %2x\n", buf.magic1);
        print_info(" - conn_id: %2x\n", buf.conn_id);
        print_info(" - seq_id: %2x\n", buf.seq_id);
        print_info(" - unk2: %2x\n", buf.unk2);

        uint16_t current_hash = be2le(0xe9f9) + buf.hash;
        print_info(" - calculated hash: %2x\n", current_hash);

        print_info(" - rawdata:\n");

        int raw_len = packet_len - 12;
        for (int i = 0; i < raw_len; i += 16) {
            if (i != 0) { printf("\n"); }
            if (!data_only) { printf("   "); }

            for (int j = 0; j < 16; j++) {
                uint8_t c = buf.raw[i+j] ^ getxor(j, current_hash);
                if (i + j < raw_len) {
                    printf(" %02x", c);
                } else {
                    printf("   ");
                }
            }

            if (text_dump) {
                printf("   ");
                for (int j = 0; j < 16; j++) {
                    uint8_t c = buf.raw[i+j] ^ getxor(j, current_hash);
                    if (i + j < raw_len) {
                        printf("%c", c >= ' ' && c <= '~' ? c : '.');
                    } else {
                        printf(" ");
                    }
                }
            }
        } printf("\n");
    }
}
