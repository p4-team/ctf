# Angel (RE, 468 points, 20 solves)
  
We're given a password-checking binary:


``` c++
int __cdecl sub_80485BF(char *input_str)
{
  int result; // eax@2
  char v2; // [sp+3h] [bp-15h]@1
  int v3; // [sp+4h] [bp-14h]@1
  size_t i; // [sp+8h] [bp-10h]@3

  v2 = *input_str;
  v3 = 0;
  if ( strlen(input_str) > 2 )
  {
    for ( i = 1; strlen(input_str) - 1 > i; ++i )
    {
      some_dark_magic(dword_804D148, &off_804C140 + 4 * (unsigned __int8)v2);
      if ( dword_804C060[v3] != dword_804D148((unsigned __int8)input_str[i]) )
        return puts("Wrong!");
      if ( ++v3 == 200 )
        break;
      v2 = input_str[i];
    }
    result = puts("Well done!");
  }
  else
  {
    result = puts("Wrong!");
  }
  return result;
}
```

There is some lookup-table stuff going on with `off_804C140` and some dark magic with `some_dark_magic` function ;)

We could reverse the whole program but we're lazy and the encryption has a cool property - the passwords nth check relies only on input bytes we've already analyzed.

This means that we could brute the correct input one byte at a time - we try to append every possible byte to the last successfull input and when we find a match we move one byte forward.

We came up with a nifty little gdb python script:

``` python
import os
import string
from subprocess import Popen, PIPE, STDOUT
import gdb
import codecs
import string
good_characters = 0

class MyBreakpoint(gdb.Breakpoint):

    def __init__(self, spec):
        super(MyBreakpoint, self).__init__(spec, gdb.BP_BREAKPOINT, internal = False)
        self.silent = True
 
    def stop (self):
        eax = int(gdb.parse_and_eval("$eax"))
        edx = int(gdb.parse_and_eval("$edx"))

        if eax == edx:
            global matches         
            matches += 1

        return False

MyBreakpoint('*0x08048656')

matches = 0
starting_piece = "you"

while True:
    for i in string.printable:

        potential_flag = starting_piece + i + "A"*30

        matches = 0

        with codecs.open("input.txt","w") as output_file:
            output_file.write(potential_flag)

        gdb.execute("r < input.txt > /tmp/a")

        if matches == len(starting_piece):
            starting_piece += i
            break;

    f = open("output", "wb")
    f.write(starting_piece)
```

We had to brute-force two first letters and then try about 4 different starting inputs but once we got overt that the script ran smoothly.

`you are looking for this EKO{4ngr_d1dn't_like_th1s}`

