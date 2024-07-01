import torch

input1 = torch.randn(3, 2, 2)
print(input1)
input2 = torch.randn(3, 2, 2)
print(input2)
output = torch.cat((input1, input2), 0)
print(output)
