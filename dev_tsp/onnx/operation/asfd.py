import onnx
import numpy as np

x = np.random.randn(3, 4, 5).astype(np.float32)
print(x)
print(x.shape)
print(x.ndim)
for i in range(x.ndim):
    axes = np.array([i]).astype(np.int64)
    node = onnx.helper.make_node(
        "Unsqueeze",
        inputs=["x", "axes"],
        outputs=["y"],
    )
    y = np.expand_dims(x, axis=i)
print(y)
