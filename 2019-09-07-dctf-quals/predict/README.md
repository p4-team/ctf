# Predict
In this task we get three files `flag.npy`, `X.npy` and `y.npy`.

It's pretty obvious given the name of the challenge and the format of the files that we are supposed to learn a classifier based on `X.npy` and `y.npy` that will classify data in `flag.npy` to retrieve the flag.

### Format
X shape = `(40000, 50, 50, 3)`

Flag shape = `(560, 50, 50, 3)`

After inspection of `y.npy` we can see that there are only two classes.

So we have 40k data to learn from. This should easily suffice.

I adapted some keras CNN example code to the shapes of the arrays above and tried to decode the flag after each epoch of learning (instead of at the end, this helps with cases of overfitting). For each entry from flag classified as first class I wrote down `0` and `1` otherwise. 
This string concatenated and converted to ASCII is the final flag.

It took around 14 epochs to get the correct flag.

Code of the solution is in `get_flag.py`.

