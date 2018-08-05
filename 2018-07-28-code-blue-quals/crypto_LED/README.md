# LED (crypto, 19 solved, 315p) 

## step 1

I analyzed function `Lazy_LED_enc` with parameter `rounds` set to `1` .
This function receives also password and key in nibbles list in an arguments.

I discovered that if you remove last step from this function which is a random permutation:

```python
  ret2 = ""
  for i in range(16):
    ret2 += ret[ sbox_lazy[i] ] # Now it's safe!
```

there are sets that every 4 nibbles in the key are responsible for other 4 nibbles in the output in constant place without changing the rest of key.


Here is a map which nibbles in key are responsible for which nibbles in the output of function `Lazy_LED_enc` when the last permutation is removed:

```
0, 5, 10, 15  ->  0, 4, 8, 12
1, 6, 11, 12  ->  1, 5, 9, 13
2, 7, 8, 13   ->  2, 6, 10, 14
3, 4, 9, 14   -> 3, 7, 11, 15
```

for example if some nibbles in key at positions `0,5,10,15` change, the output will change only at postions `0, 4, 8, 12` as long as password is the same.

You can easily brute-force every set of nibbles and recover the first 8 bytes of the key.

Now, lets consider this function with the last step not removed.
The last step is only a random permutation - bytes are unchanged but they only change their own positions.

The solution is to probe the function before brute-forcing the key.
You call this function several times for the same nibble set with different password to see at which positions nibbles changes.
Now you can brute-force every 4 set of nibbles of key.

In this step you brute-forced the first 8-bytes of key.

## step 2

Now if you have first 8-bytes of the key you can recover the random permutation - the last step in function `Lazy_LED_enc`.
Still keep calling this function with `rounds` set to `1`.

This is easy step.

## step 3

Let's break the second half of the key. It is again 8 bytes.
Now function `Lazy_LED_enc` is called with `rounds` set to `5`.
At this step you know what is the output of `Lazy_LED_enc` with `rounds=4` and the first half of key set to the value of real key.
Now, if `rounds=5` the second half of key is xored with state and now are made the same computations as in the `Lazy_LED_enc` with `rounds=1`.
You can request server with known password and `rounds=5` and now, you can brute force every nibble set at your CPU.

## step 4

The requirement in this task was that the connection with this server can take max `1 minute`.
The optimizations I made is to make computations before the connection with the server if it was possible,
multithreading for computations on CPU,
caching server responses
and making less requests to the server.

## python script

Sometimes it creashes - run it once again.

[script.py](script.py)
