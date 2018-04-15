# Hashcash - Pwn (150 + 0), 13 solves

> Shall we play a game? We need help beta testing our fancy new cryptocurrency themed lottery game. There may just be a bounty in it for you if you can pwn it.

In this task we were given a binary and `host:port` of the server. We actually solved the task withouth the binary, 
in a blackbox, probably unintended, way.

Basic communication with the server was that it was sending us one byte nonce and difficulty level, then
we have to send input such that `md5(nonce | input)` starts with n leading zero bytes. The difficulty 
rises with level, from just one byte needed, all the way up to 8, thus requiring `2^64` md5 evaluations. This
is much too much, so we had to find another way.

A quick googling on the subject showed us this website: http://0xf.kr/md5/. It keeps track of the smallest
md5 outputs ever generated, and it looks like the record has exactly 8 zeros at the start. If there was
no nonce specified, we would be able to use that preimage. But since the nonce is just one byte, we can
just wait for the server to generate one that is the first byte of our found input. Then we just send the rest,
and we're done.
