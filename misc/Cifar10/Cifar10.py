import torch
import torchvision
from utils.images import imshow

import torch.nn as nn
import torch.nn.functional as F

import torch.optim as optim
import utils.Cifar10Utils as utils


# Using ``torchvision``, it’s extremely easy to load CIFAR10.

# The output of torchvision datasets are PILImage images of range [0, 1].
# We transform them to Tensors of normalized range [-1, 1].
util = utils.Cifar10Util()

# LET US SHOW SOME OF THE TRAINING IMAGES, FOR FUN

# get some random training images
dataIter = iter(util.trainLoader)
images, labels = dataIter.next()

# show images
imshow(torchvision.utils.make_grid(images))

# print labels
print(' '.join('%5s' % util.classes[labels[j]] for j in range(4)))


# DEFINING A CONVOLUTIONAL NEURAL NETWORK

# Copy the neural network from the Neural Networks section before and modify it to
# take 3-channel images (instead of 1-channel images as it was defined).

class Net(nn.Module):

    def __init__(self):

        super(Net, self).__init__()

        self.conv1 = nn.Conv2d(3, 96, 5,padding=2)

        self.conv2 = nn.Conv2d(96, 128, 5,padding=2)
        
        self.conv3 = nn.Conv2d(128,256, 5, padding=2)

        self.fc1 = nn.Linear(2304, 2048)

        self.fc2 = nn.Linear(2048, 10)
        
        self.pool = nn.MaxPool2d(3, 2)

    def forward(self, x):

        x = self.pool(F.relu(self.conv1(x)))

        x = self.pool(F.relu(self.conv2(x)))
        
        x = self.pool(F.relu(self.conv3(x)))

        x = x.view(-1, 2304)

        x = F.relu(self.fc1(x))

        x = F.relu(self.fc2(x))

        return x

use_gpu = torch.cuda.is_available()
net = Net()

if use_gpu:
    net = net.cuda()


# Define a Loss function and optimizer
# Let's use a Classification Cross-Entropy loss and SGD with momentum.
criterion = nn.CrossEntropyLoss()

optimizer = optim.SGD(
    net.parameters(),
    lr=0.001,
    momentum=0.9
)


# TRAIN THE NETWORK

# This is when things start to get interesting.
# We simply have to loop over our data iterator, and feed the inputs to the
# network and optimize.

for epoch in range(1):  # loop over the dataset multiple times
    running_loss = 0.0

    for i, data in enumerate(util.trainLoader, 0):

        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data

        if use_gpu:
            inputs = inputs.cuda()
            labels = labels.cuda()

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = net(inputs)
       
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
       
        if i % 2000 == 1999:    # print every 2000 mini-batches
            print('[%d, %5d] loss: %.3f' %(epoch + 1, i + 1, running_loss / 2000))
            running_loss = 0.0

print('Finished Training')
