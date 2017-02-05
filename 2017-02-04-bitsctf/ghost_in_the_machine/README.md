# Gh0st in the machine (forensic,60p)

> mY CoMputEr IS ActIng uP. cAn yOu heLP mE?
> Flag format: BITS(WORDS.IN.CAPS)

In this task we were given a pcap containing two minutes worth of keyboard USB capture. Apart from the actual keystrokes
(which turned out to spell link to Rick Roll video...), there were some packets going from the host to the keyboard.
They contained only a single byte, alternating 0x01 and 0x03. As we soon found out, these bits correspond to keyboard state,
and the changing bit meant Caps Lock status. This was consistent with challenge description, which had some problems with
letter case. 

We rememembered a recent article about exfiltration of data using those LEDs and thought this could be used here as well.
so we wrote a quick script (parse3.py), calculating a difference between times the Caps Lock is turned on and off.
They seemed to follow a certain pattern, and we soon thought it could be Morse code. We treated 300ms or longer pulses
as dash and shorter as a dot, and using online morse converter gave us something close enough to flag (we had to guess two 
characters).
