from z3 import *

formula = '(x = y) and (((y = z) and not(x = z)) or (x = z))'

formula_list = ["AND", "x = y", ["OR", ["AND", "y = z", ["NOT", "x = z"]], "x = z"]]

'''
Usage: First time you pass the whole formula, the second time you pass the
whole formula + to_avoid =  result of the previous iteration.
'''
def get_inner_most(f_list, to_avoid=None):  # Todo: this works
    last_one = None
    while True:
        if to_avoid == f_list:
            return last_one
        if all(type(i) == str for i in f_list):
            return f_list
        for i in f_list:
            if type(i) == list:
                last_one = f_list
                f_list = i
                break


def sat_solver(f_list):
    variables = []
    sat_formula = None
    inner_most = get_inner_most(f_list)
    while True:
        if inner_most is None:
            break
        else:
            for i in inner_most[1:]:
                if type(i) == str:
                    variables.append(Bool(i))
            if inner_most[0] == "NOT":



s = Solver()
x = Bool("x")  # x = y
y = Bool("y")  # y = z
z = Bool("z")  # x = z

tmp = And(y, Not(z))
tmp = Or(tmp, z)
sat_solver = And(x, tmp)

solve(sat_solver)

dpt = And(x == y, y == z, Not(x == z))
solve(dpt)
