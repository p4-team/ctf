# pwn02 (pwn 130p, 37 solved)

## Exploitation

1. Add a book with a short brief

   The purpose is to create brief that can be enlarged and edited during use-after-free exploitation.

2. Add a best selling book

   Book to be used as use-after-free victim via `The best selling book today` section of `List` output.

3. Enter use-after-free state by deallocating the best selling book

   Deallocate the best selling book by removing it *two* times.
   This is due to details of reference counting implementation.

4. Leak `libc` address by exploiting use-after-free vulnerability

   Enlarge the brief of first book to reuse the memory chunk of the deallocated best selling book.

   Leak `libc` address by overwriting brief pointer of the best selling book with location of `.got` entry and executing `List` command.

5. Execute interactive shell by exploiting use-after-free vulnerability

   Call `system("/bin/sh")` by overwriting brief pointer and the formatter function of the best selling book and executing `List` command.

Full exploit is attached [here](exploit.py).
