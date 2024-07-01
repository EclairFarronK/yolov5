import numpy as np
import onnx
def shape_reference_impl(x, start=None, end=None):  # type: ignore
    dims = x.shape[start:end]
    return np.array(dims).astype(np.int64)
def test_shape(testname, xval, start=None, end=None):  # type: ignore
    node = onnx.helper.make_node(
        "Shape", inputs=["x"], outputs=["y"], start=start, end=end
    )

    yval = shape_reference_impl(xval, start, end)

    expect(node, inputs=[xval], outputs=[yval], name="test_shape" + testname)