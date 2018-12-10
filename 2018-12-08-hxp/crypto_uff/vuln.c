#define _POSIX_C_SOURCE 1
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/random.h>
#include <sys/sendfile.h>

#include "tweetnacl.h"

#define Q 1000
#define K 8

void randombytes(unsigned char *p, size_t n)
{ for (ssize_t r = 0; n -= r; p += r) if (0 > (r = getrandom(p, n, 0))) exit(-1); }

static void print_hex(unsigned char const *p, size_t n)
{ for (size_t i = 0; i < n; ++i) printf("%02hhx", p[i]); }

static size_t read_hex(unsigned char *p, size_t n)
{ for (size_t i = 0; i < n; ++i) if (1 != scanf("%02hhx", p + i)) return i; return n; }

struct keypair {
    unsigned char pk[32], sk[32];
} __attribute__((packed)) keys[K];

void init_keys()
{
    for (unsigned i = 0; i < K; ++i)
        crypto_sign_keypair(keys[i].pk, keys[i].sk);
}

unsigned find(unsigned char const *pk)
{
    unsigned idx;
    for (idx = 0; idx < K; ++idx)
        if (!strncmp(pk, keys[idx].pk, 32))
            break;
    return idx;
}

size_t sign(unsigned char *m, unsigned long long n, unsigned char const *pk, unsigned char const *sk)
{
    struct keypair k;
    memcpy(k.sk, sk, sizeof(k.sk));
    memcpy(k.pk, pk, sizeof(k.pk));
    crypto_sign(m, &n, m, n, (char *) &k);
    return n;
}

bool verify(unsigned char const *sm, unsigned long long n, unsigned char const *pk)
{
    char m[n];
    return !crypto_sign_open(m, &n, sm, n, pk);
}

void dump_flag()
{
    if (system("cat flag.txt")) {
        fprintf(stderr, "fl0g is kapot??\n");
        exit(-1);
    }
}

int main()
{
    init_keys();

    printf("Welcome to the Ed25519 existential forgery game!  Enjoy and good luck.\n");

    for (unsigned i = 0; i < K; ++i) {
        printf("public key: ");
        print_hex(keys[i].pk, sizeof(keys[i].pk));
        printf("\n");
    }

    char nope[Q][256];
    for (unsigned i = 0; i < Q; ++i) {
        char pk[32], m[320];
        unsigned idx, n;

        printf("public key> "); fflush(stdout);
        if (sizeof(pk) != read_hex(pk, sizeof(pk)) || K == (idx = find(pk)))
            break;

        printf("length>     "); fflush(stdout);
        if (1 != scanf("%u", &n) || n > 256)
            break;

        printf("message>    "); fflush(stdout);
        if (n != read_hex(m, n))
            break;

        memcpy(nope[i], m, n);
        memset(nope[i] + n, 0, sizeof(nope[i]) - n);

        printf("signed:     ");
        print_hex(m, sign(m, n, keys[idx].sk, pk));
        printf("\n");
    }

    char sm[320];
    printf("forgery>    "); fflush(stdout);
    unsigned long long n = read_hex(sm, 320);

    for (unsigned i = 0; i < Q; ++i) {
        if (!memcmp(sm + 64, nope[i], n - 64)) {
            printf("nope!\n");
            exit(0);
        }
    }

    for (unsigned i = 0; i < K; ++i)
        if (verify(sm, n, keys[i].pk)) {
            dump_flag();
            exit(0);
        }

    printf("nope!\n");
}

