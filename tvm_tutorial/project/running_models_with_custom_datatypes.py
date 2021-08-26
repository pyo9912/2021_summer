import tvm
from tvm import relay
import numpy as np
from tvm.relay.frontend.change_datatype import ChangeDatatype

tvm.target.datatype.register("myfloat", 150)

# Set registers
tvm.target.datatype.register_op(
    tvm.target.datatype.create_lower_func(
        {
            (32, 32): "FloatToCustom32",  # cast from float32 to myfloat32
        }
    ),
    "Cast",
    "llvm",
    "float",
    "myfloat",
)

tvm.target.datatype.register_op(
    tvm.target.datatype.create_lower_func({32: "Custom32Add"}),
    "Add",
    "llvm",
    "myfloat",
)

tvm.target.datatype.register_op(
    tvm.target.datatype.create_lower_func({(32, 32): "Custom32ToFloat"}),
    "Cast",
    "llvm",
    "myfloat",
    "float",
)

tvm.target.datatype.register_op(
    tvm.target.datatype.create_lower_func({32: "FloatToCustom32"}),
    "FloatImm",
    "llvm",
    "myfloat",
)

tvm.target.datatype.register_op(
    tvm.target.datatype.lower_ite, "Call", "llvm", "myfloat", intrinsic_name="tir.if_then_else"
)

tvm.target.datatype.register_op(
    tvm.target.datatype.lower_call_pure_extern,
    "Call",
    "llvm",
    "myfloat",
    intrinsic_name="tir.call_pure_extern",
)

tvm.target.datatype.register_op(
    tvm.target.datatype.create_lower_func({32: "Custom32Mul"}),
    "Mul",
    "llvm",
    "myfloat",
)
tvm.target.datatype.register_op(
    tvm.target.datatype.create_lower_func({32: "Custom32Div"}),
    "Div",
    "llvm",
    "myfloat",
)

tvm.target.datatype.register_op(
    tvm.target.datatype.create_lower_func({32: "Custom32Sqrt"}),
    "Call",
    "llvm",
    "myfloat",
    intrinsic_name="tir.sqrt",
)

tvm.target.datatype.register_op(
    tvm.target.datatype.create_lower_func({32: "Custom32Sub"}),
    "Sub",
    "llvm",
    "myfloat",
)

tvm.target.datatype.register_op(
    tvm.target.datatype.create_lower_func({32: "Custom32Exp"}),
    "Call",
    "llvm",
    "myfloat",
    intrinsic_name="tir.exp",
)

tvm.target.datatype.register_op(
    tvm.target.datatype.create_lower_func({32: "Custom32Max"}),
    "Max",
    "llvm",
    "myfloat",
)

tvm.target.datatype.register_min_func(
    tvm.target.datatype.create_min_lower_func({32: "MinCustom32"}, "myfloat"),
    "myfloat",
)

# Function to convert tensors
def convert_ndarray(dst_dtype, array):
    """Converts an NDArray into the specified datatype"""
    x = relay.var("x", shape=array.shape, dtype=str(array.dtype))
    cast = relay.Function([x], x.astype(dst_dtype))
    with tvm.transform.PassContext(config={"tir.disable_vectorize": True}):
        return relay.create_executor("graph").evaluate(cast)(array)

def get_mobilenet():
    dshape = (1, 3, 224, 224)
    from mxnet.gluon.model_zoo.vision import get_model

    block = get_model("mobilenet0.25", pretrained=True)
    shape_dict = {"data": dshape}
    return relay.frontend.from_mxnet(block, shape_dict)


def get_cat_image():
    from tvm.contrib.download import download_testdata
    from PIL import Image

    url = "https://gist.githubusercontent.com/zhreshold/bcda4716699ac97ea44f791c24310193/raw/fa7ef0e9c9a5daea686d6473a62aacd1a5885849/cat.png"
    dst = "cat.png"
    real_dst = download_testdata(url, dst, module="data")
    img = Image.open(real_dst).resize((224, 224))
    # CoreML's standard model image format is BGR
    img_bgr = np.array(img)[:, :, ::-1]
    img = np.transpose(img_bgr, (2, 0, 1))[np.newaxis, :]
    return np.asarray(img, dtype="float32")


module, params = get_mobilenet()
ex = tvm.relay.create_executor("graph", mod=module)

input = get_cat_image()
result = ex.evaluate()(input, **params).numpy()

# print first 10 elements
print(result.flatten()[:10])

src_dtype = "float32"
dst_dtype = "custom[myfloat]32"

module = relay.transform.InferType()(module)

# Currently, custom datatypes only work if you run simplify_inference beforehand
module = tvm.relay.transform.SimplifyInference()(module)

# Run type inference before changing datatype
module = tvm.relay.transform.InferType()(module)

# Change datatype from float to myfloat and re-infer types
cdtype = ChangeDatatype(src_dtype, dst_dtype)
expr = cdtype.visit(module["main"])
module = tvm.relay.transform.InferType()(module)

# We also convert the parameters:
params = {k: convert_ndarray(dst_dtype, v) for k, v in params.items()}

# We also need to convert our input:
input = convert_ndarray(dst_dtype, input)


# Vectorization is not implemented with custom datatypes.
with tvm.transform.PassContext(config={"tir.disable_vectorize": True}):
    result_myfloat = ex.evaluate(expr)(input, **params)
    result_myfloat = convert_ndarray(src_dtype, result_myfloat).numpy()
    # print first 10 elements
    print(result_myfloat.flatten()[:10])

# Again, note that the output using 32-bit myfloat exactly the same as 32-bit floats,
# because myfloat is exactly a float!
np.testing.assert_array_equal(result, result_myfloat)
