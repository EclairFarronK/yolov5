import torch
from torch import nn

input = torch.arange(1, 13, dtype=torch.float32).view(1, 3, 2, 2)
print(input)
m = nn.Upsample(scale_factor=2, mode='nearest')
output = m(input)
print(output)
