# Special (Misc, 405p, 58 solved)

```
You will find a special path where the answer lies. 
```

A recon task, where nothing is given.
We spent some time looking around for some strange js files, comment in source code of the page etc. by to no avail.
Then just accidentally someone got interested in the [background of the CTF webpage](background.jpg).
It's rather common to place some random codes on IT webpages in images/logos etc, but still it might be something.
Once you try to read the blurry code it becomes obvious that this is in fact the `Special` task.

The code is quite simple, we have hexbytes which should get decoded to ascii chars, the resulting string is again hex encoded so we need to decode it one more time and finally we have to invert it to get the flag.

The hard part was to type down those blurry values but in the end we got it:

```python
"".join([chr(int(c,16)) for c in '37 39 37 33 36 31 36 35 37 30 35 66 37 39 37 33 36 31 36 35'.split()]).decode("hex")[::-1]
```

Which becomes a flag: `EKO{easy_peasy}`
