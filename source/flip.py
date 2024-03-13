import random
from PIL import Image, ImageOps

SAMPLES_PER_CLASS = 18600

class_names = ['triangle']

for name in class_names:
    READPATH = './images/03_crop/' + name + '/'
    WRITEPATH = './images/03_crop' + name + '_flip/'
    for index in range(SAMPLES_PER_CLASS):
        with Image.open(READPATH + name + str(1 + index).rjust(4, '0') + '.png') as img:
            img_flip = ImageOps.flip(img)
            img_flip.save(WRITEPATH + name + '_flip' + str(1 + index).rjust(4, '0') + '.png', 'png')
