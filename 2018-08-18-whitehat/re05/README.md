# re5 (re, 120pts)


```bash
michal@DESKTOP-U3SJ9VI:/mnt/c/Users/nazyw/Downloads$ file ctfq.exe
ctfq.exe: PE32 executable (console) Intel 80386, for MS Windows
```

The binary is rather simple, it offers us 2 possibilities:

```c++
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v3; // ecx
  FILE *v4; // eax
  char v5; // al
  int v7; // [esp+0h] [ebp-4h]

  v7 = v3;
  init_socket();
  print_stuff("\n press 1 to input conmmand\n 2 to generate offline key\n 3 help? \n 4 exit\n");
  do
  {
    v4 = (FILE *)__acrt_iob_func(0);
    fflush(v4);
    gets((char *)&v7);
    v5 = v7;
    if ( (_BYTE)v7 == '1' )
    {
      send_command();
      v5 = v7;
    }
    if ( v5 == '2' )
    {
      encrypt_thing();
      v5 = v7;
    }
    if ( v5 == '3' )
    {
      print_stuff("id/command help have been sended to you email");
      v5 = v7;
    }
  }
  while ( v5 != '4' );
  return 0;
}
```

The first option allows us to send a message to the server in a following format:

```python
"%s|%s|%s|%s\n" % (command_id, command_name, company_name, other_data)
```

Since command_id has only 1000 possible values, let's try out all of them:


```python
from pwn import *

for i in range(1000):
	secret_id = str(i)
	command_name = "test"
	company_name = "test"
	other_data = "test"

	r = remote("66.42.55.226", 8888)
	r.send("%s|%s|%s|%s\n" % (secret_id, command_name, company_name, other_data))
	data = r.recv()

	if data != 'wrong id\n id looklike 000-999\n\x00':
		print(i, data)
```

Gave us:
```
(720, 'wrong id\n id looklike 000-999\n\x00')
```

After a bunch of guessing, we came up with:

A final script:
```python
from pwn import *

secret_id = 720
command_name = "view"
company_name = "fis"
other_data = "1111111111"

r = remote("66.42.55.226", 8888)
r.send("%s|%s|%s|%s\n" % (secret_id, command_name, company_name, other_data))
data = r.recv()

print(data)
```

Gives us a following string:
```
[+] Opening connection to 66.42.55.226 on port 8888: Done
vqmuwzjxfmqmdnfhr
\x00
[*] Closed connection to 66.42.55.226 port 8888
```

The second option in the menu allows us to encrypt a string using our company name, so we probably have to decrypt it.

```
  print_stuff("\n companyname:\n");
  gets(v10);
  print_stuff("\n secret key:\n");
  memset(v8, 0, 0x100u);
  gets(v9);
  v0 = 0;
  v1 = 0;
  v2 = strlen(v9);
  if ( v2 )
  {
    v3 = strlen(v10);
    do
    {
      if ( v0 == v3 )
        v0 = 0;
      v4 = v10[v0++];
      v8[v1++] = v4;
    }
    while ( v1 < v2 );
  }
  v5 = 0;
  if ( v2 )
  {
    do
    {
      if ( v6 >= 'a' && v6 <= 'z' )
        v9[v5] = ((unsigned __int8)v8[v5] + v6 - 192) % 27 + 0x60;
      ++v5;
    }
    while ( v5 < strlen(v9) );
  }
  return print_stuff("\nkey:%s\n", v9);
```

Nothing fancy:
```python
data = 'vqmuwzjxfmqmdnfhr'
company_name = 'fis'

# there is probably a smarter way of doing this ¯\_(ツ)_/¯
def et_tu_brute(c, f):
	for x in range(ord('a'), ord('z') + 1):
		if ((x + f - 192) % 27) + 0x60 == c:
			return x

flag = ''.join([chr(et_tu_brute(ord(x), ord(company_name[i % len(company_name)]))) for i,x in enumerate(data)])
print(flag)
```

Which gives us `phuongdonghuyenbi`