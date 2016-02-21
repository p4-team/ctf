## A numbers game II (PPC, 70p)

	Description: Math is used in cryptography, but someone got this wrong. Can you still solve the equations? 
	Hint: You need to encode your answers. 
	
	This snippet may help:

```python
    def encode(self, eq):
        out = []
        for c in eq:
            q = bin(self._xor(ord(c),(2<<4))).lstrip("0b")
            q = "0" * ((2<<2)-len(q)) + q
            out.append(q)
        b = ''.join(out)
        pr = []
        for x in range(0,len(b),2):
            c = chr(int(b[x:x+2],2)+51)
            pr.append(c)
        s = '.'.join(pr)
        return s
```
	
###ENG
[PL](#pl-version)

###PL version

