# Battleships (reverse, ppc, 872p)

> A perfect candidate should be a strong leader, excellent negotiator and outstanding commander. Among his qualities must be strategic thinking and battle skills.Campaign office reports that large naval exercise will take place in the neighbouring city where anyone could try himself as an admiral and fight against famous admiral Odin.This naval exercise is a perfect chance to show the superiority of our candidate over the others. We must make provision for the victory of the leader who would lead our nation to a better future. However, your team had to face unexpected difficulties – your vessels look like they are from Middle Ages while the vessels of your enemy are state-of-the-art fire ships that DESTROYS EVERYTHING AROUND. After this, it is not a surprise that the radar in your command center is not working partially and targeting system is messed up. And what is more – you suspect that your team’s first assistance is Odin’s spy…
> All the indications are that this exercise is organized by your rivals in order to tar your candidate’s reputation. Cheer up! Victory in such an uphill battle will show the strength and genius of your candidate – go for it!

> battleships

> nc 82.202.212.28:1337

In this task we were given a binary, which turns out to be a command line client for playing battleships
game with a server (hardcoded in the binary to localhost, but we patched it to use supplied IP).

The game is pretty normal: first you set your ships' positions on a 10x10 board (4 single-tile ones, 3 double, 2 triple
and 1 four-tile vessel). Then, after completing a simple proof of work, the game starts and you can guess where
computer's ships are.

After writing a simple Python script intrerfacing with the binary, using simple strategies (guessing randomly or 
sequentially, i.e. a1, a2, a3...), we found out the server has only single-tiled ships - or at least we didn't
sink any bigger ones in dozens of games. Still, it didn't seem we could win the game just like that, it would be too simple.

After disassembling and reverse engineering the binary, we found out the client communicates with the server using
custom protocol. All messages are encrypted using RC4, but we know the key as it's sent in plaintext on the wire.
Apart from the encryption part, the protocol is quite simple - you can send position which you want to target as
byte `x*16+y` and server responds with hit or miss and other, less relevant data. We implemented the protocol in
Python and played a lot more of games. After collecting a nice statistical sample of hundreds of games, we noticed two
patterns in hit positions.

First, enemy ships never touched each other, even though our ships were allowed to be placed in that way. In the 
hindsight, this was hinted in the task description (that enemy vessels destroy everything around). We implemented that
improvement in the code (so that we never try to shoot near sunk ships), but this still wasn't enough to win the game.

The second observation we made was that all the ships we sunk were in the left 7 columns of the board. Although we
often shot the rightmost columns too, they never resulted in successful hit. After reading the description again,
we deduced this might be because of `our targeting system being messed up`. In other words, our board view was stretched
in the X direction. If that was the case, maybe the Y axis was stretched too? Indeed, when we allowed our script
to shoot on Y=11, there were some hits.

In the end, we changed the board size to 7x14 (notice `7*14 == 98`, remarkably close to 100), which allowed us to
win the game after a couple of tries.
