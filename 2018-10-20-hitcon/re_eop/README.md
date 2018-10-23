# EOP, re

This task was a reverse engineering challenge with binary using exceptions as control flow (post
factum we noticed name of the task may mean Exception Oriented Programming). Each exception
handler did just a tiny bit of computation on global state and set up another exception to be thrown.
Thankfully, there were no branches, just linear code. We wrote a simple IDA code parser in Python
to dump computation instructions in correct order. The remaining code seemed to be some kind of
encryption - we Googled the constants and found Twofish. Gathering sample code from the Internet
and decrypting constant buffer with constant key (both directly in binary), we got the flag.
