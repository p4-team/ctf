# Combo 100 (forensics/osint/re, 100p, ? solved)

W very long multi-stage challenge, no idea what it was worth only 100p.
In the challenge we get a 267MB pcap file, so we won't be attaching it.

The most indispensible tool to work with pcaps of this size of NetworkMiner.
It automatically extracts files, parameters, passwords, messages etc.

In the task description there is a mention os some email exchange so we first look at emails extracted from pcap.
It turns out those emails are driving the whole challenge from start to the finish.

```
Hi James,

Hey! It's been a while! By the way, remember the fishing trip we went to 
last month, I took some pictures.
Here take a look, I attached one.

Regards,
Bond 
```

```
Hi Bond,

Nice picture! Better remember the EXACT place where that picture was taken. 
You may want to check the lodging we took when we went there. I left a very
important note for that thing we've discussed from our fishing trip... which
I also attached.

Regards,
James
```

To one of the emails there is  a [picture](Fishing_Trip.jpg) attached.
The email mentions to look `exactly` where the picture was taken, so we extract EXIF data and it turns out the picture contains coordinates.
This leads us to: https://www.google.com/maps/place/GiethoornTMCTF/@52.7203254,6.0898781,17z/data=!3m1!4b1!4m5!3m4!1s0x47c86f063fec1ef9:0x8d76ad68f8a4424d!8m2!3d52.7203254!4d6.0920668

And there is a marker for `GiethoornTMCTF`, which seems like a clue.
The other email contained an [encrypted zip](flag-encrypted.zip).
We can decrypt this zip using `GiethoornTMCTF` as password and we get a [strange file](flag-encrypted.txt).

We tried to do some analysis of this file, and since charset size is 16 we assumed this might be some substitution cipher over hexencoded bytes, but we were unable to do anything with it.

We follow the trail of emails:

```
Hi James,

Got the note. Was it supposed to be a gift? Now, I need to know how to make 
this thing work.
For that, I have to know where to find you, could you give me some 
directions?

Regards,
Bond
```

```
Hi Bond,

Sure thing. Let's meet then, but I am traveling across Europe man... a
Europe Tour!! 
First, I visited NORWAY, you need to stop by there too, the place is so
great! 
After seeing the sights there, I remembered that I needed to drop some
things in LATVIA, but in order to go there, I need to cut across SWEDEN to
get there quicker.
That is very important because you will only see the direction to LATVIA if
you go right in the MIDDLE of SWEDEN.
After that, I have to travel all the way to BELARUS, I left my keys there.
Or maybe I can just ask FRANCE to fetch it for me so we can go meet in
LITHUANIA much earlier.

Regards,
James
```

Now this part was a bit confusing, because we initially thought they meant actual locations on the map, and we tried to draw something.
In the end we first solved the next part before getting back here with better understanding of what we're looking for, but we're describe the solution in proper order.

The idea here is to notice in the files downloaded by the user an article [Norway.html](Norway.html) downloaded from `weakipedia`.
It seems legit apart from strange parts:

```
<!--SwedenQvz aGJNNXndZapTBYRLCpKQGdpJWNw:aGJNNXndZapTBYRLCpKQGdpJWNw="xlmAZJMejaLkGsMznIss":Vs aGJNNXndZapTBYRLCpKQGdpJWNw="xlmAZJMejaLkGsMznIss"Gura:Raq Vs:Qvz PETahTHZHUFjwEzDRNSweden-->
```

And the emails says `cut across SWEDEN` and `MIDDLE of SWEDEN`.
We guessed the idea is to extract the data inside so we proceed with:

```python
def main():
    data = open("Norway.html").read()
    print("".join(data.split("Sweden")[1::2]).decode("rot13").replace(":","\n"))


main()
```

Now it would be pretty confusing, but from solving later AMERICA and AFRICA steps, we already knew that we're looking for obfuscated VBS code where `:` denote newlines.

This way we extract [obfuscated stage1](stage1ob.vbs).
This code is `obfuscated` by lots of useless instructions:

```vbscript
nTWAAKaqMncGOLEYPcXDTqcWJAj="kyzNMWZrwnYxTfZmaVff"
If nTWAAKaqMncGOLEYPcXDTqcWJAj="kyzNMWZrwnYxTfZmaVff"Then
End If
```

Such instruction does nothing so we can remove all of them.
Finally we get [stage1.vbs](stage1.vbs) and combined with the inputs we got from zip we get [results of stage1](resultstage1.txt).
Interestingly enough antivirus and windows defender get triggered by stage1 script after we remove the obfuscation.

