# Xor-as-a-Service (misc)

```
Xor-as-a-Service is the new hot thing. And we think it's unbreakable!

Hint: nosmt, mds=full and clear of secret dependent algorithms.
```

## Analysis

After solving proof of work, you are given a shell session on a Linux machine.

The `/app` directory contains files of interest that are owned by another user:
* `flag.txt` with permissions "-r--------", and
* `xaas` with permissions `-r-sr-xr-x`

The task is clearly to leak content of the text file by abusing executable.

The binary reads the secret from `flag.txt` file at startup and starts a simple service implementing the following commands:
* `ResizeCommand` to resize an internal buffer,
* `ReadSecretCommand` to copy an arbitrary slice of the secret into an arbitrary location within the buffer,
* `ScrambleCommand` to xor an arbitrary slice of the buffer with provided key and store result into new location within the buffer, and
* `StopCommand` to terminate the service.

There are no known programming bugs in the binary and the hint points to hardware issues.

Turns-out that Travis Downs posted a blog [Hardware Store Elimination](https://travisdowns.github.io/blog/2020/05/13/intel-zero-opt.html) a few months before the CTF that described an obscure optimization implemented by some Intel CPUs.
The optimization is that CPU may significantly improve throughput of specific memory operations when operating on blocks of zeros.

The above microarchitectural optimization can be abused as an oracle to leak the secret.

## Exploitation

Our [solver](solver/solver.cxx) checks secret byte-by-byte.
For each position in the secret, all possible 256 xor keys are tested.
The xor result is replicated multiple time within the buffer, such that we end-up with large block of zeros once the xor key matches the secret byte.
This is sufficient to affect the service performance, such that effect can be observed from another process.

And so we can successfully reveal the content of `flag.txt`:
```
p4{zero_values_move_faster}
```
