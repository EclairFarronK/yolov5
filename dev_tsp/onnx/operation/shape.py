import numpy as np

x = np.array(
    [
        [1, 2, 3],
        [4, 5, 6],
    ]
).astype(np.float32)
test_shape("_example", x)  # preserve names of original test cases

x = np.random.randn(3, 4, 5).astype(np.float32)

test_shape("", x)  # preserve names of original test cases

test_shape("_start_1", x, start=1)

test_shape("_end_1", x, end=1)

test_shape("_start_negative_1", x, start=-1)

test_shape("_end_negative_1", x, end=-1)

test_shape("_start_1_end_negative_1", x, start=1, end=-1)

test_shape("_start_1_end_2", x, start=1, end=2)

test_shape("_clip_start", x, start=-10)

test_shape("_clip_end", x, end=10)