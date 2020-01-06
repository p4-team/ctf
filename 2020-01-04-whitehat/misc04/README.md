# misc 04

We're given a huge binary file `kevin_mitnick.raw`. Let's see what we can find out.
```
$ file kevin_mitnick.raw 
kevin_mitnick.raw: data
$ ls -lah kevin_mitnick.raw 
-rw-r--r-- 1 chivay chivay 2.0G Jan  4 18:21 kevin_mitnick.raw
```
Well, nothing interesting. Could be a disk image or a VM memory dump.
Time for the almighty `strings` (don't forget to try `strings -el`!).

Trying different lengths and encodings suggests that we're dealing with a Windows memory dump. But which version?

```
$ strings kevin_mitnick.raw -n 10| grep -i "windows 10"
Windows 10
Windows 10 Pro 6.3
      <!-- Windows 10 -->
Windows 10, 64-bit  (Build 10240)
[...]
```
Ok, time for `volatility`.

And since we're lazy:
```
export VOLATILITY_PROFILE=Win10x64_10240_17770
export VOLATILITY_LOCATION=file://kevin_mitnick.raw
```

Let's see what's currently running:
```
$ volatility pstree
[...]
... 0xffffe001e0270080:chrome.exe      5344   3188     26      0 2019-12-04 17:27:41 UTC+0000
.... 0xffffe001e0a66080:chrome.exe     4128   5344     10      0 2019-12-22 14:50:51 UTC+0000
.... 0xffffe001e303d300:chrome.exe     4144   5344     10      0 2019-12-22 14:49:41 UTC+0000
.... 0xffffe001e1ccc840:chrome.exe     6324   5344     10      0 2019-12-22 14:51:15 UTC+0000
.... 0xffffe001e3142840:chrome.exe     7008   5344     10      0 2019-12-22 14:53:51 UTC+0000
.... 0xffffe001e031c840:chrome.exe     6332   5344     10      0 2019-12-22 14:51:16 UTC+0000
.... 0xffffe001e1583080:chrome.exe     6256   5344     11      0 2019-12-22 14:53:19 UTC+0000
.... 0xffffe001e0bd63c0:chrome.exe     2220   5344     10      0 2019-12-22 14:49:57 UTC+0000
.... 0xffffe001e0a79080:chrome.exe     2172   5344      7      0 2019-12-04 17:33:48 UTC+0000
[...]
```
There are some typical Windows services and a Chrome instance. Fortunately there are some volatility plugins for Chrome analysis.
I've used https://github.com/superponible/volatility-plugins.

```
$ volatility --plugins ./volatility-plugins/ chromehistory | grep -i necsoft
Volatility Foundation Volatility Framework 2.6.1
[...]
72 ftp://necsoftwares.com/ Index of / 
73 ftp://necsoftwares.com/sourcecode/  Index of /sourcecode/ 
[...]
```
Some of the entries that stand out among things like logging into Gmail, googling Kevin Mitnick are entries 72 and 73 which access an FTP server. What's even more suspicious is that the service is not responding, because the domain is pointing at `1.1.1.1`. Time for some DNS archeology.

Searching for the history of `necsoftwares.com` domain we can find the original IP address - `172.104.71.146`, last seen on `2019-12-30`.

FTP server is working, however login and password is required. We have to dig deeper. We can dump Chrome memory and look for credentials.

```
$ volatility memdump -p 5344 -D ./chrome-dump
```

Grepping the strings for `ftp://necsoftwares.com`, we can find:
```
ftp://necsoftwares.com com.ftp://necsoftwares kev1n_mitn1ck Socia1_engin33ring_c4n_g3t_ev3rything - ftp
```
On the FTP server there's only one file - `sourcecode/nec2dx.f` with the flag:
```
WhiteHat{SHA1(G00D_J0B_Y0u4r3Dump5oExcellen7)}
```
