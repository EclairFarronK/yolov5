import torch.nn

# 升维
input = torch.randn(3, 2, 2)
print(input)
output1 = input.unsqueeze(0)
print(output1)
# 降维
output2 = output1.squeeze(0)
print(output2)
