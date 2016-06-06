from PIL import Image
import sys, math

nice = []

for f in range(464):

	im = Image.open("tv/out-"+str(f)+".png")
	pix = im.load()

	for y in range(200):
		for x in range(200):

			if(pix[y, x] != 0 and pix[y, x] != 0xff):
				if(f not in nice):
					nice.append(f)
print(nice)


			
