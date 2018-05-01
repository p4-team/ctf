# Car Crash, RE, 500pts

> This ECU firmware dump, or what's left of it, was taken out of a crashed prototype car. We have to extract the logs from it to investigate the crash. Bad luck, we get some strange garbage printed instead.

> Attached is a program you can reverse-engineer and a program you can test. Don't mix them up.

Long story short, it turned out to be broken implementation of
https://en.wikipedia.org/wiki/Kuznyechik. The only changes were
that the S-box was modified, and the reverse S-box was corrupted.
After calculating the reverse S-box from forward one, we were able to 
calculate the flag.