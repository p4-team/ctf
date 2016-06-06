## Television (Misc)
	tl;dr Frames 231 and 463 contain parts of the flag

We're given a gif file, with what looks like static noise. Let's start by splitting it to png of each frame using imagemagick: 
`covert television.gif out.png`

That gave us 463 frames, our first guess was to read the noise as binary and search for the flag in all files but that didn't work out.

While implementing the previous idea, we've noticed that some pixels are not entirely white or black, a quick [script](search.py) told us that this happens only in 2 images. (231 and 463)

After taking a look at them we've noticed some interesting-looking arrangements:

![alt](scr1.png)

Multiplying pixels of those 2 frames gave us an image, from which we could barely read the flag ;)

### Author @apsdehal's solution

Since this was not the expected solution by the author, many people got image with barely readable flag. According to author:

Every image `i` has to be xored `i+1` and resulting image should be xored with image `i+2` and so on. This would result in copies of original images which are xored. Following script can work fine:

Extract pngs in pngs folder and

```bash
cp pngs/0.png pngs/0_comb.png
```

```python
import os
for i in range(0, 463):
	s = 'convert pngs/%d_comb.png pngs/%d.png -fx "(((255*u)&(255*(1-v)))|((255*(1-u))&(255*v)))/255" pngs/%d_comb.png' % (i, i+1, i+1);
	os.system(s)
```

This should result in clearly readable flag in image 231_comb.png and `not yet` written in `463.png`. Xoring these two images lead to unreadable flag because `not yet` and flag overlap each other.
