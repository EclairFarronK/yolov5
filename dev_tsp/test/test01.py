import numpy as np
import onnx

# from torch import onnx

x = np.array(
    [
        [
            [
                [0.0, 1.0, 2.0, 3.0, 4.0],  # (1, 1, 5, 5) input tensor
                [5.0, 6.0, 7.0, 8.0, 9.0],
                [10.0, 11.0, 12.0, 13.0, 14.0],
                [15.0, 16.0, 17.0, 18.0, 19.0],
                [20.0, 21.0, 22.0, 23.0, 24.0],
            ]
        ]
    ]
).astype(np.float32)
W = np.array(
    [
        [
            [
                [1.0, 1.0, 1.0],  # (1, 1, 3, 3) tensor for convolution weights
                [1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0],
            ]
        ]
    ]
).astype(np.float32)

# Convolution with padding
node_with_padding = onnx.helper.make_node(
    "Conv",
    inputs=["x", "W"],
    outputs=["y"],
    kernel_shape=[3, 3],
    # Default values for other attributes: strides=[1, 1], dilations=[1, 1], groups=1
    pads=[1, 1, 1, 1],
)
y_with_padding = np.array(
    [
        [
            [
                [12.0, 21.0, 27.0, 33.0, 24.0],  # (1, 1, 5, 5) output tensor
                [33.0, 54.0, 63.0, 72.0, 51.0],
                [63.0, 99.0, 108.0, 117.0, 81.0],
                [93.0, 144.0, 153.0, 162.0, 111.0],
                [72.0, 111.0, 117.0, 123.0, 84.0],
            ]
        ]
    ]
).astype(np.float32)
expect(
    node_with_padding,
    inputs=[x, W],
    outputs=[y_with_padding],
    name="test_basic_conv_with_padding",
)

# Convolution without padding
node_without_padding = onnx.helper.make_node(
    "Conv",
    inputs=["x", "W"],
    outputs=["y"],
    kernel_shape=[3, 3],
    # Default values for other attributes: strides=[1, 1], dilations=[1, 1], groups=1
    pads=[0, 0, 0, 0],
)
y_without_padding = np.array(
    [
        [
            [
                [54.0, 63.0, 72.0],  # (1, 1, 3, 3) output tensor
                [99.0, 108.0, 117.0],
                [144.0, 153.0, 162.0],
            ]
        ]
    ]
).astype(np.float32)
expect(
    node_without_padding,
    inputs=[x, W],
    outputs=[y_without_padding],
    name="test_basic_conv_without_padding",
)
