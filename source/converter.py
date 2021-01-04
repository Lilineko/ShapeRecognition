from PIL import Image, ImageDraw

CLASS = 'circle'
PATH = './database/' + CLASS + '/'
BACKGROUND_COLOR = 'black'
RESOLUTION = 128
COUNT = 100

for index in range(1, 1 + COUNT):
    fileName = PATH + CLASS + str(index).rjust(4, '0')
    print("Operatin on file : ", fileName)
    eps = Image.open(fileName + '.eps')
    eps = eps.resize((RESOLUTION, RESOLUTION), Image.ANTIALIAS)
    img = Image.new('RGB', (RESOLUTION, RESOLUTION), BACKGROUND_COLOR)
    img.paste(eps, eps.split()[-1])
    img.save(fileName + '.png', 'png')
