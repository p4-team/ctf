# Shall we play a game (re 113p, 111 solved)

This turned out to be a very annoying challenge, because I was working on the x86 version of it, and it was broken and didn't give the proper flag.
As a result I solved this task 3 times, with 3 different methods, which is worth writing down.

The challenge is a simple [Android App](app.apk) with tic-tac-toe game.
We need to win 1M times to get the flag.

The code is not pure Java - there is also a native library with a single function.
Since the library was provided for ARM, x86 and x64 I was using x86 emulator, which is much faster than ARM, and this was a mistake, most likely not anticipated by the author.

My first approach to the task was to Reverse Engineer the code and figure out how the flag is calculated.
I didn't know Smali very well so I was not eager to dive into patching the app at this point.

I got the [decompiled code](app_source.zip) and started looking at what was happening there.
The important bits were (labelled by me):

```java
    Object f2329n = C0644N.m3217_(Integer.valueOf(3), C0644N.f2341h, Long.valueOf((((((((1416127776 + 1869507705) + 544696686) + 1852403303) + 544042870) + 1696622963) + 544108404) + 544501536) + 1886151033));
    int winCounter;
    boolean gameEnd;
    byte[] f2332q = new byte[32];
    byte[] f2333r = new byte[]{(byte) -61, (byte) 15, (byte) 25, (byte) -115, (byte) -46, (byte) -11, (byte) 65, (byte) -3, (byte) 34, (byte) 93, (byte) -39, (byte) 98, (byte) 123, (byte) 17, (byte) 42, (byte) -121, (byte) 60, (byte) 40, (byte) -60, (byte) -112, (byte) 77, (byte) 111, (byte) 34, (byte) 14, (byte) -31, (byte) -4, (byte) -7, (byte) 66, (byte) 116, (byte) 108, (byte) 114, (byte) -122};

    public GameActivity() {
        C0644N.m3217_(Integer.valueOf(3), C0644N.f2342i, this.f2329n, this.f2332q);
        this.winCounter = 0;
        this.gameEnd = false;
    }

    void showFlag() {
        Object _ = C0644N.m3217_(Integer.valueOf(0), C0644N.f2334a, Integer.valueOf(0));
        Object _2 = C0644N.m3217_(Integer.valueOf(1), C0644N.f2335b, this.f2332q, Integer.valueOf(1));
        C0644N.m3217_(Integer.valueOf(0), C0644N.f2336c, _, Integer.valueOf(2), _2);
        ((TextView) findViewById(R.id.score)).setText(new String((byte[]) C0644N.m3217_(Integer.valueOf(0), C0644N.f2337d, _, this.f2333r)));
        endTheGame();
    }

    void finishRound() {
        for (int i = 0; i < 3; i++) {
            for (int i2 = 0; i2 < 3; i2++) {
                this.f2327l[i2][i].m3222a(C0648a.EMPTY, 25);
            }
        }
        animateSomething();
        this.winCounter++;
        Object _ = C0644N.m3217_(Integer.valueOf(2), C0644N.f2338e, Integer.valueOf(2));
        C0644N.m3217_(Integer.valueOf(2), C0644N.f2339f, _, this.f2332q);
        this.f2332q = (byte[]) C0644N.m3217_(Integer.valueOf(2), C0644N.f2340g, _);
        if (this.winCounter == 1000000) {
            showFlag();
            return;
        }
        ((TextView) findViewById(R.id.score)).setText(String.format("%d / %d", new Object[]{Integer.valueOf(this.winCounter), Integer.valueOf(1000000)}));
    }
```

There are some constants at the top, but all the rest interesting parts use the `C0644N.m3217_` which is the native function call.
The native code didn't look very promising, so I decided to use a debugger to check what those calls do.

For this reason I started a new Android NDK Project, added the native lib to this project and cloned the computation part of the code (skipping all the animations, sounds etc).
With this setup I could stop the debugger after each of the native calls and see what got returned.

For example the first call in the constructor `C0644N.m3217_(Integer.valueOf(3), C0644N.f2342i, this.f2329n, this.f2332q);` creates a Random object and uses it to fill the buffer.
Native calls in the `showFlag` function do pretty much:

