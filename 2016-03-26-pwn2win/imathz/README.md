## iMathze (PPC)
In this chall we must connect through ssh to the game and solve 3 mazes and 9 equations (3 for each maze). 

At first we tried writing a python script to connect, parse the input and send solution, but the game was drawn in a terminal using escape sequences. It would be troublesome to parse them, so we took different approach. We wrote a program to find a path in the maze and just quickly press arrow keys to navigate in the maze (we even had an old code snippet somewhere to do such things). The input was copy-pasted from terminal (it was fast enough even for the 20s limit).

Unfortunately, due to a bug in the program (literally pressing one arrow key more than necessary) we couldn't obtain the flag ;(. After a lot of thinking we found it just in the moment the ctf has ended. 
