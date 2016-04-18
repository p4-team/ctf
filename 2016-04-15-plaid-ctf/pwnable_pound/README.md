# pound (Pwnable, 290pts, 20 solves)

In this task, we were given service running `host.py`. It had two functions:
- printing some tweets stored as files
- compiling a binary using user supplied two macros.

We quickly noticed that we could exploit the first function: giving it
`../pound.c` gave us source of compiled binary. In general, we were able
to read any file in the system (readable by our user).

Looking at `pound.c`, we do not see any obvious vulnerabilities. However, since
we control two macros, we were able to create a buffer overflow in this structure:
```
const int N=1024;

const int l1_len = L1;
const int l2_len = L2;

#define STATE_SIZE_LEN 512

struct global_s {
    int s1_citizens[l1_len];
    int s2_citizens[l2_len];
    char s1_name[STATE_SIZE_LEN]; // Name of state 1
    char s2_name[STATE_SIZE_LEN]; // Name of state 2
    char *announcement;
    int announcement_length;
    int secret;
} global;
```
We were able to define L1 and L2 as any strings, up to 3 characters long. This turned up
to be quite problematic when generating a vulnerable binary. However, with L1 defined as
`N^9` and L2 as `N*N`, the following line had an error:
```
    int length_diff = L2 - L1;
```
This was supposed to calculate difference beween these two constants, but with C operator
precedence, `N*N - N^9` actually meant `(N*N - N)^9`, which gave us an overflow allowing us
to control the `announcement` field in the global structure.

I created a script (`get_binary.py`) downloading their compiled version of the binary 
(`their_binary`), in case their compilation process differs from the one on our machine.

At this point, I gave the task to another team member, so no final exploit is given here. 
As far as I know, he was able to overwrite that `announcement` field and then use program
code to overwrite GOT entry and eventually exploit the binary to the end.
