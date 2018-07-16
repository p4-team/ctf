# EX5 (re, 26 solved, 500p)

## Reconnaissance

The task is to reverse-engineer [strange file](M.ex5) that isn't recognizable by file program:

```
a@x:~/Desktop/ex5$ file M.ex5 
M.ex5: data
```

But we can see that the first 3 bytes are `EX5`.
I googled this magic and I've found that this extension is supported by program MetaTrader5.

```
MetaTrader 5 is a free application for traders allowing to perform technical analysis and trading operations in the Forex and exchange markets.
```

EX5 is a compiled script written in MQL5 language which is a language for automated strategies.

I installed MetaTrader5 and I've run this script (dragged and dropped the file).

## Breaking the flag

I've loaded the compiled script by clicking 2 times on it (placed on Desktop).
Then, I've run this script in MetaTrader5 (Clicked on it).

Then I launched process hacker. There was a process called `terminal64.exe`.
I've filtered the memory for string "flag:  
- I've clicked on it and went to tab "memory". Button "strings" -> check mapped, image, private -> ok -> filter -> contains -> "flag".  
One of these was very promising - `0x2d50b56: your flag: %s`. 
I followed this string and ended up in a memory region with other interesting strings:

- `Hello hacker!`
- `Try again!`

They all are encoded in UTF16 format. It is placed length before every string encoded in 4 bytes (little-endian)

One of these strings was very interesting:

```
MdgsskESNr]8`am?}"M!KA~$G[v/\x7fvAO\x14S\x16G\x17X
```

I've xored the beginning of it with flag format prefix and I've got:

```
>>> xor('MdgsskESN','MeePwnCTF')
'\x00\x01\x02#\x04\x05\x06\x07\x08'
```

I've concluded that the key is 0,1,2,3,4...... and so on:

```
>>> xor('MdgsskESNr]8`am?}"M!KA~$G[v/\x7fvAO\x14S\x16G\x17X',range(0,50))
'MeepwnCTF{W3llc0m3_2_Th3_Bl4ck_P4r4d3}kCOZY@i~`]m\t'
>>> 
```

That was the flag.
