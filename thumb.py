from PIL import Image
import os


path = r'files/janext/4.jpg'

img = Image.open(path)

width, height = img.size
print(width,height)

if width > height:
    delta = (width - height) / 2
    box = (int(delta), 0, int(width - delta), int(height))
    region = img.crop(box)
elif height > width:
    delta = (height - width) / 2
    box = (0, int(delta), int(width), int(height - delta))
    region = img.crop(box)
else:
    region = img

print(region)

thumb = region.resize((100,100), Image.ANTIALIAS)

base, ext = os.path.splitext(os.path.basename(path))
filename = os.path.join('', '%s_thumb.jpg' % (base,))

thumb.save(filename, quality=100)
