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

After decrypting `cnc.enc` using password `amFjaGltXWhvXHhvXG9zbH4vamU`, we saw a link to [this Gist](https://gist.github.com/loyza0/9035bc975c3786952df60bf57d490285/)

```
#echo Flag
#echo TMCT... #removed in this cmd
cp /etc/passwd /var/www/html/p0004.html
```

Unfortunately flag was removed from that one and there was no revision containing the actual flag. We've started to look for another link in previous commits.

```
agent$ git log
commit 2fdc0abda09847a28ba7c9c36e7322b8a87c57d9 (HEAD, origin/master, origin/HEAD, old, master)
Author: loyza0 <54145325+loyza0@users.noreply.github.com>
Date:   Sat Aug 17 14:47:36 2019 -0700

    new cnc

commit 152ce9e6ce69bd84b666a0ec31c3b32525d0a527
Author: loyza0 <54145325+loyza0@users.noreply.github.com>
Date:   Sat Aug 17 09:28:29 2019 -0700

    new cnc

commit 05c54c7b35cf17503d05be2be2254ab4df76b3b6
Author: loyza0 <54145325+loyza0@users.noreply.github.com>
Date:   Sat Aug 17 07:19:33 2019 -0700

    new cnc

...

====

private$ git log
commit b008e8c18346f7c59c293721410fdb62e79a0b42 (HEAD -> master, origin/master, origin/HEAD)
Author: loyza0 <54145325+loyza0@users.noreply.github.com>
Date:   Sat Aug 17 14:49:18 2019 -0700

    new pwd

commit 9379a8b245aed2aac3be27e559613f5fd6e943d5
Author: loyza0 <54145325+loyza0@users.noreply.github.com>
Date:   Sat Aug 17 09:26:13 2019 -0700

    new pwd

commit b064ff44b49ef273023313586d4a54e754d253e5
Author: loyza0 <54145325+loyza0@users.noreply.github.com>
Date:   Thu Aug 15 17:02:19 2019 +0200

    Create pwd.txt

...
```

```
$ git diff HEAD HEAD~1
diff --git a/pwd.txt b/pwd.txt
index 2dbd3d2..d6a5e48 100644
--- a/pwd.txt
+++ b/pwd.txt
@@ -1 +1 @@
-amFjaGltXWhvXHhvXG9zbH4vamU
+amFjaGltZWhvZHhvZG9zdH4vamU
```

Password and ciphered text has been changed two times. The flag was in `agent:152ce9e` and we were able to decrypt it using password `amFjaGltZWhvZHhvZG9zdH4vamU` from `private:9379a8b`.

```
echo flag
echo 'TMCTF{GHC461708DV}'
```

... and 300 points has been earned for this task!