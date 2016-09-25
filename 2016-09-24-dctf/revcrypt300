# Decoy (RevCrypt 300)

> https://dctf.def.camp/quals-2016/re300.bin

The binary had a lot of dead ends and some code hidden behind impossible checks, such as `if(1==2)`. The binary also
checked whether `SP_K` environmental variable is defined, and if so, decreased a certain global variable.
To increase running time, the code was encrypted using an algorithm exponentially complex in terms of key length, which
fortunately was just 8 in this case - there was also a function genreating primes up to around 3000 and then doing nothing
with them - all probably to reduce brute forcing attempts. The code then tried to submit the decrypted flag to the server
using CURL library, but it didn't work because of wrong pinned certificate - just another annoyance to be patched out.
The flag (server response) wasn't even printed out, so I had to see it in the debugger. One final thing - as one of 
destructors, the binary was modifying the stored flag, so the breakpoint had to be set after they are done, far behind the end
of main.
