import random
from PIL import Image, ImageOps

RESOLUTION = 128
SAMPLES_PER_CLASS = 300
MAX_ANGLE = 15

classes = 3
class_names = ['circle', 'triangle', 'square']

for name in class_names:
    READPATH = './images/01_init/' + name + '/'
    WRITEPATH = './images/02_transform/' + name + '/'
    images = [Image.open(READPATH + name + str(1 + index).rjust(4, '0') + '.png') for index in range(SAMPLES_PER_CLASS)]

    index = 0
    for img in images:
        img_mirror = ImageOps.mirror(img)

        for angle in range(-MAX_ANGLE, MAX_ANGLE + 1, 1):
            img_new = img.rotate(angle)
            img_new.save(WRITEPATH + name + str(1 + index).rjust(4, '0') + '.png', 'png')
            index += 1
            img_new = img_mirror.rotate(angle)
            img_new.save(WRITEPATH + name + str(1 + index).rjust(4, '0') + '.png', 'png')
            index += 1
