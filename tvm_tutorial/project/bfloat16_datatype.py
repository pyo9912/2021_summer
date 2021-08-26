import tvm

from tvm import relay

import time



# Basic program: Z = X + Y
x = relay.var("x", shape=(3,), dtype="float16")
y = relay.var("y", shape=(3,), dtype="float16")
z = x + y

program = relay.Function([x,y],z)
module = tvm.IRModule.from_expr(program)

# Create random inputs to feed into this program using numpy
import numpy as np

np.random.seed(23)

x_input = np.random.rand(3).astype("float16")
y_input = np.random.rand(3).astype("float16")

print("x: {}".format(x_input))
print("y: {}".format(y_input))

ex = relay.create_executor(mod=module)

# start_time = time.time()
z_output = ex.evaluate()(x_input, y_input)
# end_time = time.time()

print("z: {}".format(z_output))
# print("WorkingTime: {} sec".format(end_time - start_time))
print(program)
i
