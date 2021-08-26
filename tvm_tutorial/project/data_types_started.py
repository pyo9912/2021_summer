import tvm
from tvm import relay

import time

# Basic program: Z = X + Y
x = relay.var("x", shape=(3,), dtype="float32")
y = relay.var("y", shape=(3,), dtype="float32")
z = x + y

program = relay.Function([x,y],z)
module = tvm.IRModule.from_expr(program)

# Create random inputs to feed into this program using numpy
import numpy as np

np.random.seed(23)

x_input = np.random.rand(3).astype("float32")
y_input = np.random.rand(3).astype("float32")

print("x: {}".format(x_input))
print("y: {}".format(y_input))

ex = relay.create_executor(mod=module)

# start_time = time.time()
z_output = ex.evaluate()(x_input, y_input)
# end_time = time.time()

print("z: {}".format(z_output))
# print("WorkingTime: {} sec".format(end_time - start_time))
print(program)

# Register the custom type with TVM, giving it a name and type code
tvm.target.datatype.register("myfloat", 150)

x_myfloat = relay.cast(x, dtype="custom[myfloat]32")
y_myfloat = relay.cast(y, dtype="custom[myfloat]32")
z_myfloat = x_myfloat + y_myfloat
z = relay.cast(z_myfloat, dtype="float32")

# Create Add lowering function
tvm.target.datatype.register_op(
    tvm.target.datatype.create_lower_func({32: "Custom32Add"}),
    "Add",
    "llvm",
    "myfloat",
)

# Create lowering function
tvm.target.datatype.register_op(
    tvm.target.datatype.create_lower_func(
        {
            (32, 32): "FloatToCustom32",
        }
    ),
    "Cast",
    "llvm",
    "float",
    "myfloat",
)

compiled = ex.evaluate(program)
z_output_myfloat = compiled(x_input, y_input)

print("z: {}".format(z_output_myfloat))
print("x:\t\t{}".format(x_input))
print("y:\t\t{}".format(y_input))
print("z (float32):\t{}".format(z_output))
print("z (myfloat32):\t{}".format(z_output_myfloat))

# print("WorkingTime: {} sec".format(end_time - start_time))

program = relay.Function([x,y],z)
#module = tvm.IRModule.from_expr(program)
#module = relay.transform.InferType()(module)

print(program)


