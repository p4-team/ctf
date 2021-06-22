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

The task is clearly to leak content of the text file by abusing the executable.

The binary reads the secret from `flag.txt` file at startup and starts a simple service implementing the following commands:
* `ResizeCommand` to resize an internal buffer,
* `ReadSecretCommand` to copy an arbitrary slice of the secret into an arbitrary location within the buffer,
* `ScrambleCommand` to xor an arbitrary slice of the buffer with provided key and store the result into a new location within the buffer, and
* `StopCommand` to terminate the service.

There are no known programming bugs in the binary and the hint points to hardware issues.

Turns-out that Travis Downs blogged about [Hardware Store Elimination](https://travisdowns.github.io/blog/2020/05/13/intel-zero-opt.html) a few months before the CTF, describing an obscure optimization implemented by some Intel CPUs.
The optimization allows to significantly improve throughput of specific memory operations on blocks of zeros.

The above microarchitectural optimization can be abused as an oracle to leak the secret from the analysed service.

## Exploitation

Our [solver](solver/solver.cxx) checks the secret byte-by-byte.
For each position in the secret, all possible 256 xor keys are tested.
The xor result is replicated multiple times within the buffer, such that we end-up with a large block of zeros once the xor key matches the secret byte.
This is sufficient to affect the service performance, such that effect can be observed from another process.

And so we can successfully reveal the content of `flag.txt`:
```
p4{zero_values_move_faster}
```

## Post Mortem

While content-dependent optimizations may be risky in general, we cannot think of any practical abuse of _Hardware Store Elimination_ against real-world applications.

However Intel [reportedly](https://travisdowns.github.io/blog/2021/06/17/rip-zero-opt.html) found some reasons to [disable this optimization](https://www.intel.com/content/www/us/en/security-center/advisory/intel-sa-00464.html) with the most recent microcode update.
