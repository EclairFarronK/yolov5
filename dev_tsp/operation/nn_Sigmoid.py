import torch
from torch import nn

method = nn.Sigmoid()

input = torch.randn(3, 2, 2)
print(input)
output = method(input)
print(output)
