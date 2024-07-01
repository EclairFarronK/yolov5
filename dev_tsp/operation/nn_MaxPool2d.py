import torch
from torch import nn

method = nn.MaxPool2d(kernel_size=5, stride=1, padding=2, dilation=1)

input = torch.randn(3, 4, 4)
print(input)
output = method(input)
print(output)
output1 = method(output)
print(output1)
output2 = method(output1)
print(output2)
