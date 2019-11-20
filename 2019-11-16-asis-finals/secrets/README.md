# Secrets (Forensics, 304p, 10 solved)

In the challenge we get an archive with a bunch of PNG files.
Initial analysis shows only 2 strange strings:

1. `no SecDrive`
2. base64 encoded `the password is: atalmatal`

After some extensive googling we finally found https://github.com/mgeitz/albumfs which seemed to fit our task perfectly.
We tried using any of the files as `root` and for `amy.png` with drive name `SecDrive` and password `atalmatal` we managed to get appropriate response that in fact there are 70 bytes stored over 2 image files.

Unfortunately the tool crashed with segfault without giving us the flag.
We debugged it for a while until we found the reason:

https://github.com/mgeitz/albumfs/blob/master/afs.c#L562

```c
png_data *new_img = malloc(sizeof(png_data)); // 1
char tmp[strlen(new_img->md5)]; // 2
readBytes((void *) new_img->md5, sizeof(new_img->md5), offset);
offset = offset - sizeof(new_img->md5);
while ((dir = readdir(FD)) != NULL) {
    memset(tmp, 0, sizeof(new_img->md5)); // 3
```

Author of the library mallocs some memory (1) and then creates a temporary stack based buffer, but size of this buffer is calculated via `strlen(new_img->md5)` (2).
Strlen called on just allocated memory!
Finally author zeros this temporary buffer (3) this time using proper `sizeof(new_img->md5)`.

As a result, unless you're very lucky, this causes stack smashing and application segfaults.
In order to solve the challenge we simply set the tmp buffer to have some reasonably large static size.

Once we mount the drive we get `ASIS{21a0fc15ce259585afd14ac1210fcdd2162cd897}`
