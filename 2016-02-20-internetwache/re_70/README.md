## ServerfARM (RE, 70p)

	Description: Someone handed me this and told me that to pass the exam, I have to
	extract a secret string. I know cheating is bad, but once does not count. So are
	you willing to help me?

###ENG
[PL](#pl-version)

After reversing the provided ARM binary, we quickly find some print statements printing
hardcoded characters and short strings, such as `printf("%s%c", "IW",'{')`. Gathering all
of them, we quickly get the password.

###PL version

Spojrzawszy na zdeasemblowany kod ARMowej binarki, zauważamy miejsce, w którym następuje
wypisywanie flagi. Skłąda się ona z kilku/kilkunastu wypisań znaków i krótkich stringów, jak
`printf("%s%c", "IW",'{')`. Po zebraniu wszystkich z nich, dostajemy flagę.
