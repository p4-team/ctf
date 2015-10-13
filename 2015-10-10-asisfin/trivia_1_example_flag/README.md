## What's example flag?

There is an example flag in http://asis-ctf.ir/rules/ :

    ASIS{476f20676f6f2e676c2f67776a625466}

However, that's not the flag we are looking for. This supposed MD5 hash is actually hex encoded ASCII.

	bytes.fromhex('476f20676f6f2e676c2f67776a625466').decode('ascii')

evaluates to:

    Go goo.gl/gwjbTf

where we can find the real flag:

    hi all, the flag is: ASIS{c0966ad97f120b58299cf2a727f9ca59}