from PIL import Image
import sys

s=open(sys.argv[1],"rb").read()

im=Image.new("L", (601, 600))
im.putdata(s)
im.save("out.png")
