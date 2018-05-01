# Climate Controller Catastrophe, Exp, 750pts

> Catting cars is a major issue these days. It's impossible to sell your stolen car as a whole, so you sell it in parts. Dashboard computers are popular since they break quite often ;-).

> Unfortunately, the dashboard computer is paired with the main computer. So, simply exchanging it will not do the trick. In fact, without the handshake to the main computer it will not operate the climate control buttons.

> Of course just pairing the dashboard computer isn't cool enough, try to smash the stack instead! We suspect the device isn't using the serial interface for its pairing algorithm.

> In addition to the attached challenge and reversing binaries, you're provided a special "challenge" which you can flash to wipe the EEPROM of your dashboard computer.

This was a long challenge. Most of the communication with the board
had to be made via a custom CAN protocol, not UART. Some of the 
messages required "authentication", which after closer look was
implemented as challenge-response based on RSA. The binary had
the public key hardcoded, but it was only 32-bit long, so trivially 
factorizable. Using Arduino and MCP2515, we implemented the
authentication scheme.

Being authenticated, we had access to some useful commands,
one of which erased part of EEPROM. Using patched `simavr`, we 
implemented exploit, which overwrote one of return addresses
via heap and stack collision. The vulnerable function was multiplication
of two bigints during processing of sent certificate (using CAN id 0x776).

Final exploit is in `climate/ardu.cpp`, to be flashed on Arduino. The
whole folder also contains some notes from reverse engineering,
along with code for generating the exploit and `simavr` patches.