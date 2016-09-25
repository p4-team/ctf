#  Bad OTPxploited (RevCrypt 100)

> Security buzzwords are used by companies and individuals everywhere althought not all of them even follow good practices, some even provide closed source implementations. Someone published his own OTP library on a subreddit and claims it's unbeatable. Is it? 10.13.37.41 

> https://dctf.def.camp/quals-2016/mypam.bin

The binary in the task was a shared library implementing a couple of functions, such as `pam_sm_authenticate`. Googling
it revealed it's `Pluggable authentication module`, used for example as SSH authentication extension. The algorithm was
simple: the user was compared to hardcoded `dctf`, and the password was also constant string concatenated with current date
and time, precise up to minute. After logging in to SSH server running on given IP with found credentials, we received the flag.
