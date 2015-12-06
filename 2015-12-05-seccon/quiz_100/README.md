## Command-Line Quiz (Unknown, 100p)

    telnet caitsith.pwn.seccon.jp
    User:root
    Password:seccon
    The goal is to find the flag word by "somehow" reading all *.txt files.

###PL
[ENG](#eng-version)

Łączymy się ze wskazanym serwerem: 

```
CaitSith login: root
Password:
$ ls
bin         flags.txt   linuxrc     stage1.txt  stage4.txt  usr
dev         init        proc        stage2.txt  stage5.txt
etc         lib         sbin        stage3.txt  tmp
$ cat flags.txt
cat: can't open 'flags.txt': Operation not permitted
$ cat stage1.txt
What command do you use when you want to read only top lines of a text file?

Set your answer to environment variable named stage1 and execute a shell.

  $ stage1=$your_answer_here sh

If your answer is what I meant, you will be able to access stage2.txt file.
$ cat stage2.txt
cat: can't open 'stage2.txt': Operation not permitted
```

Jesteśmy w stanie przeczytać tylko plik stage1.txt, kolejne są odblokowywane w momencie kiedy
rozwiążemy poprzednie zagadki. Więc idziemy po kolei:

```
$ cat stage1.txt
What command do you use when you want to read only top lines of a text file?

Set your answer to environment variable named stage1 and execute a shell.

  $ stage1=$your_answer_here sh

If your answer is what I meant, you will be able to access stage2.txt file.
$ stage1=head sh
$ cat stage2.txt
What command do you use when you want to read only bottom lines of a text file?

Set your answer to environment variable named stage2 and execute a shell.

  $ stage2=$your_answer_here sh

If your answer is what I meant, you will be able to access stage3.txt file.
$ stage2=tail sh
$ cat stage3.txt
What command do you use when you want to pick up lines that match specific patterns?

Set your answer to environment variable named stage3 and execute a shell.

  $ stage3=$your_answer_here sh

If your answer is what I meant, you will be able to access stage4.txt file.
$ stage3=grep sh
$ cat stage4.txt
What command do you use when you want to process a text file?

Set your answer to environment variable named stage4 and execute a shell.

  $ stage4=$your_answer_here sh

If your answer is what I meant, you will be able to access stage5.txt file.
$ stage4=awk sh
$ cat stage5.txt
OK. You reached the final stage. The flag word is in flags.txt file.

flags.txt can be read by only one specific program which is available
in this server. The program for reading flags.txt is one of commands
you can use for processing a text file. Please find it. Good luck. ;-)
$ sed -e ''  flags.txt
OK. You have read all .txt files. The flag word is shown below.

SECCON{CaitSith@AQUA}
```

### ENG version

We connect to server pointed in description:

```
CaitSith login: root
Password:
$ ls
bin         flags.txt   linuxrc     stage1.txt  stage4.txt  usr
dev         init        proc        stage2.txt  stage5.txt
etc         lib         sbin        stage3.txt  tmp
$ cat flags.txt
cat: can't open 'flags.txt': Operation not permitted
$ cat stage1.txt
What command do you use when you want to read only top lines of a text file?

Set your answer to environment variable named stage1 and execute a shell.

  $ stage1=$your_answer_here sh

If your answer is what I meant, you will be able to access stage2.txt file.
$ cat stage2.txt
cat: can't open 'stage2.txt': Operation not permitted
```

We can only read stage1.txt file, other files are locked untill we solve earlier challenges. So we proceed step by step:

```
$ cat stage1.txt
What command do you use when you want to read only top lines of a text file?

Set your answer to environment variable named stage1 and execute a shell.

  $ stage1=$your_answer_here sh

If your answer is what I meant, you will be able to access stage2.txt file.
$ stage1=head sh
$ cat stage2.txt
What command do you use when you want to read only bottom lines of a text file?

Set your answer to environment variable named stage2 and execute a shell.

  $ stage2=$your_answer_here sh

If your answer is what I meant, you will be able to access stage3.txt file.
$ stage2=tail sh
$ cat stage3.txt
What command do you use when you want to pick up lines that match specific patterns?

Set your answer to environment variable named stage3 and execute a shell.

  $ stage3=$your_answer_here sh

If your answer is what I meant, you will be able to access stage4.txt file.
$ stage3=grep sh
$ cat stage4.txt
What command do you use when you want to process a text file?

Set your answer to environment variable named stage4 and execute a shell.

  $ stage4=$your_answer_here sh

If your answer is what I meant, you will be able to access stage5.txt file.
$ stage4=awk sh
$ cat stage5.txt
OK. You reached the final stage. The flag word is in flags.txt file.

flags.txt can be read by only one specific program which is available
in this server. The program for reading flags.txt is one of commands
you can use for processing a text file. Please find it. Good luck. ;-)
$ sed -e ''  flags.txt
OK. You have read all .txt files. The flag word is shown below.

SECCON{CaitSith@AQUA}
```

