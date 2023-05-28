import torch
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)  # Assuming the input is an RGB image
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        # Adapt the size of the linear layer based on your image dimensions
        self.fc1 = nn.Linear(64 * 25 * 25, 512)  # 25*25 is the resulting dimension after two pooling operations on a 100*100 image
        self.fc2 = nn.Linear(512, 4)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.contiguous().view(-1, 64 * 25 * 25)  # Flatten the tensor
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        # Apply tanh to first three outputs and sigmoid to the last one
        x = torch.cat((torch.tanh(x[:, :3]), torch.sigmoid(x[:, 3:])), dim=1)
        return x
