# Internet of fail - 400p, 10 solves

> The machines are already here, lurking in your things. They've learned to fool humans
> by speaking a strange language. Can you find their secret password? This is running 
> at http://iof.teaser.insomnihack.ch

In this task we got a strange ELF file. Running `readelf -a iof.elf` on it gives us some basic information -
it seems it's a binary for Tensilica Xtensa Processor - from some strings in the binary, we concluded it's
ESP32 chip (a pretty new successor to popular ESP8266). Unfortunately, this being a very unpopular architecture,
there were almost no tools we could use for analysis - IDA does not support Xtensa out of the box, and even adding
some plugins we found on the Internet didn't help (apparently they were meant for reversing original Espressif 
chips).

In the end, we used good old radare2. It turned out the task was pretty challenging - although ELF mentioned entry
point, it was far away from the actual `main` of the application. We were also stumped by some calls to memory
that didn't exist in the ELF - it turns out ESP32 maps ROM in here. This gave us an idea to google some of the
called functions' addresses - and we found 
[this little gem.](https://raw.githubusercontent.com/espressif/esp-idf/master/components/esp32/ld/esp32.rom.ld)

It contains entries of the form `function - address`, which significantly helped in initial reversing. Still, 
we had to get through the RTOS boilerplate code - it didn't even call the main function directly, but rather created
a new task running it. In the end, we found some public ESP32 HTTP 
[server code.](https://github.com/feelfreelinux/myesp32tests/blob/master/examples/http_server.c)
It seemed to match most of the code nicely, with only slight modifications. The only sinificant difference was
in the `serve` function, which contained code responsible for checking the password.

It called around 20 of different functions, each of which had a similar form:
```
if(condition(password)){ g_state^=CONST; }
```
The conditions were somewhat annoying to reverse, not having access to anything more than assembly, we had to 
analyze them by hand. They used various techniques, including, but not limited to, multiplication, division,
summing of MAC address bytes, xoring, etc. After running all the functions, the `g_state` variable was compared
to `0xffff`. We brute forced all the possible subsets of conditions that yielded that result, and filtered
those that didn't make sense (such as `s[3]&17 == 104`). In the end, combining all the conditions using pen and
paper, we got the final password, which worked on the challenge website: `G0t_yoU_xt3ns4!`
