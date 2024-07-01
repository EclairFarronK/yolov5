import torch

# todo 矩阵的转置？
input = torch.randn(3, 4, 5)
print(input)
output1 = input.permute(1, 2, 0)
print(output1)
print(output1.shape)

output2 = input.transpose(0, 2)
print(output2)
print(output2.shape)