Now we follow the emails trail to figure out what to do with this:

```
Hi Bond,

Just a reminder about what we've talked about. You have to visit NICARAGUA
to get that certificate I hid, then head back to USA. 
That document is very important as you needed for your entry in COLOMBIA. 
Well, you can visit other countries too with that certificate, like
VENEZUELA, ARGENTINA, BRAZIL, even CANADA, and many more.
Seems like you'll be having your own tour, an Americas Tour!

Regards,
James
```

This email mentions some `certificate` and `NICARAGUA` so we dive again in NetworkMiner and we find [a certificate](hidden.cer.html).
However when you try to decode it, it doesn't seem to be valid certificate at all.
It turns out its just base64 payload, which decoded gives us [stage 2](stage2.vbs).

Notice here that this was the first VBS code we found, because this one was only base64 encoded and easy to spot.
Only after that we managed to find the EUROPE one.

When we combine the code with data we got from stage 1 we get [results of stage 2](resultstage2.txt) which again looks like encoded data.

Let's follow the emails:

```
Hi James,

Americas tour is a blast! But I feel like the experience ain't complete yet. 
Am I missing something. Is there anything else I need to know? or perhaps, 
need to visit?
Maybe an African Tour wouldn't be a bad idea?

Regards,
Bond
```

```
Hi Bond,

Good thing you mention it! We really need to visit Africa, I'm querying some
travel blogs, looking for good sights, I must say pyramid of Giza in EGYPT
might be a good spot to start, or maybe SUDAN?
Oh, did you know that SUDAN has more pyramid than EGYPT? Isn't it crazy?
While we're on it, we can visit some neighboring countries along the
Mediterranean such as LIBYA, TUNISIA, ALGERIA up to MOROCCO.

Regards,
James
```

This exchange hints about `querying some
travel blogs`, `pyramids`, `Egypt` and `Sudan` so again we check in NetworkMiner if there is anything interesting.
And we find interesting GET parameters:

```
/pyramids/images/giza.jpg?query=ctf&sudan=VFVOSVNJQSUzRCUyMnN0cmluZyUyMiUzQVRVTklTSUElM0RyZVBMQUNlJTI4VFVOSVNJQSUyQyUyMi0lMjIlMkMlMjIwJTIyJTI5JTNBVFVOSVNJQSUzRHJlUExBQ2UlMjhUVU5JU0lBJTJDJTIyJTIzJTIyJTJDJTIyMSUyMiUyOSUzQVRVTklTSUElM0RyZVBMQUNlJTI4VFVOSVNJQSUyQyUyMiU3QiUyMiUyQyUyMjIlMjIlMjklM0FUVU5JU0lBJTNEcmVQTEFDZSUyOFRVTklTSUElMkMlMjIlNUQlMjIlMkMlMjIzJTIyJTI5JTNBVFVOSVNJQSUzRHJlUExBQ2UlMjhUVU5JU0lBJTJDJTIyJTJBJTIyJTJDJTIyNCUyMiUyOSUzQVRVTklTSUElM0RyZVBMQUNlJTI4VFVOSVNJQSUyQyUyMiU1QiUyMiUyQyUyMjUlMjIlMjklM0FUVU5JU0lBJTNEcmVQTEFDZSUyOFRVTklTSUElMkMlMjIlN0MlMjIlMkMlMjI2JTIyJTI5JTNBVFVOSVNJQSUzRHJlUExBQ2UlMjhUVU5JU0lBJTJDJTIyJTNEJTIyJTJDJTIyNyUyMiUyOSUzQVRVTklTSUElM0RyZVBMQUNlJTI4VFVOSVNJQSUyQyUyMiUyRiUyMiUyQyUyMjglMjIlMjklM0FUVU5JU0lBJTNEcmVQTEFDZSUyOFRVTklTSUElMkMlMjIlNUMlMjIlMkMlMjI5JTIyJTI5JTNBVFVOSVNJQSUzRFNwTGlUJTI4VFVOSVNJQSUyQyUyMiUyMSUyMiUyOSUzQUZPUiUyMEFMR0VSSUUlM0QxJTIwVE8lMjBVYm9VbkQlMjhUVU5JU0lBJTI5JTNBTU9ST0NDTyUzRE1PUk9DQ08lMkJjSHIlMjhUVU5JU0lBJTI4QUxHRVJJRSUyOSUyRiUyODI1JTJCMjUtMzIlMjklMjklM0FORVhU
```

