# rms, Web / Pwning, 365
> Difficulty: medium (13 solvers)
>
> I generally do not connect to web sites from my own machine, aside from a few sites I have some special relationship with. I usually fetch web pages from other sites by sending mail to a program that fetches them, much like wget, and then mails them back to me.
> ~ Richard Stallman
>
> Flag is at http://127.0.0.1:8000/flag

In this task we are given a binary and IP running this service. When connected, we can
ask it to connect to any HTTP domain and port, and get the response - localhost, where flag is hosted,
is filtered
though. 

The binary uses `gethostbyname2` function to resolve domains, which is not thread safe - and the
app uses multiple threads to queue the requests. The app also supports IPv6 and IPv4, which allows
us to exploit the race condition more easily:
* Thread 1: request http://foo.com:8000/flag, wait for it to connect through IPv6
* Thread 2: request http://localhost:8000/flag, and fail
* Thread 1: IPv6 times out or does not connect, connects to IPv4 which is overwritten
  by thread 1 to point to localhost. 
  
