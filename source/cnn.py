import torch
import torchvision as tv
import torchsummary
from PIL import Image
from matplotlib import pyplot as plt
import random


RESOLUTION = 64

# 4 * 18600
samples0, samples1 = 16000, 2600
classes = 4
class_names = ['circle', 'triangle', 'square', 'triangle_flip']

DATABASE = torch.empty((samples0 + samples1) * classes, 1, RESOLUTION, RESOLUTION)
DATACLASS = torch.empty((samples0 + samples1) * classes, dtype = torch.int64)

DATA0 = torch.empty(samples0 * classes, 1, RESOLUTION, RESOLUTION)
TARGET0 = torch.empty(samples0 * classes, dtype = torch.int64)

DATA1 = torch.empty(samples1 * classes, 1, RESOLUTION, RESOLUTION)
TARGET1 = torch.empty(samples1 * classes, dtype = torch.int64)

for n in range(classes):
    name = class_names[n]
    PATH = './database_crop/' + name + '/'
    print("Extracting Files from Path : ", PATH)
    for index in range(samples0 + samples1):
        fileName = PATH + name + str(1 + index).rjust(4, '0')
        # print("Extracting Training File : ", fileName)
        img = Image.open(fileName + '.png')
        DATABASE[(samples0 + samples1) * n + index] = tv.transforms.functional.to_tensor(img)
        DATACLASS[(samples0 + samples1) * n + index] = n

    sampling = sorted(random.sample(range(samples0 + samples1), samples1))
    s0, s1 = 0, 0
    for index in range(samples0 + samples1):
        if sampling[s1] == index:
            DATA1[samples1 * n + s1] = DATABASE[(samples0 + samples1) * n + index]
            TARGET1[samples1 * n + s1] = DATACLASS[(samples0 + samples1) * n + index]
            s1 += 1
            if s1 == samples1:
                s1 = 0
        else:
            DATA0[samples0 * n + s0] = DATABASE[(samples0 + samples1) * n + index]
            TARGET0[samples0 * n + s0] = DATACLASS[(samples0 + samples1) * n + index]
            s0 += 1

# GRID0 = tv.utils.make_grid(DATA0, 10, pad_value = 1)
# plt.imshow(GRID0.permute(1, 2, 0))
# plt.show()

# GRID1 = tv.utils.make_grid(DATA1, 20, pad_value = 1)
# plt.imshow(GRID1.permute(1, 2, 0))
# plt.show()

# source0 = tv.datasets.MNIST("../MNIST", train = True, download = True)
# source1 = tv.datasets.MNIST("../MNIST", train = False, download = True)
DATA0 = DATA0.cuda()
DATA1 = DATA1.cuda()
TARGET0 = TARGET0.cuda()
TARGET1 = TARGET1.cuda()

model = torch.nn.Sequential(                    #  64
    torch.nn.Conv2d(1, 8, 5),                   #  60 = 64 - (5 - 1)
    torch.nn.ReLU(),
    torch.nn.MaxPool2d(2),                      #  30 = 60 / 2

    torch.nn.Conv2d(8, 16, 7),                  #  24 = 30 - (7- 1)
    torch.nn.ReLU(),
    torch.nn.MaxPool2d(2),                      #  12 = 24 / 2

    torch.nn.Flatten(),
    torch.nn.Linear(16 * 12 * 12, 72),
    torch.nn.ReLU(),
    torch.nn.Linear(72, 12),
    torch.nn.ReLU(),
    torch.nn.Linear(12, 4)
).cuda()
variables = model.parameters()

torchsummary.summary(model, input_size = DATA0.shape[1:])

samples0 *= classes
samples1 *= classes

tc = 0
batch = 300
optimizer = torch.optim.Adam(variables) #, lr = 0.001)
for epoch in range(100):
    LOSS0 = torch.zeros((), device = "cuda")
    ACCURACY0 = torch.zeros((), device = "cuda")
    count0 = 0
    for index in range(0, samples0, batch):
        optimizer.zero_grad()
        DATA = DATA0[index : index + batch]
        TARGET = TARGET0[index : index + batch]
        count = TARGET.size(0)
        ACTIVATION = model(DATA)
        LOSS = torch.nn.functional.cross_entropy(ACTIVATION, TARGET)
        LOSS0 += LOSS * count
        VALUE = torch.argmax(ACTIVATION, 1)
        ACCURACY0 += torch.sum(VALUE == TARGET)
        count0 += count
        LOSS.backward()
        optimizer.step()
    LOSS0 /= count0
    ACCURACY0 /= count0
    with torch.no_grad():
        LOSS1 = torch.zeros((), device = "cuda")
        ACCURACY1 = torch.zeros((), device = "cuda")
        count1 = 0
        for index in range(0, samples1, batch):
            DATA = DATA1[index : index + batch]
            TARGET = TARGET1[index : index + batch]
            ACTIVATION = model(DATA)
            LOSS1 += torch.nn.functional.cross_entropy(ACTIVATION, TARGET, reduction = "sum")
            VALUE = torch.argmax(ACTIVATION, 1)
            ACCURACY1 += torch.sum(VALUE == TARGET)
            count1 += TARGET.size(0)
        LOSS1 /= count1
        ACCURACY1 /= count1
    print("%5d %12.3f %4.3f %12.3f %4.3f" % \
          (epoch, LOSS0, ACCURACY0, LOSS1, ACCURACY1), flush = True)
    if ACCURACY1 > 0.9997:
        tc += 1
    if tc == 5:
        torch.save(model.state_dict(), './cnn/model.pth')

