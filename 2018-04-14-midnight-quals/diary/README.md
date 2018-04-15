# Diary - Misc (50 + 0), 120 solves

> We found a torn diary on the ground. It seems to belong to a local boy.

In this task we were given a small zipped git repository. Trying to do anything with it (`git log` etc.) failed
with errors. It seemed like we had to find the flag in raw git objects then.

The first thing we did was enough - a simple inspection of the objects:

```
λ cat doit.sh 
zlib-flate -uncompress < $1 | strings  | grep midnight
λ find -exec bash doit.sh {} \;
flate: inflate: data: incorrect header check
flate: inflate: data: incorrect header check
Today I found a flag, it said: midnight{if_an_object_ref_falls_and_no_one_hears} that sounds very interesting.
```
