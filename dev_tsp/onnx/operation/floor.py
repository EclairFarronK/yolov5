import onnx
import numpy as np
import torch

x = np.random.randn(40).astype(np.float32)
print(x)
y = np.floor(x)
print(y)
