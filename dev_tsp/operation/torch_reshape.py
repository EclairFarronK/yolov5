import torch

input = torch.randn(4, 2, 2)
print(input)
output = torch.reshape(input, (2, 2, 2, 2))
print(output)
