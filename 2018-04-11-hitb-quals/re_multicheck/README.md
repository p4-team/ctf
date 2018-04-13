# Multicheck (re)

The task was a mobile (android) reversing challenge.
We get [android app](multicheck.apk) to work with.
After decompiling we can see there is only [a single class there](MainActivity.java).

What is does is loading from resources file `claz.dex` (in method `m2541i`) and then loading method `check` from class `com.a.Check`, and using this method to validate the password.

If we decompile the `claz.dex` from resources we do get [Check class](Check.java), but it turns out to be a red herring with `this is not the flag` message.

Last piece of the puzzle is the native library which is in fact loaded by the main activity:

```java
static {
	System.loadLibrary("check");
}
```

It's ARM dynamic library, and if we look into it we find an interesting function at `0x1380`:

```c
int sub_1380(int arg0, int arg1, int arg2) {
    stack[2043] = r4;
    *((sp - 0x14) + 0xfffffffffffffffc) = r8;
    r5 = arg0;
    r8 = arg2;
    r6 = arg1;
    r4 = *0x474c;
    if (r4 == 0x0) {
            r4 = malloc(0x100);
            *0x474c = r4;
            *0x4750 = malloc(0x100);
    }
    sprintf(r4, 0x1450);
    readlink(*0x474c, *0x4750, 0x100);
    if (sub_1318(*0x4750, "claz.dex") != 0x0) {
            if (*(int8_t *)0x4754 == 0x0) {
                    r4 = malloc(**0x3f40);
                    if (**0x3f40 >= 0x1) {
                            r0 = 0xe9;
                            r1 = 0x0;
                            do {
                                    *(r4 + r1) = *(int8_t *)(*0x3f44 + r1) ^ r0;
                                    r1 = r1 + 0x1;
                                    r0 = r0 + 0x1;
                            } while (r1 < **0x3f40);
                    }
                    write(r5, r4, **0x3f40);
                    free(r4);
                    *0x4754 = 0x1;
            }
            r0 = r8;
    }
    else {
            r0 = loc_29c4();
    }
    return r0;
}
```

What it does is actually "decrypt" (via simple xor) a real `claz.dex` file.
We can therefore repeat the same operation and recover dex and then decompile it, getting [real Check.java](CheckReal.java) class.

This one is a bit more complex than the fake one.

There is a static array with expected values, some encryption-like function is called on our input, and then compared with this array.

```java
public static boolean CheckReal(String str) {
	return Arrays.equals(CheckReal.m1a(str.getBytes()), f1b);
}
```

Functions `m4a` and `m3a` are easy enough to label.
First one takes array of bytes and combines those bytes into 32 bit integers.
Second one does the reverse, so takes array of integers and splits them into separate bytes.
Function `m0a` simply makes sure we're working with unsigned byte values.
Function `m1a` creates payload to encrypt from our input, and then encrypts the data in 8-byte blocks.

What we really need to invert is function `m2a` which does the actual encryption.
This function is very complex to read:

- combine the 8 bytes input into two 32-bit integers
- perform some XOR and arithmetic operations in 32 loop iterations
- split the result back into 8 bytes array

Fortunately for us the whole process is invertible, because we can simply perform all those operations backwards:

```java
    static byte[] decode8Bytes(byte[] inputData, int startIndex) {
        int[] combined = CheckReal.combine8BytesIntoTwo32bitInts(inputData, startIndex);
        int firstInt = combined[0];
        int secondInt = combined[1];
        int i5 = 0;
        for (int i = 0; i < 32; i++) {
            i5 -= 1640531527;
        }
        int const1 = f0a[0];
        int const2 = f0a[1];
        int const3 = f0a[2];
        int const4 = f0a[3];
        for (int i = 0; i < 32; i++) {
            secondInt -= (((firstInt << 4) + const3) ^ (firstInt + i5)) ^ ((firstInt >> 5) + const4);
            firstInt -= (((secondInt << 4) + const1) ^ (secondInt + i5)) ^ ((secondInt >> 5) + const2);
            i5 += 1640531527;
        }
        int[] result = new int[2];
        result[0] = firstInt;
        result[1] = secondInt;
        return CheckReal.splitIntoSeparateBytes(result);
    }
```

We can call this function on the expected results and recover the input:

```java
    public static void main(String[] args) {
        StringBuilder flag = new StringBuilder();
        for (int i = 0; i < 32; i += 8) {
            byte[] expectedInput = CheckReal.decode8Bytes(f1b, i);
            flag.append(new String(expectedInput));
        }
        System.out.println(flag);
    }
```

Which gives: `HITB{SEe!N9_IsN'T_bELIEV1Ng}`
