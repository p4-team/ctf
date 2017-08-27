/*
 *
 *  Filename: encryptor.c
 *  Description: My 1337 s3cur3 encrypt0r
 *  Author: Mad Sc0lTrAg <vyasa2004@antimozg.ru>
 *  Comment: Comments are for n00bz
 *
 */

#include <ctype.h>
#include <errno.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <unistd.h>

void encrypt(uint8_t * buffer, uint32_t lfsr, uint32_t poly, unsigned int length)
{
    for(uint32_t i = 0; i != length; i++)
    {
        for(uint8_t j = 7;; j--)
        {
            unsigned char lsb = lfsr & 1;
            buffer[i] ^= lsb<<j;
            lfsr >>= 1;
            if (lsb)
                lfsr ^= poly;
            if (j == 0) break;
        }
    }
}

uint32_t parse_int(char * str)
{
    char *endptr;
    uint32_t val = strtoul(str, &endptr, 16);
    if (endptr == str || *endptr != '\0') 
    {
        fprintf(stderr, "%s is not a valid hex number\n", str);
        exit(1);
    }
    return val;
}

int main(int argc, char ** argv)
{
    struct stat sb;
    off_t len;
    char *p;
    int fd;
    int c;
    int index;
    char * kvalue = NULL;
    char * pvalue = NULL;
    if (argc < 5) {
        fprintf (stderr, "usage: %s -k hex_number -p hex_number <file>\n", argv[0]);
        return 1;
    }
    while ((c = getopt (argc, argv, "p:k:")) != -1)
        switch (c)
        {
        case 'k':
            kvalue = optarg;
            break;
        case 'p':
            pvalue = optarg;
            break;
        case '?':
            if (optopt == 'k')
                fprintf (stderr, "Option -%c requires an argument.\n", optopt);
            else if (optopt == 'p')
                fprintf (stderr, "Option -%c requires an argument.\n", optopt);
            else if (isprint(optopt))
                fprintf (stderr, "Unknown option `-%c'.\n", optopt);
            else
                fprintf (stderr, "Unknown option character `\\x%x'.\n", optopt);
            return 1;
        default:
            abort ();
        }
    char * file_name = argv[optind];
    uint32_t key = parse_int(kvalue);
    uint32_t poly = parse_int(pvalue);
    fd = open (file_name, O_RDWR);
    if (fd == -1) {
        fprintf(stderr, "Cannot open file %s for writing: %s\n", argv[optind], strerror(errno));
        return 1;
    }
    if (fstat (fd, &sb) == -1) {
        fprintf(stderr, "Cannot stat file %s: %s\n", argv[optind], strerror(errno));
        return 1;
    }
    if (!S_ISREG (sb.st_mode)) {
        fprintf (stderr, "%s is not a file\n", argv[optind]);
        return 1;
    }
    p = mmap (0, sb.st_size, PROT_WRITE | PROT_READ, MAP_SHARED, fd, 0);
    if (p == MAP_FAILED) {
        perror ("mmap failed:");
        return 1;
    }
    encrypt(p, parse_int(kvalue), parse_int(pvalue), sb.st_size);
    if (close (fd) == -1) {
        perror ("close");
        return 1;
    }
    if (munmap (p, sb.st_size) == -1) {
        perror ("munmap");
        return 1;
    }
    return 0;
}
