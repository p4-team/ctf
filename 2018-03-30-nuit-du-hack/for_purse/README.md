# Where is my purse (for)

In the task we get a large filesystem image and a memdump to work with.
Interesting part of memdump is a running KeePass instance.

We got some password-like strings from it, but we've never actually used them.
For some reason they were not necessary at all.

We've looked around the drive image and the only unusual files we've noticed were connected with `Dcrwallet` (which had some connotation with "purse" from the task name).
We grabbed all the files of the wallet, and there was a [db file](wallet.db) which contains plaintext string `flag{thx_you_found_my_wallet}`
