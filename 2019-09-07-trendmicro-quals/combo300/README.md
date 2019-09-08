# Combo 300

We were given a link to a repository with potentially suspicious content: `https://github.com/HelmutVonSay/explorer`. Unfortunately, repository was removed and nowhere forked nor archived.

We've noticed that related account has two another projects and one of them has 10 stargazers, regardless of the fact that it is a:

* fork of another repository ([Hoaxr/DekkCrypt](https://github.com/Hoaxr/DekkCrypt), latest commit from 2016)
* the only change is single commit with added pretty laconic `README.md` file
* HelmutVonSay's fork has more stargazers than original repo

All stargazers joined Github on the same time as HelmutVonSay (15-16 Aug 2019). All ten accounts have been pushed single repository `demo` on their accounts and starred around 50 other (mostly popular) repositories. After looking at these accounts, we've found that another jointly starred repository is [loyza0/agent](https://github.com/loyza0/agent).

Repository contained few files:

* `stargazer.ssh` - SSH private key which can be used for cloning loyza0's private repositories on Github
* `cnc.enc` - encrypted link to secret Gist
* `run.sh` which adds private key to SSH keyring, clones `loyza0/private` repo and uses `pwd.txt` file from that repo to decrypt `cnc.enc` file.

After decrypting `cnc.enc`, we saw a link to [this Gist](https://gist.github.com/loyza0/9035bc975c3786952df60bf57d490285/)

```
#echo Flag
#echo TMCT... #removed in this cmd
cp /etc/passwd /var/www/html/p0004.html
```

Unfortunately flag was removed from that one and there was no revision containing the actual flag. We've started to look for another link.

