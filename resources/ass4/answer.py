import pdb

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from torchvision import transforms


# %%
class NN(nn.Module):
    def __init__(self, arr=[]):
        super(NN, self).__init__()
        self.relu = nn.ReLU()
        self.fc1 = nn.Linear(30 * 30 * 3, 128)
        self.fc2 = nn.Linear(128, 5)

    def forward(self, x):
        batch_size = x.shape[0]
        x = x.view(batch_size, -1)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x


# %%
class SimpleCNN(nn.Module):
    def __init__(self, arr=[]):
        super(SimpleCNN, self).__init__()
        self.conv_layer = nn.Conv2d(3, 8, 3)
        self.pool = nn.MaxPool2d(2)
        self.fc1 = nn.Linear(1568, 5)

    def forward(self, x):
        """
        Question 2
        TODO: fill this forward function for data flow
        """

        # convolutional unit
        x = self.conv_layer(x)

        # downsampling unit
        # can repeat convolutional layer --> downsampling layer 

        x = F.relu(x) # should go first?

        # global average pooling
        x = self.pool(x)


        # get batch to connect to fully connected layer
        batch_size = x.shape[0]
        x = x.view(batch_size, -1)

        # fully-connected or linear layer (rectified linear layer?)
        x = self.fc1(x)

        return x


# %%
basic_transformer = transforms.Compose([transforms.ToTensor()])

"""
Question 3
TODO: Add color normalization to the transformer. For simplicity, let us use 0.5 for mean
      and 0.5 for standard deviation for each color channel.
"""
norm_transformer = transforms.Compose([transforms.ToTensor(), # make it a tensor
                                       transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]) # normalize all three color channels for a mean and standard deviation of 0.5


# %%
class DeepCNN(nn.Module):
    def __init__(self, arr=[]):
        super(DeepCNN, self).__init__()
        """
        Question 4
        TODO: setup the structure of the network
        """

        # arr[# channels in convolutional layer, # channels in convolutional layer, # channels in convolutional layer, "pool" if pooling desired]
        self.arr = arr

        self.conv1 = nn.Conv2d(3, arr[0], 3)
        self.conv2 = nn.Conv2d(arr[0], arr[1], 3)
        self.conv3 = nn.Conv2d(arr[1], arr[2], 3)

        if(arr[3] == "pool"):
            self.pool = nn.MaxPool2d(2)
            self.fc1 = nn.Linear(arr[2] * 12 * 12, 5)
        else:
            self.pool = nn.MaxPool2d(1) # 1 item kernel (same as not pooling?)
            self.fc1 = nn.Linear(arr[2] * 24 * 24, 5)
        



    def forward(self, x):
        """
        Question 4
        TODO: setup the flow of data (tensor)
        """
        # add a ReLU layer after each conv layer


        x = self.conv1(x)
        x = F.relu(x)

        x = self.conv2(x)
        x = F.relu(x)

        x = self.conv3(x)
        x = F.relu(x)

        x = self.pool(x)

        batch_size = x.shape[0]
        x = x.view(batch_size, -1)

        x = self.fc1(x)

        return x


# %%
"""
Question 5
TODO:
    change the train_transformer to a tranformer with random horizontal flip
    and random affine transformation
    1. It should randomly flip the image horizontally with probability 50%
    2. It should apply random affine transformation to the image, which randomly rotate the image 
        within 5 degrees, and shear the image within 10 degrees.
    3. It should include color normalization after data augmentation. Similar to question 3.
"""

"""Add random data augmentation to the transformer"""
aug_transformer = transforms.Compose([
    transforms.ToTensor(),
    transforms.RandomHorizontalFlip(),
    transforms.RandomAffine(5, shear=10),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])