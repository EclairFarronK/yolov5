import cv2
import numpy as np
import torch.nn
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        # out_channels为多少就有多少个卷积核，如果in_channels=3，out_channels=6？
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=5, kernel_size=3, stride=1, padding=0)
        # self.conv2 = nn.Conv2d(in_channels=3, out_channels=20, kernel_size=5, stride=1, padding=0)

    def forward(self, x):
        # x = F.relu(self.conv1(x))
        # return F.relu(self.conv2(x))
        return self.conv1(x)


image = cv2.imread('../../data/images/bus.jpg')
print(image.shape)
# todo 这就是矩阵的转置？
image = image.transpose(2, 0, 1)
print(image.shape)
# image = np.array(image)
image = torch.tensor(image)

# 选一个就行了
# image = image.to(torch.float32)
image = image.float()
print(image.shape)

model = Model()
loss_function = torch.nn.MSELoss()
# optim和Module关联
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
optimizer.step()
for i in range(1000):
    data = model.forward(image)
    print(data.shape)
    # 计算损失
    loss = loss_function(data, 'rusult')

    optimizer.zero_grad()
    # 反向传播
    loss.backward()
    optimizer.step()
    # todo 卷积核的参数在哪里？在model里面还是在loss里面？

# torch.nn.functional.conv2d(input, 'weight', bias=None, stride=1, padding=0, dilation=1, groups=1)
