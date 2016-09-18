## Fuzyll (Recon, 200p)

###ENG
[PL](#pl-version)

In the task we start off on page http://fuzyll.com/files/csaw2016/start to get a riddle:

```
CSAW 2016 FUZYLL RECON PART 1 OF ?: People actually liked last year's challenge, so CSAW made me do it again... Same format as last year, new stuff you need to look up. The next part is at /csaw2016/<the form of colorblindness I have>.
```

We could check the author twitter and reddit where he writes a bit about which colors he can't see, or we could brute-force this, either way the answer is `deuteranomaly`, and we get to next level.
We get a [picture](deuteranomaly.png) and if we look inside with hexeditor we can see another riddle:

```
CSAW 2016 FUZYLL RECON PART 2 OF ?: No, strawberries don't look exactly like this, but it's reasonably close. You know what else I can't see well? /csaw2016/&lt;the first defcon finals challenge i ever scored points
```

We check on author blog and other sources to see which defcons should be consider and there brute-force the task name (good thing Fuzyll actually has nice listings on his github for all Defonc challenge names!), and we get the name `tomato`. 

This leads to another [file](tomato.bin) which we guess to be `ebdic` encoded, and from it we extract new riddle:

```
CSAW 2016 FUZYLL RECON PART 3 of ?: I don't even like tomatoes] Anyway, outside of CTFs, I've been playing a fair amount of World of WarCraft over the past year (never thought I'd be saying that after Cataclysm, but here we are). The next part is at /csaw2016/<my main WoW character's name>.
```

Quick googling to find Fuzyll's account on some WoW site and we get the name `elmrik`, and we get some custom-made ruby encryption:

```ruby
#!/usr/bin/env ruby

CHARS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "B", "C", "D",
         "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T",
         "V", "W", "X", "Y", "Z", "b", "c", "d", "f", "g", "h", "j", "k",
         "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]

def encode(string)
    input = string.bytes.inject {|x, y| (x << 8) + y }
    output = ""
    while input > 0
        output = CHARS[input % 52].to_s + output
        input /= 52
    end
    return output
end

def decode(input)
    # your implementation here
end

message = "JQSX2NBDykrDZ1ZHjb0BJt5RWFkcjHnsXvCQ4LL9H7zhRrvVZgLbm2gnXZq71Yr6T14tXNZwR1Dld2Y7M0nJsjgvhWdnhBll5B8w0VP3DFDjd3ZQBlcV4nkcFXBNzdPCSGMXQnQ7FTwcwbkG6RHX7kFHkpvgGDDGJvSDSTx7J6MFhRmTS2pJxZCtys4yw54RtK7nhyW6tnGmMs1f4pW6HzbCS1rSYNBk3PxzW9R1kJK54R2b7syLXd7x1Mr8GkMsg4bs3SGmj3rddVqDf4mTYq1G3yX1Rk9gJbj919Jw42zDtT2Jzz4gN0ZBmXPsBY9ktCLPdFrCPZ33NKJy5m37PK0GLXBxZz9k0cjzyt8x199jMsq7xrvNNgDNvgTbZ0xjZzHhkmrWrCmD7t4q4rWYFSJd4MZBxvnqc0VgGzdkq8jSJjnwcynq9VfH22WCQSdPKw48NkZL7QKGCT94pSb7ZSl2G6W37vBlW38q0hYDVcXTTDwr0l808nDPF6Ct1fPwKdNGKbRZ3Q3lHKMCYBC3w8l9VRjcHwMb1s5sMXM0xBvF8WnWn7JVZgPcXcwM2mDdfVkZsFzkrvVQmPfVNNdk9L5WtwDD8Wp9SDKLZBXY67QkVgW1HQ7PxnbkRdbnQJ4h7KFM2YnGksPvH4PgW2qcvmWcBz62xDT5R6FXJf49LPCKL8MQJLrxJpQb7jfDw0fTd00dX1KNvZsWmfYSTl1GxPlz1PvPSqMTQ036FxSmGb6k42vrzz2X90610Z"
puts decode(message)
```

We first rewrote this code into Python and then prepared decryption code:

```python
message = "JQSX2NBDykrDZ1ZHjb0BJt5RWFkcjHnsXvCQ4LL9H7zhRrvVZgLbm2gnXZq71Yr6T14tXNZwR1Dld2Y7M0nJsjgvhWdnhBll5B8w0VP3DFDjd3ZQBlcV4nkcFXBNzdPCSGMXQnQ7FTwcwbkG6RHX7kFHkpvgGDDGJvSDSTx7J6MFhRmTS2pJxZCtys4yw54RtK7nhyW6tnGmMs1f4pW6HzbCS1rSYNBk3PxzW9R1kJK54R2b7syLXd7x1Mr8GkMsg4bs3SGmj3rddVqDf4mTYq1G3yX1Rk9gJbj919Jw42zDtT2Jzz4gN0ZBmXPsBY9ktCLPdFrCPZ33NKJy5m37PK0GLXBxZz9k0cjzyt8x199jMsq7xrvNNgDNvgTbZ0xjZzHhkmrWrCmD7t4q4rWYFSJd4MZBxvnqc0VgGzdkq8jSJjnwcynq9VfH22WCQSdPKw48NkZL7QKGCT94pSb7ZSl2G6W37vBlW38q0hYDVcXTTDwr0l808nDPF6Ct1fPwKdNGKbRZ3Q3lHKMCYBC3w8l9VRjcHwMb1s5sMXM0xBvF8WnWn7JVZgPcXcwM2mDdfVkZsFzkrvVQmPfVNNdk9L5WtwDD8Wp9SDKLZBXY67QkVgW1HQ7PxnbkRdbnQJ4h7KFM2YnGksPvH4PgW2qcvmWcBz62xDT5R6FXJf49LPCKL8MQJLrxJpQb7jfDw0fTd00dX1KNvZsWmfYSTl1GxPlz1PvPSqMTQ036FxSmGb6k42vrzz2X90610Z"
CHARS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "B", "C", "D",
         "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T",
         "V", "W", "X", "Y", "Z", "b", "c", "d", "f", "g", "h", "j", "k",
         "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]


def encrypt(input_data):
    orded = [ord(c) for c in input_data]
    print(orded)
    number = reduce(lambda x, y: (x << 8) + y, orded)
    output = ""
    while number > 0:
        output = CHARS[number % 52] + output
        number /= 52
    return output


def decrypt(input_data):
    number = 0
    for c in input_data:
        number *= 52
        number_mod = CHARS.index(c)
        number += number_mod
    initial = []
    while number > 127:
        y = number & 127
        print(y)
        initial.insert(0, y)
        number -= y
        number >>= 8
    initial.insert(0, number)
    return "".join([chr(c) for c in initial])


print(decrypt(message))
```

As a result we get:

```
CSAW 2016 FUZYLL RECON PART 4 OF ?: In addition to WoW raiding, I've also been playing a bunch of Smash Bros. This year, I competed in my first major tournament! I got wrecked in every event I competed in, but I still had fun being in the crowd. This tournament in particular had a number of upsets (including Ally being knocked into losers of my Smash 4 pool). On stream, after one of these big upsets in Smash 4, you can see me in the crowd with a shirt displaying my main character! The next part is at /csaw2016/<the winning player's tag>.
```

This was by far the hardest part!
Since we were too lazy to watch some random streams, we used a brute-force approach.
First we pinpointed a tournaments where Ally went into losers and then we checked if Fuzyll was on players list.
This lead to CEO 2016 tournament.
Then we simply scrapped all players form the tournament webpage and wrote a script to brute-force check all 1000 player names.
It turned out to be `jade` so we got the next [file](jade.jpg) with a riddle.
We extract the riddle agian with hexeditor:

```
CSAW 2016 FUZYLL RECON PART 5 OF 6: I haven't spent the entire year playing video games, though. This past March, I spent time completely away from computers in Peru. This shot is from one of the more memorable stops along my hike to Machu Picchu. To make things easier on you, use only ASCII: /csaw2016/<the name of these ruins>
```

A bit of googling and reverse image search gives us the name `Winay Wayna` and the page gives us the flag: `flag{WH4T_4_L0NG_4ND_STR4NG3_TRIP_IT_H45_B33N}`

###PL version

Zadanie zaczynamy na stronie http://fuzyll.com/files/csaw2016/start żeby dostać zagadkę:

```
CSAW 2016 FUZYLL RECON PART 1 OF ?: People actually liked last year's challenge, so CSAW made me do it again... Same format as last year, new stuff you need to look up. The next part is at /csaw2016/<the form of colorblindness I have>.
```

Można poczytać twittera autora oraz jego komentarze na reddicie gdzie wspomina o tym których kolorów nie widzi, lub zwyczajnie tesutjemy wszystkie możliwości, tak czy siak odpowiedź to `deuteranomaly` i rozpoczynami kolejny poziom.
Dostajemy [obrazek](deuteranomaly.png) i jeśli popatrzymy do środka hexedytorem widzimy nową zagadkę:

```
CSAW 2016 FUZYLL RECON PART 2 OF ?: No, strawberries don't look exactly like this, but it's reasonably close. You know what else I can't see well? /csaw2016/&lt;the first defcon finals challenge i ever scored points
```

Po sprawdzeniu bloga autora i kilku innych źródeł wiemy które defcony można brać pod uwagę a następnie za pomocą brute-force testujemy nazwy zadań (Fuzyll na swoim githubie ma listę wszystkich defonowych zadań!) i dostajemy odpowiedź `tomato`.

To prowadzi do kolejnego [pliku](tomato.bin) o którym zgadujemy że jest kodowany jako `ebdic` i wyciągamy z niego nową zagadke:

```
CSAW 2016 FUZYLL RECON PART 3 of ?: I don't even like tomatoes] Anyway, outside of CTFs, I've been playing a fair amount of World of WarCraft over the past year (never thought I'd be saying that after Cataclysm, but here we are). The next part is at /csaw2016/<my main WoW character's name>.
```

Szybki rzut oka w google szukając konta Fuzyll na stronach dotyczących WoWa i dostajemy nazę `elmrik` i dostajemy zaszyfrowaną zagadkę:

```ruby
#!/usr/bin/env ruby

CHARS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "B", "C", "D",
         "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T",
         "V", "W", "X", "Y", "Z", "b", "c", "d", "f", "g", "h", "j", "k",
         "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]

def encode(string)
    input = string.bytes.inject {|x, y| (x << 8) + y }
    output = ""
    while input > 0
        output = CHARS[input % 52].to_s + output
        input /= 52
    end
    return output
end

def decode(input)
    # your implementation here
end

message = "JQSX2NBDykrDZ1ZHjb0BJt5RWFkcjHnsXvCQ4LL9H7zhRrvVZgLbm2gnXZq71Yr6T14tXNZwR1Dld2Y7M0nJsjgvhWdnhBll5B8w0VP3DFDjd3ZQBlcV4nkcFXBNzdPCSGMXQnQ7FTwcwbkG6RHX7kFHkpvgGDDGJvSDSTx7J6MFhRmTS2pJxZCtys4yw54RtK7nhyW6tnGmMs1f4pW6HzbCS1rSYNBk3PxzW9R1kJK54R2b7syLXd7x1Mr8GkMsg4bs3SGmj3rddVqDf4mTYq1G3yX1Rk9gJbj919Jw42zDtT2Jzz4gN0ZBmXPsBY9ktCLPdFrCPZ33NKJy5m37PK0GLXBxZz9k0cjzyt8x199jMsq7xrvNNgDNvgTbZ0xjZzHhkmrWrCmD7t4q4rWYFSJd4MZBxvnqc0VgGzdkq8jSJjnwcynq9VfH22WCQSdPKw48NkZL7QKGCT94pSb7ZSl2G6W37vBlW38q0hYDVcXTTDwr0l808nDPF6Ct1fPwKdNGKbRZ3Q3lHKMCYBC3w8l9VRjcHwMb1s5sMXM0xBvF8WnWn7JVZgPcXcwM2mDdfVkZsFzkrvVQmPfVNNdk9L5WtwDD8Wp9SDKLZBXY67QkVgW1HQ7PxnbkRdbnQJ4h7KFM2YnGksPvH4PgW2qcvmWcBz62xDT5R6FXJf49LPCKL8MQJLrxJpQb7jfDw0fTd00dX1KNvZsWmfYSTl1GxPlz1PvPSqMTQ036FxSmGb6k42vrzz2X90610Z"
puts decode(message)
```

Najpierw przepisalismy kod do pythona a następnie przygotowaliśmy kod deszyfrujący:

```python
message = "JQSX2NBDykrDZ1ZHjb0BJt5RWFkcjHnsXvCQ4LL9H7zhRrvVZgLbm2gnXZq71Yr6T14tXNZwR1Dld2Y7M0nJsjgvhWdnhBll5B8w0VP3DFDjd3ZQBlcV4nkcFXBNzdPCSGMXQnQ7FTwcwbkG6RHX7kFHkpvgGDDGJvSDSTx7J6MFhRmTS2pJxZCtys4yw54RtK7nhyW6tnGmMs1f4pW6HzbCS1rSYNBk3PxzW9R1kJK54R2b7syLXd7x1Mr8GkMsg4bs3SGmj3rddVqDf4mTYq1G3yX1Rk9gJbj919Jw42zDtT2Jzz4gN0ZBmXPsBY9ktCLPdFrCPZ33NKJy5m37PK0GLXBxZz9k0cjzyt8x199jMsq7xrvNNgDNvgTbZ0xjZzHhkmrWrCmD7t4q4rWYFSJd4MZBxvnqc0VgGzdkq8jSJjnwcynq9VfH22WCQSdPKw48NkZL7QKGCT94pSb7ZSl2G6W37vBlW38q0hYDVcXTTDwr0l808nDPF6Ct1fPwKdNGKbRZ3Q3lHKMCYBC3w8l9VRjcHwMb1s5sMXM0xBvF8WnWn7JVZgPcXcwM2mDdfVkZsFzkrvVQmPfVNNdk9L5WtwDD8Wp9SDKLZBXY67QkVgW1HQ7PxnbkRdbnQJ4h7KFM2YnGksPvH4PgW2qcvmWcBz62xDT5R6FXJf49LPCKL8MQJLrxJpQb7jfDw0fTd00dX1KNvZsWmfYSTl1GxPlz1PvPSqMTQ036FxSmGb6k42vrzz2X90610Z"
CHARS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "B", "C", "D",
         "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T",
         "V", "W", "X", "Y", "Z", "b", "c", "d", "f", "g", "h", "j", "k",
         "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]


def encrypt(input_data):
    orded = [ord(c) for c in input_data]
    print(orded)
    number = reduce(lambda x, y: (x << 8) + y, orded)
    output = ""
    while number > 0:
        output = CHARS[number % 52] + output
        number /= 52
    return output


def decrypt(input_data):
    number = 0
    for c in input_data:
        number *= 52
        number_mod = CHARS.index(c)
        number += number_mod
    initial = []
    while number > 127:
        y = number & 127
        print(y)
        initial.insert(0, y)
        number -= y
        number >>= 8
    initial.insert(0, number)
    return "".join([chr(c) for c in initial])


print(decrypt(message))
```

W wyniku dostajemy:

```
CSAW 2016 FUZYLL RECON PART 4 OF ?: In addition to WoW raiding, I've also been playing a bunch of Smash Bros. This year, I competed in my first major tournament! I got wrecked in every event I competed in, but I still had fun being in the crowd. This tournament in particular had a number of upsets (including Ally being knocked into losers of my Smash 4 pool). On stream, after one of these big upsets in Smash 4, you can see me in the crowd with a shirt displaying my main character! The next part is at /csaw2016/<the winning player's tag>.
```

To była najtrudniejsza część!
Jesteśmy zbyt leniwi żeby oglądać jakieś streamy, więc stosujemy podejście brute-force.
Najpierw odszukaliśmy tegoroczne zawody gdzie Ally wypadł do drabinki przegranych a potem sprawdziliśmy gdzie grał Fuzyll.
W ten sposób trafilismy na CEO 2016.
Następnie po prostu pobraliśmy listę wszystkich graczy ze strony zawodów i napisaliśmy skrypt który sprawdził każdego z 1000 graczy.
Graczem okazał sie `jade` a my dostaliśmy nowy [plik](jade.jpg) z zagadką.
Zagadkę wyciągamy znów hexedytorem:

```
CSAW 2016 FUZYLL RECON PART 5 OF 6: I haven't spent the entire year playing video games, though. This past March, I spent time completely away from computers in Peru. This shot is from one of the more memorable stops along my hike to Machu Picchu. To make things easier on you, use only ASCII: /csaw2016/<the name of these ruins>
```

Chwila googlowania i reverse image search daje name nazwe `Winay Wayna` a strona daje flagę: `flag{WH4T_4_L0NG_4ND_STR4NG3_TRIP_IT_H45_B33N}`
