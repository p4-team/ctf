# Wired CSV, misc, 220p

> We have a photo and a CSV file. NOTE: The flag does not follow the CTF{...} format, but is clearly marked as the flag. Please add the CTF{...} around the flag manually when submitting.

The chip on the attached photo was POKEY, which interfaces with keyboard on Atari.
We also got a CSV with logic dumps of several pins, which were D0-D5 and select lines. If we dump state of Dx
at times when the select is on, then we should get raw keyboard codes. We also found a code to character mapping 
somewhere on the internet, which finally allowed us to create `read.py` and get the flag.
