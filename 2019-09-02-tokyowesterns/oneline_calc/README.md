We are presented with [a form](http://olc.chal.ctf.westerns.tokyo):

![`[114+514_______] % 256 [=] [____________]`](screenshot.png)

Pressing `=` puts the result, `116`, into the output field. A quite substantial
delay (> 1 s) suggests that the calculation is performed server-side, which is
confirmed by the [HTML source code](form.html):

```javascript
document.querySelector('#button').addEventListener('click', (e) => {
    const input = document.querySelector('#formula')
    const result = document.querySelector('#result')
    input.disabled = true
    const es = new EventSource(`/calc.php?formula=${encodeURIComponent(input.value)}`);
    es.addEventListener('message', (e) => {
        result.value = e.data
    })
    es.addEventListener('error', (e) => {
        result.value = e.data
        input.disabled = false
    })
    es.addEventListener('close', (e) => {
        es.close()
        input.disabled = false
    })
})
```

An obvious goal emerges: identify how the evaluation is performed. Evaluating
`sleep(2)` seems to take longer than simple numeric expressions and results in 0.
However, `sleep(10)`, with the same result, does not take much longer. Perhaps
0 also means "timeout"?

```
sleep(1)+12 -> 12
sleep(3)+12 -> 0
```

Indeed, this seems to be quite likely. What about automatic coercions?

```
1+"2"   -> 133
1+"17"  -> 133
"2"+"3" -> failed to parse
```

It appears that the value of a string literal does not depend on the characters.
But, what *is* the value? The result is modulo 256, after all. Are right shifts supported?
And why doesn't `"2"+"3"` work?

```
42>>2  -> 10
"2">>8 -> failed to parse
```

It appears that strings aren't always converted to numbers. Are there any explicit casts?

```
1+((int)"2")   -> 133
((int)"2")+"3" -> 10
((int)"2")>>8  -> varies: 91,123,11,203,43,27, ...
```

Okay, what?

```python
$ python
Python 3.7.4 (default, Jul 16 2019, 07:12:58)
[GCC 9.1.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> x=[91,123,11,203,43,27]
>>> list(map(hex, x))
['0x5b', '0x7b', '0xb', '0xcb', '0x2b', '0x1b']
```

It seems like only the low 12 bits is constant. Sounds familiar? At this point,
one might guess that the expression evaluator in question is called "GCC".

```
__cplusplus -> failed to parse
__GNUC__    -> 7
```

Yeah, that would explain things. So, what functions are available?

```
fwrite -> 160
exit   -> 32
system -> 64
malloc -> 112
sqrt   -> failed to parse
```

Can we have multiple expressions?

```
3;4        -> 3
3;return 4 -> 4
3;exit(7)  -> 7
```

Looks like the result is first stored in a variable. Also, the `% 256` could
relate to the limited range of process exit codes. Can we just call `system`, then?

```
system("sleep 1");return 3 -> 0
```

Hmm, that does not sound right. It seems like this kills our process, like the timeout.
So, what are the limitations? Can we open files?

```
fopen("/etc/passwd","r") -> 96
```

Okay, let's leak some files then. Can we write normal programs, with loops and conditions?

```
3;if(1){}; -> invalid char found
```

Uh oh. Can [trigraphs](https://en.wikibooks.org/wiki/C_Programming/C_trigraph)
help?

```
3;if(1)??<??>; -> failed to parse
```

Makes sense, [trigraphs are disabled by default on GCC](https://tio.run/##S9ZNT07@/z8zr0QhNzEzT0PT3t7G3t7u/38A):

```
.code.tio.c:1:11: warning: trigraph ??< ignored, use -trigraphs to enable [-Wtrigraphs]
 int main()??<??>
            
.code.tio.c: In function ‘main’:
.code.tio.c:1:11: error: expected declaration specifiers before ‘?’ token
 int main()??<??>
           ^
.code.tio.c:1:14: warning: trigraph ??> ignored, use -trigraphs to enable [-Wtrigraphs]
 int main()??<??>
```

However, *di*graphs work just fine:

```
3;if(1)<%%>; -> 3
```


