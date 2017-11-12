# Adversarial (Misc/PPC)

In the task we get the [source code](adversarial-public.py) of the scoring server.
What it does it pretty straightforward:

1. Generate a matrix 100x1000 with random values from (-1,1)
2. Select a single row in this matrix

Our goal is to provide a vector of 100 values from range (-1,1) for which the `1 - get_probability(x)` function calculated on the dot product between our vector and the selected matrix row will be < 0.001

The `get_probability` function is simply:

```python
def get_probability(z):
	return 1./(1+np.exp(-(z)))
```

It's easy to see that in order to get a small final result we need `get_probability` to return a value close to 1.
This implies that we need `e^-z` to be as small as possible, and therefore we want `z` to be as large as possible.

As mentioned above `z` here is just a dot product between selected matrix row and vector we supply.
Dot product is simply a sum of multiplied corresponding vector coordinates, eg. `[1,2,3] * [4,5,6] = 1*4+2*5+3*6`

It's rather trivial to figure out that in order to get the highest possible result we simply need to multiply all negative values by -1 and all positive values by 1:

```python
def solve(feats):
    return [-1 if feats[i] < 0 else 1 for i in range(len(feats))]
```

Whole solver available [here](solver.py)
