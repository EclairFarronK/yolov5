import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np

import onnx
from onnx.backend.test.case.test_case import TestCase
from onnx.backend.test.case.utils import import_recursive
from onnx.onnx_pb import (
    AttributeProto,
    FunctionProto,
    GraphProto,
    ModelProto,
    NodeProto,
    TensorProto,
    TypeProto,
)

_NodeTestCases = []
_TargetOpType = None
_DiffOpTypes = None


def expect(
        node_op: onnx.NodeProto,
        inputs: Sequence[Union[np.ndarray, TensorProto]],
        outputs: Sequence[Union[np.ndarray, TensorProto]],
        name: str,
        **kwargs: Any,
) -> None:
    # skip if the node_op's op_type is not same as the given one
    if _TargetOpType and node_op.op_type != _TargetOpType:
        return
    if _DiffOpTypes is not None and node_op.op_type.lower() not in _DiffOpTypes:
        return

    # in case node_op is modified
    node = deepcopy(node_op)
    present_inputs = [x for x in node.input if (x != "")]
    present_outputs = [x for x in node.output if (x != "")]
    input_type_protos = [None] * len(inputs)
    if "input_type_protos" in kwargs:
        input_type_protos = kwargs["input_type_protos"]
        del kwargs["input_type_protos"]
    output_type_protos = [None] * len(outputs)
    if "output_type_protos" in kwargs:
        output_type_protos = kwargs["output_type_protos"]
        del kwargs["output_type_protos"]
    inputs_vi = [
        _extract_value_info(arr, arr_name, input_type)
        for arr, arr_name, input_type in zip(inputs, present_inputs, input_type_protos)
    ]
    outputs_vi = [
        _extract_value_info(arr, arr_name, output_type)
        for arr, arr_name, output_type in zip(
            outputs, present_outputs, output_type_protos
        )
    ]
    graph = onnx.helper.make_graph(
        nodes=[node], name=name, inputs=inputs_vi, outputs=outputs_vi
    )
    kwargs["producer_name"] = "backend-test"

    if "opset_imports" not in kwargs:
        # To make sure the model will be produced with the same opset_version after opset changes
        # By default, it uses since_version as opset_version for produced models
        produce_opset_version = onnx.defs.get_schema(
            node.op_type, domain=node.domain
        ).since_version
        kwargs["opset_imports"] = [
            onnx.helper.make_operatorsetid(node.domain, produce_opset_version)
        ]

    model = _make_test_model_gen_version(graph, **kwargs)

    _NodeTestCases.append(
        TestCase(
            name=name,
            model_name=name,
            url=None,
            model_dir=None,
            model=model,
            data_sets=[(inputs, outputs)],
            kind="node",
            rtol=1e-3,
            atol=1e-7,
        )
    )

    # Create list of types for node.input, filling a default TypeProto for missing inputs:
    # E.g. merge(["x", "", "y"], [x-value-info, y-value-info]) will return [x-type, default-type, y-type]
    def merge(
            node_inputs: List[str], present_value_info: List[onnx.ValueInfoProto]
    ) -> List[TypeProto]:
        if node_inputs:
            if node_inputs[0] != "":
                return [
                    present_value_info[0].type,
                    *merge(node_inputs[1:], present_value_info[1:]),
                ]
            else:
                return [TypeProto(), *merge(node_inputs[1:], present_value_info)]
        return []

    merged_types = merge(list(node.input), inputs_vi)
    (
        expanded_tests,
        since_version,
    ) = function_testcase_helper(node, merged_types, name)
    for expanded_function_nodes, func_opset_import in expanded_tests:
        kwargs["producer_name"] = "backend-test"

        # TODO: if kwargs["opset_imports"] already exists, only generate test case for the opset version.
        # replace opset versions with what are specified in function proto
        if "opset_imports" not in kwargs:
            kwargs["opset_imports"] = func_opset_import
        else:
            for opset_import in func_opset_import:
                matches = [
                    opset
                    for opset in kwargs["opset_imports"]
                    if opset.domain == opset_import.domain
                ]
                if matches:
                    matches[0].version = opset_import.version
                else:
                    kwargs["opset_imports"].append(opset_import)

        onnx_ai_opset_version = ""
        if "opset_imports" in kwargs:
            onnx_ai_opset_imports = [
                oi for oi in kwargs["opset_imports"] if oi.domain in ("", "ai.onnx")
            ]
            if len(onnx_ai_opset_imports) == 1:
                onnx_ai_opset_version = onnx_ai_opset_imports[0].version

        function_test_name = name + "_expanded"
        if onnx_ai_opset_version and onnx_ai_opset_version != since_version:
            function_test_name += f"_ver{onnx_ai_opset_version}"
        graph = onnx.helper.make_graph(
            nodes=expanded_function_nodes,
            name=function_test_name,
            inputs=inputs_vi,
            outputs=outputs_vi,
        )
        model = _make_test_model_gen_version(graph, **kwargs)
        _NodeTestCases.append(
            TestCase(
                name=function_test_name,
                model_name=function_test_name,
                url=None,
                model_dir=None,
                model=model,
                data_sets=[(inputs, outputs)],
                kind="node",
                rtol=1e-3,
                atol=1e-7,
            )
        )
