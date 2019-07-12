from z3 import *
# import builtins
# import os
#
# builtins.Z3_LIB_DIRS = [os.path.join("C:", "Users", "vulzaa", "Desktop", "Z3", "venv", "Lib", "site-packages", "z3",
#                                      "lib", "libz3.dll")]

c1 = 1, 3, -4
c2 = -1, 2
c3 = -1, -4, 3
c4 = -1, 3, 5

x1 = Bool("x1")
x2 = Bool("x2")
x3 = Bool("x3")
x4 = Bool("x4")
x5 = Bool("x5")

s = Solver()
s.add(Or(x1, x3, Not(x4)))
s.add(Or(Not(x1), x2))
s.add(Or(Not(x1), Not(x4), x3))
s.add(Or(Not(x1), x3, x5))

print(s.check())
print(s.model())
