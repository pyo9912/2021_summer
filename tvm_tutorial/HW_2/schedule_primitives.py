from __future__ import absolute_import, print_function

import tvm
from tvm import te
import numpy as np

# declare some variables for use later
n = te.var("n")
m = te.var("m")

# declare a matrix element-wise multiply
A = te.placeholder((m, n), name="A")
B = te.placeholder((m, n), name="B")
C = te.compute((m, n), lambda i, j: A[i, j] * B[i, j], name="C")

s = te.create_schedule([C.op])
# lower will transform the computation from definition to the real
# callable function. With argument `simple_mode=True`, it will
# return you a readable C like statement, we use it here to print the
# schedule result.
print(tvm.lower(s, [A, B, C], simple_mode=True))

# :code:`split` can split a specified axis into two axes by
# :code:`factor`.
A = te.placeholder((m,), name="A")
B = te.compute((m,), lambda i: A[i] * 2, name="B")

s = te.create_schedule(B.op)
xo, xi = s[B].split(B.op.axis[0], factor=32)
print(tvm.lower(s, [A, B], simple_mode=True))

# You can also split a axis by :code:`nparts`, which splits the axis
# contrary with :code:`factor`.
A = te.placeholder((m,), name="A")
B = te.compute((m,), lambda i: A[i], name="B")

s = te.create_schedule(B.op)
bx, tx = s[B].split(B.op.axis[0], nparts=32)
print(tvm.lower(s, [A, B], simple_mode=True))

# :code:`tile` help you execute the computation tile by tile over two
# axes.
A = te.placeholder((m, n), name="A")
B = te.compute((m, n), lambda i, j: A[i, j], name="B")

s = te.create_schedule(B.op)
xo, yo, xi, yi = s[B].tile(B.op.axis[0], B.op.axis[1], x_factor=10, y_factor=5)
print(tvm.lower(s, [A, B], simple_mode=True))

# :code:`fuse` can fuse two consecutive axes of one computation.
A = te.placeholder((m, n), name="A")
B = te.compute((m, n), lambda i, j: A[i, j], name="B")

s = te.create_schedule(B.op)
# tile to four axes first: (i.outer, j.outer, i.inner, j.inner)
xo, yo, xi, yi = s[B].tile(B.op.axis[0], B.op.axis[1], x_factor=10, y_factor=5)
# then fuse (i.inner, j.inner) into one axis: (i.inner.j.inner.fused)
fused = s[B].fuse(xi, yi)
print(tvm.lower(s, [A, B], simple_mode=True))

# :code:`reorder` can reorder the axes in the specified order.
A = te.placeholder((m, n), name="A")
B = te.compute((m, n), lambda i, j: A[i, j], name="B")

s = te.create_schedule(B.op)
# tile to four axes first: (i.outer, j.outer, i.inner, j.inner)
xo, yo, xi, yi = s[B].tile(B.op.axis[0], B.op.axis[1], x_factor=10, y_factor=5)
# then reorder the axes: (i.inner, j.outer, i.outer, j.inner)
s[B].reorder(xi, yo, xo, yi)
print(tvm.lower(s, [A, B], simple_mode=True))

# :code:`bind` can bind a specified axis with a thread axis, often used
# in gpu programming.
A = te.placeholder((n,), name="A")
B = te.compute(A.shape, lambda i: A[i] * 2, name="B")

s = te.create_schedule(B.op)
bx, tx = s[B].split(B.op.axis[0], factor=64)
s[B].bind(bx, te.thread_axis("blockIdx.x"))
s[B].bind(tx, te.thread_axis("threadIdx.x"))
print(tvm.lower(s, [A, B], simple_mode=True))

# For a schedule that consists of multiple operators, TVM will compute
# tensors at the root separately by default.
A = te.placeholder((m,), name="A")
B = te.compute((m,), lambda i: A[i] + 1, name="B")
C = te.compute((m,), lambda i: B[i] * 2, name="C")

s = te.create_schedule(C.op)
print(tvm.lower(s, [A, B, C], simple_mode=True))

# :code:`compute_at` can move computation of `B` into the first axis
# of computation of `C`.
A = te.placeholder((m,), name="A")
B = te.compute((m,), lambda i: A[i] + 1, name="B")
C = te.compute((m,), lambda i: B[i] * 2, name="C")

s = te.create_schedule(C.op)
s[B].compute_at(s[C], C.op.axis[0])
print(tvm.lower(s, [A, B, C], simple_mode=True))

# :code:`compute_inline` can mark one stage as inline, then the body of
# computation will be expanded and inserted at the address where the
# tensor is required.
A = te.placeholder((m,), name="A")
B = te.compute((m,), lambda i: A[i] + 1, name="B")
C = te.compute((m,), lambda i: B[i] * 2, name="C")

s = te.create_schedule(C.op)
s[B].compute_inline()
print(tvm.lower(s, [A, B, C], simple_mode=True))

# :code:`compute_root` can move computation of one stage to the root.
A = te.placeholder((m,), name="A")
B = te.compute((m,), lambda i: A[i] + 1, name="B")
C = te.compute((m,), lambda i: B[i] * 2, name="C")

s = te.create_schedule(C.op)
s[B].compute_at(s[C], C.op.axis[0])
s[B].compute_root()
print(tvm.lower(s, [A, B, C], simple_mode=True))


