# CAN opener, CAN, 150pts

> Our operatives have recovered a DeLorean in the ruins of an old mid-west US town. It appears to be locked, but we have successfully accessed its internal communications channels. According to the little data we have, the DeLorean internally uses an archaic technology called CAN bus. We need you to analyze the communications and find a way to unlock the vehicle; once unlocked, recover the secret flag stored inside. We have reason to believe that vehicle entry should be a fairly easy challenge, but to aid you in this, we have restored and reconnected the vehicle dashboard.

> Best of luck.

> The Dashboard app is available here.

> Challenge developed by Argus Cyber Security.

This was first of the challenges related to CAN bus. The board we got
has two CAN controllers, connected to each other, allowing the AVR
chip to talk to itself (in a loopback mode, so to say). Apparently
it was sending messages through one interface to the other, to simulate
full, car-wide CAN bus. Connecting
logic analyzer to the CAN bus we could sniff the sent messages. 

One of those was particularly interesting - `lock\x00\x00\x00\x00`.
We could only think that the opposite of it would be `unlock\x00\x00`...
At this point of time, I had no CAN hardware, but I had... Arduino.
So I wrote a software implementation of CAN bus:
https://gist.github.com/akrasuski1/b1904966c4de0b50672e6fc1fd116d3e
It's not very efficient, does absolutely no error-checking, and the
code quality is quite poor, but it was enough to send the unlock message.
After the board received it, it sent the flag through UART interface to the
dashboard.