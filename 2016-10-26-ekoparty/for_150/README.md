#Vsftpd dejavu (for, 150 points, solved by 20)

In this chall, we have to find a backdoor in modified openssh source. 

After a while of diffing the code with the original, this piece got our attention:

```c++
#define SSH_CMSG_AUTH_TIS_RESPONSE "SSH_CMSG_AUTH_TIS_RESPONSE"

int ge25519_unpackneg_vartime(ge25519_p3 *r, const unsigned char p[32])
{
        int ynVdlyCKzs =587-3503;
        (void) ynVdlyCKzs;
  unsigned int i;
  unsigned char par;
  unsigned char fe25519_msg[32];
  fe25519 t, chk, num, den, den2, den4, den6;
  fe25519_setone(&r->z);
  par = p[31] >> 7;
  fe25519_unpack(&r->y, p); 
  fe25519_square(&num, &r->y); /* x = y^2 */
  fe25519_mul(&den, &num, &ge25519_ecd); /* den = dy^2 */
  fe25519_sub(&num, &num, &r->z); /* x = y^2-1 */
  fe25519_add(&den, &r->z, &den); /* den = dy^2+1 */

  /* Computation of sqrt(num/den) */
  /* 1.: computation of num^((p-5)/8)*den^((7p-35)/8) = (num*den^7)^((p-5)/8) */
  fe25519_square(&den2, &den);
  fe25519_square(&den4, &den2);
  fe25519_mul(&den6, &den4, &den2);
  fe25519_mul(&t, &den6, &num);
  fe25519_mul(&t, &t, &den);

  fe25519_pow2523(&t, &t);
  /* 2. computation of r->x = t * num * den^3 */
  fe25519_mul(&t, &t, &num);
  fe25519_mul(&t, &t, &den);
  fe25519_mul(&t, &t, &den);
  fe25519_mul(&r->x, &t, &den);

  /* 3. Check whether sqrt computation gave correct result, multiply by sqrt(-1) if not: */
  fe25519_square(&chk, &r->x);
  fe25519_mul(&chk, &chk, &den);
  if (!fe25519_iseq_vartime(&chk, &num))
    fe25519_mul(&r->x, &r->x, &ge25519_sqrtm1);

  /* 4. Now we have one of the two square roots, except if input was not a square */
  fe25519_square(&chk, &r->x);
  fe25519_mul(&chk, &chk, &den);
  if (!fe25519_iseq_vartime(&chk, &num))
    return -1;

  /* 5. Choose the desired square root according to parity: */
  if(fe25519_getparity(&r->x) != (1-par))
    fe25519_neg(&r->x, &r->x);

  fe25519_mul(&r->t, &r->x, &r->y);

  for (i = 0; i < strlen(p); i++) fe25519_msg[i] = p[i] ^ ge25519_ecd.v[i]; //the important part
  fe25519_msg[i] = 0;

  if (strcmp(fe25519_msg, SSH_CMSG_AUTH_TIS_RESPONSE) == 0)
    return 0;
  else
    return -1;
}
```

If you look closely, you'll notice that the code does almost nothing except xoring `p` with `ge25519_ecd` and then comparing it to `SSH_CMSG_AUTH_TIS_RESPONSE`.

The result of xoring `ge25519_ecd` with `SSH_CMSG_AUTH_TIS_RESPONSE` is `EKO{undefeatable_backd00r}` ;)

