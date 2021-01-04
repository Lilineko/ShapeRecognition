from PIL import Image
from skimage.io import imread
from skimage.morphology import convex_hull_image
from matplotlib import pyplot as plt
import numpy as np

RESOLUTION = 64
SAMPLES_PER_CLASS = 18600

classes = 3
class_names = ['circle', 'triangle', 'square']

for name in class_names:
    READPATH = './database/' + name + '/'
    WRITEPATH = './database_crop/' + name + '/' 
    images = [imread(READPATH + name + str(1 + index).rjust(4, '0') + '.png') for index in range(SAMPLES_PER_CLASS)]
    index = 0
    for img in images:
        threshold = 0.5
        img[img <= threshold] = 0
        img[img > threshold] = 1
        chull = convex_hull_image(img)
        imageBox = Image.fromarray((chull*255).astype(np.uint8)).getbbox()
        cropped = Image.fromarray((img*255).astype(np.uint8), mode = 'L').crop(imageBox)
        cropped = cropped.resize((RESOLUTION, RESOLUTION))
        cropped.save(WRITEPATH + name + str(1 + index).rjust(4, '0') + '.png', 'png')
        index += 1

### TODO: add cropping and resizing to 64x64