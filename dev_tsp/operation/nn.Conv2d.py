import torch
from torch import nn

method = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=6, stride=1, padding=2)
input = torch.randn(3, 32, 32)
print(input.shape)
output = method(input)
print(output.shape)
