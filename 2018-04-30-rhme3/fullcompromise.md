# Full compromise, RE, 250pts

> An attacker managed to hack our CI server and sign+encrypt his malicious code in a ECU firmware, that is now running in millions of cars and doing Chaos knows what. To stop the attackers, we must know what the malicious code is doing. We have a history of all binaries signed by the server on the day of the hack, and a device running the attacker's firmware. Help us find which sample was provided by the attacker and get access to its management interface.


In this task, we got 1000 samples of unencrypted binaries, and one
encrypted to be flashed on the chip. We did not know which one of
these 1000 is the correct one. After reversing their code, we noticed
that the password check takes very long time (hours), so we cannot
just brute force our way and check all 1000 passwords.

Instead, we noticed there's a debug mode in the program, which
outputs some analog data to chip's DAC. Each of the 1000 samples 
has somewhat different pattern.

We dumped the pattern from our chip using logic analyzer, and
simulated each of the 1000 known ones using `simavr`. One of them
matched ours. Typing its password to the chip's UART, we got the flag.