# CRC

In this task we were given 26 encrypted zip files. It is easy to notice though, that they have
very small size - they uncompress to 5 byte files. That means we should be able to brute force
the actual contents, and check their validity using crc, since ZIPs contain CRC32 of 
their uncompressed contents:
```
[adam@adam-Y510P ~/CTF/backdoor/zipcrc]λ unzip -lv 0.zip
Archive:  0.zip
 Length   Method    Size  Cmpr    Date    Time   CRC-32   Name
--------  ------  ------- ---- ---------- ----- --------  ----
       5  Stored        5   0% 2015-11-26 19:49 a36bb2ae  0.txt
--------          -------  ---                            -------
       5                5   0%                            1 file
```
We listed all CRCs in `list`, and wrote a brute forcer - `check.cpp`. It looped over all printable
5-character strings and calculated its CRC, after which it checked whether it fits any zip.

Unfortunately there were many collisions, so we wrote a quick visualizer showing possibilites
for each zip (`parse.py`). Output:
```
[ p,id] [ func] [h&3o4] [func(] [) { e] [.ERM*] [H'9!R] [!LZW(] ["; fo] [ngxh4]
[<?php] [<))ow] [tion ] [z:2b<] [5o'!q] [B6In]  [The F] [M?wSl] [>t|g{] [r($i ] 
[PL]l4]                         [ESV$!] [^y#Hz]         [Qp+Rx]
                                        [cho "]         [lag: ]                
                                        ['3!6]          [p.;;4]                 


[!ol:4] [$i < ] [/}g!0] [8IJE<] [echo ] [.EOE8] [)VPL7] [ (($i]
[= 0; ] [8&|=4] [32; $] [Hu;@l] [y,4n4] [B6bA|] [E%}Hs] [<gt%}] 
[lBQW<] [TUQ9p] [bPZL8] [T:gAx]         [^y>@h] [Yj!Ig] [qJIHu]
                        [i++) ]         [chr(0] [d{m!?]        
                        [udw(4]         ['.)$]  [x41 +]          




[ ^ 0x] [-}u!1] [ 0x19] [)); e] [.ERM*] [,RS>p] [ao:tz] [2JHW<] [*4DeR]
[PbQ5(] [12) %] [<$0-]  [5fg!q] [B6In]  [@!~:4] [} fun] [Bv9Rl]
[q<A\d] [`PHL9] [LCU5}] [xKZLy] [^y#Hz] [\n"; ]         [^9eSx] 
                                [cho "] [anSx]          [c(); ]         
                                ['3!6]  [}02Rl]         [gu:4]            
```
We quickly noticed it should be a PHP code (`<?php` in the first block gives it away). Connecting
the dots, we manually created the script:
```
function func() { 
	echo "The Flag: "; 
	for($i = 0; $i<32; $i++) 
		echo chr(0x41 + (($i ^ 0x12) % 0x19)); 
	echo "\n"; 
} 
func();
```
After running it, we got the flag.
