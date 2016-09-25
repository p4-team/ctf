# dctfizer (RevCrypt 400)

> Format Response: DCTF{md5(sol)} https://dctf.def.camp/quals-2016/re400.bin 

> [UPDATE]: Initially it was MDCCCXLVI ...... don't even bother if you have nerve problems. 

> [UPDATE] Updated ciphertext again. This time key was modified too! --- http://pastebin.com/r4BndGiy

In this task, we got just the encrypted, hex-encoded file. It was easy to see some patterns were repeating, such as
`qEdocBqhc` or `8dwnel`. If we read them backwards, they are `chqBcodEq` and `lenwd8`, respectively, which seem similar
to `charCode` or `length` - some JavaScript function names - which seemed good, so we reversed the whole ciphertext. 
We found a couple of such ciphertext-plaintext pairs and noticed
that the lower nibbles of the character never changes - for example, `q` (ASCII 0x71) from `chqBcodE` was changed to `a`
(ASCII 0x61). We wrote an [interactive brute forcer](interactive.py), which allowed us to recover a couple
dozens of plaintext bytes:
```
`ufa,(hvensdio.(y{fq"p:];8)<7 <6 <8%<8'<9$<9 <7!<7$<8 <7)<8(<7&<8!<7%<6%<6&<8&<8"<7R={fq"p1][
 eval((function(){var j=[89,70,60,85,87,94,90,71,74,80,79,88,76,81,75,65,66,86,82,7B];var a=[
```
If we write higher nibble of ciphertext, of plaintext, and of their xor, we will get something like this:
```
`ufa,(hvensdio.(y{fq"p:];8)<7 <6 <8%<8'<9$<9 <7!<7$<8 <7)<8(<7&<8!<7%<6%<6&<8&<8"<7R={fq"p1][
 eval((function(){var j=[89,70,60,85,87,94,90,71,74,80,79,88,76,81,75,65,66,86,82,7B];var a=[
676622676676662277672735332332332332332332332332332332332332332332332332332332332335376727355
267662267667666227767263533233233233233233233233233233233233233233233233233233233234537672635
411040411011004050115556601101101101101101101101101101101101101101101101101101101101641155560
```
We can notice a pattern: lower row is xor of last two numbers on top row. With this in mind, we wrote a [script](solv.py)
to decrypt the whole file.

The decrypted file was the following script (after unpacking and unminifying):
```javascript
var _$_ddec = [ "toString", "charCodeAt", "length", "0", "map", "", "split", "join", "fromCharCode", "max", "log", "dctfizer", "undctfizer", "So what exactly do you want?" ];
 
function goToHex(b) {
    var c = b["split"]("")["map"](function(d) {
        var e = d["charCodeAt"](0)["toString"](16);
        return e["length"] == 1 ? "0" + e : e;
    });
    return c["join"]("");
}
 
function backFromHex(b) {
    var c = "";
    for (var a = 0; a < b["length"]; a += 2) {
        c += String["fromCharCode"](parseInt(b[a] + b[a + 1], 16));
    }
    return c;
}
 
function memoryGood(b, l) {
    var f = [];
    var g = 0;
    for (var a = 0; a < 234; a++) {
        f[a] = a;
    }
    for (a = 0; a < Math["max"](234, b["length"]); a++) {
        var h = l["charCodeAt"](a);
        l += String["fromCharCode"]((h << 1 | h >> 7) & 255);
    }
    console["log"](l["charCodeAt"](4));
    for (a = 0; a < 234; a++) {
        g = (g + f[a] + l["charCodeAt"](a)) % 234;
        f[a] ^= f[g];
        f[g] ^= f[a];
        f[a] ^= f[g];
    }
    a = g = 0;
    result = "";
    for (var m = 0; m < b["length"]; m++) {
        a = (a + 1) % 234;
        g = (g + f[a]) % 234;
        f[a] ^= f[g];
        f[g] ^= f[a];
        f[a] ^= f[g];
        var n = f[(f[a] + f[g]) % 234];
        var o = l["charCodeAt"](m);
        result = result + String["fromCharCode"](n ^ b["charCodeAt"](m) ^ o);
    }
    return result;
}
 
function proceed(b, l, p) {
    if (p == "dctfizer") {
        cipherText = memoryGood(b, l);
        return goToHex(cipherText);
    } else {
        if (p == "undctfizer") {
            plainText = memoryGood(backFromHex(b), l);
            return plainText;
        }
    }
    return "So what exactly do you want?";
}
```

TODO: write the rest.