```java
            Cipher cipher = Cipher.getInstance("AES/ECB/NoPadding");
//            Cipher cipher = (Cipher) N.callNativeFun(0, N.f2334a, 0);
            SecretKeySpec key = new SecretKeySpec(this.keyBuffer, "AES");
//            Object key = N.callNativeFun(1, N.f2335b, this.keyBuffer, 1);
            cipher.init(Cipher.DECRYPT_MODE, key);
//            N.callNativeFun(0, N.f2336c, cipher, 2, key);
            Object decryptedFlag = cipher.doFinal(this.encryptedFlag);
//            Object decryptedFlag = N.callNativeFun(0, N.f2337d, cipher, this.encryptedFlag);
            String flag = new String((byte[]) decryptedFlag);
```

So they simply decrypt the flag from the buffers using AES-ECB.
Finish round function does:

```java
    void finishRound() {
        this.winCounter++;
        try {
            MessageDigest messageDigestDelegate = MessageDigest.getInstance("SHA-256");
//            Object messageDigestDelegate = N.callNativeFun(2, N.f2338e, 2);
            messageDigestDelegate.update(this.keyBuffer);
//            N.callNativeFun(2, N.f2339f, messageDigestDelegate, this.keyBuffer);
            this.keyBuffer = messageDigestDelegate.digest();
//            this.keyBuffer = (byte[]) N.callNativeFun(2, N.f2340g, messageDigestDelegate);
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
    }
```

So this function, apart from animations and sounds, calculates SHA256 hash over one of the buffers.
The whole "game" logic code boils down to:

```java
        for (int i = 0; i < 1000000; i++) {
            finishRound();
        }
        showFlag();
```


We can add logging to the constructor to recover the initial buffer states, and then simply run the algorithm to recover the flag:

```python
import hashlib

from Crypto.Cipher import AES


def main():
    ct = # initial value
    key = # initial value
    for i in range(1000000):
        key = hashlib.sha256(key).digest()
    encrypt = AES.new(key, AES.MODE_ECB)
    decrypted = encrypt.decrypt(ct)
    print(key.encode("hex"), decrypted.encode("hex"), decrypted)


main()
```

But since intially we used x86 emulator, the initial buffer values were incorrect and the result turned out not to be a proper flag.
We assumed that maybe there are some unusual things happening in the native lib, depending on the iteration steps, and the algorithm we reverse-engineered is not correct, or for some reason Android Java does something differently than the python counterpart.

This was still fine, we still had the Android NDK Project, so we could just add some logging for the final flag, and run the Android app on the emulator.
And this is what we did, but as can be expected, we got exactly the same results, in both cases - when using pure-java code, and when using calls for the native library.
And those results were consistent with what we got from python too.

This was strange, but we guessed that maybe the app is doing some strange things we didn't notice, or that maybe decompiler made a mistake somewhere.

We were left with last option - patching the Smali code in the app.
We started off by disassembling the code:

```
apktool d app.apk
```

By patching we could win the game, and still introduce as little changes to the original apk as possible.
We decided to add a loop around the call to the function we labelled `finishRound` in the OnClick handler, and loop over this 1M times, after the first win.
To make things faster we also removed the calls to animation and sounds functions:

```
	:goto_magic
	
    invoke-virtual {p0}, Lcom/google/ctf/shallweplayagame/GameActivity;->n()V
	
	iget v0, p0, Lcom/google/ctf/shallweplayagame/GameActivity;->o:I
	
	if-eqz v0, :cond_3
	goto :goto_magic
```


We also added some logging to certain functions, just to know what is going on.
For example:

```
.method n()V
    .locals 10
    
    iget v5, p0, Lcom/google/ctf/shallweplayagame/GameActivity;->o:I

    invoke-static {v5}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    move-result-object v1
    
    const-string v5, "wins"

    invoke-static {v5, v1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I
```

This tells us how many times we've won already, each time function `n` is called.

With such changes we could invoke:

```
apktool b test
```

To make a new apk file.
In order to run it we had to sign it as well:

```
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore app/dist/app.apk alias_name
```

And as might be expected, the result was again identical, but was still not a proper flag.

Fortunately at this point someone suggested that maybe we could run this on a real ARM Android device, just to be sure, and it turns out the [patched apk](app_patched.apk) worked like a charm on ARM device and finally gave the flag: `CTF{ThLssOfInncncIsThPrcOfAppls}`