Decoding this via:

```python
print(urllib.unquote(param.decode("base64")).replace(":", "\n"))
```

Gives us [stage3](stage3.vbs) script, which combined with the results from previous stage provide [stage 3 results](resultstage3.txt).
Which actually contains a flag!
Well at least ascii-art flag (but also true flag in fact).

Again we follow the emails:

```
Hi James,

I have an idea for our nexxt tour... Asian tour is it.
I feel like we shouldd go to these places, since we visitd pyramid in 
EgHypt, let's visit other wonders in Asia too.
So, TYhe Great Wall of China and Taj Mahal in India is a must in ths tour.
Then if it''s Okkay with you, from China we move to HongKKong, then Japan, 
lots of beautifull and historical places...
Then we go doWwn t Vietnam, nexXt is Cambodia, then Lao0s,. and Thailancd.
Oh I want to see the Petronas twin towWer in MalayYsia, then we move 
straight to Singapore, so much choices here as well.
I want to viist Bali, Indoonesia too. Oww, Philippines is a must see, there 
are tons oOf nice places.
MNaybe there are too much I want to see, can:'t be help, Asia has lots of 
sights to offer;, well, if it's too repetitive, I can remove one or two from 
the lsit.
Perhaps five itineraries would be enough.
I'm so excited for our next tour.

Regards,
Bond 
```

```
Hi James,

Sorry for my last mail, I'm in a car earlier and road is kinda rough...
I'm so excited to share you my thoughts and I just can't wait to have a good 
place to write mail, hence, some typos here and there.
I know it ain't necessary but I fix them below.

Regards,
Bond
----- Original Message ----- 
From: "Bond Paper" <bond_paper@tmctf.com>
To: "Coco James" <coco_james@tmctf.com>
Sent: Friday, August 16, 2019 5:53 AM
Subject: Re: Hello World!


Hi James,

I have an idea for our next tour... Asian tour is it.
I feel like we should go to these places, since we visited pyramid in Egypt, 
let's visit other wonders in Asia too.
So, The Great Wall of China and Taj Mahal in India is a must in this tour.
Then if it's okay with you, from China we move to HongKong, then Japan, lots 
of beautiful and historical places...
Then we go down to Vietnam, next is Cambodia, then Laos, and Thailand.
Oh I want to see the Petronas twin tower in Malaysia, then we move straight 
to Singapore, so much choices here as well.
I want to visit Bali, Indonesia too. Oww, Philippines is a must see, there 
are tons of nice places.
Maybe there are too much I want to see, can't be help, Asia has lots of 
sights to offer, well, if it's too repetitive, I can remove one or two from 
the list.
Perhaps five itineraries would be enough.
I'm so excited for our next tour.

 Regards,
Bond
```

This step was quite clear, and we wouldn't really need the email hint for that.
The ascii-art flag has very limited charset:

```
Counter({'\x00': 25752, 'H': 12884, '.': 4214, "'": 2008, ';': 1916, ',': 1201, 'Y': 666, 'N': 483, 'X': 481, 'K': 388, '0': 291, '\n': 232, 'O': 160, 'x': 131, 'W': 129, 'o': 117, 'k': 115, 'd': 108, 'c': 72, 'l': 65, ':': 62, 'T': 3, '!': 3, 'y': 3, 'e': 3, 'G': 2, 'a': 2, 'r': 2, 'A': 1, 'Z': 1, 'm': 1, 'ţ': 1, 'F': 1, 'n': 1, 'V': 1, '}': 1, 'M': 1, '˙': 1, '{': 1, 'C': 1, 'i': 1})
```

So it's quite clear that there are very common characters and characters which appear only a handful of times in the whole picture.
From the misspells in the email we can get the list of characters we need to remove, and the coincide with the most common characters in the file.
For some reason the misspells contained some of the actual flag characters, and picture contained something like `ţ`, so we just stuck to removing all most common chars and leaving only reasonable charset:

```python
def main():
    data = open("resultstage3.txt").read()
    c = collections.Counter(data)
    print(c)
    for char, score in c.items():
        if score > 50:
            data = data.replace(char, "")
    print("".join([c for c in data if c in string.ascii_letters + string.digits + '{}_-!']))

main()
```

Once we remove those characters we finally get: `TMCTF{yey!AmaZinG!VeryGreaT!}`
