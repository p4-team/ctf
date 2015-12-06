import re

data = open('MrFusion.gpjb', 'rb').read()

def findndx(str, data):
    return [m.start() for m in re.finditer(str, data)]

ext = {
    '.gif': 'GIF89a',
    '.png': '\x89PNG',
    '.bmp': 'BM',
    '.jpg': '\xFF\xD8\xFF\xE0'
}

for ext, pat in ext.iteritems():
    for n in findndx(pat, data):
        open('out.' + str(n) + ext, 'wb').write(data[n:])

