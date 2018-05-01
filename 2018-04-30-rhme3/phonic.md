# Phonic Frenzy 1, Misc, 100pts

> Your car has a brand new infotainment center. In order to activate the system you have to register the serial number on the company's website. The only problem is, it's not trivial to find the dang thing.

When we flashed given binary to the device, it wrote some
story-related, but otherwise useless, text to the console. 
It turns out there were some electric changes happening on
some of the pins. In particular, two of those seemed to be of analog
nature (not just switching between two values). Connecting these pins
to a speaker gave us low quality sound of human speech, eventually
saying the serial number we were after.

Due to the low quality of the sounds, we could not  understand some of 
the letters (`e`, `d` and `b` were almost indistinguishable to us).
Instead, we recorded the sound and used Audacity to visually find
the differences between the letters.